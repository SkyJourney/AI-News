#!/usr/bin/env python3
"""fetch-with-assets.py — 通用 HTML 抓取 + 图片下载（F1 · 60-Originals 层）

给 news-originalizer subagent 提供 IO + 清洗能力：抓 HTML → 清噪 → 抽正文 →
下载图片到 _assets/YYYY-MM-DD/ → rewrite <img src> 为本地相对路径 → 输出 JSON。
下游 agent 用 LLM 一步做 HTML→Markdown + 翻译，脚本不介入语言层。

约束：
- 纯 Python 标准库（无第三方依赖），沿用 scripts/ 惯例
- 默认浏览器 UA，可切署名 UA（--ua-mode project）
- 图片降级：下载失败保留原 URL + alt，加 data-fallback-reason 供 agent 识别

使用：
    python3 fetch-with-assets.py <URL> \\
      --out-dir /Volumes/Projects/AInews/60-Originals \\
      --id 2026-07-01-0816-openai-gpt5-preview \\
      --date 2026-07-01 \\
      [--timeout 30] \\
      [--max-image-bytes 5242880] \\
      [--ua-mode browser|project]

exit code:
    0 = 成功（HTML 拿到，图片可能部分失败）
    1 = fatal（HTML 拿不到 / 参数错）
    2 = HTML OK 但所有图都挂

输出（stdout）：JSON，见 vault-schema.md §3 60-Originals frontmatter 契约
"""

import argparse
import datetime as dt
import html as html_lib
import json
import re
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

# ============================================================
# 常量
# ============================================================
UA_BROWSER = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
UA_PROJECT = "AInews-skill/1.0 (personal-vault; https://github.com/local/ainews)"

IMAGE_TIMEOUT_SEC = 15

# ─── Jina Reader 兜底（Cloudflare 挑战 / rate limit / timeout 场景） ───
# 免 auth HTTPS GET，非第三方 MCP，符合 CLAUDE.md D5 边界
JINA_READER_BASE = "https://r.jina.ai/"
JINA_TRIGGER_ERRORS = {"http_403", "http_429", "http_503", "timeout"}
JINA_TIMEOUT_SEC = 45  # Jina 内部跑 headless render，比直连宽松

# 噪声标签（连同内容一并删除）
NOISE_TAG_RE = re.compile(
    r"<(script|style|noscript|nav|header|footer|aside|form|iframe|template|svg)\b[^>]*>.*?</\1>",
    re.IGNORECASE | re.DOTALL,
)
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)

MIME_EXT_MAP = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/gif": ".gif",
    "image/webp": ".webp",
    "image/svg+xml": ".svg",
    "image/avif": ".avif",
    "image/bmp": ".bmp",
}
ALLOWED_IMG_EXTS = set(MIME_EXT_MAP.values()) | {".jpeg"}

IMG_TAG_RE = re.compile(r"<img\b([^>]*?)/?>", re.IGNORECASE)
ATTR_RE = re.compile(r'(\w[\w\-]*)\s*=\s*(["\'])(.*?)\2', re.IGNORECASE | re.DOTALL)


# ============================================================
# HTTP 抓取
# ============================================================
def fetch_html(url: str, timeout: int, ua: str):
    """返回 (html_text, error)。error=None 表示成功"""
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": ua,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            raw = resp.read()
            return raw.decode(charset, errors="replace"), None
    except urllib.error.HTTPError as e:
        return None, f"http_{e.code}"
    except urllib.error.URLError as e:
        return None, f"url_error: {e.reason}"
    except socket.timeout:
        return None, "timeout"
    except Exception as e:
        return None, f"unexpected: {type(e).__name__}: {e}"


def fetch_via_jina(url: str, timeout: int = JINA_TIMEOUT_SEC):
    """Jina Reader 兜底通道，返回 (markdown_body, title, published_time, error)

    Jina 响应体结构：
        Title: <title>

        URL Source: <url>

        Published Time: <YYYY-MM-DDTHH:MM:SSZ>   # 可选，非所有站点都有

        Markdown Content:
        <正文 markdown>

    解析策略：前 8 行遍历抽字段，"Markdown Content:" 之后全部为正文。
    走 splitlines() 而非 split("Markdown Content:") 避免正文里同串误切。
    """
    try:
        jina_url = JINA_READER_BASE + url
        req = urllib.request.Request(
            jina_url,
            headers={"User-Agent": UA_PROJECT, "Accept": "text/plain, */*"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return None, None, None, f"jina_http_{e.code}"
    except urllib.error.URLError as e:
        return None, None, None, f"jina_url_error: {e.reason}"
    except socket.timeout:
        return None, None, None, "jina_timeout"
    except Exception as e:
        return None, None, None, f"jina_unexpected: {type(e).__name__}: {e}"

    title, published_time = "", ""
    lines = raw.splitlines()
    body_start = 0
    for i, line in enumerate(lines[:8]):
        if line.startswith("Title:"):
            title = line[len("Title:"):].strip()
        elif line.startswith("Published Time:"):
            published_time = line[len("Published Time:"):].strip()
        elif line.startswith("Markdown Content:"):
            body_start = i + 1
            break

    markdown_body = "\n".join(lines[body_start:]).strip()
    if not markdown_body:
        return None, None, None, "jina_empty_body"
    return markdown_body, title, published_time, None


# ============================================================
# 元数据抽取
# ============================================================
def _first_group(pattern: str, text: str):
    m = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    return m.group(1).strip() if m else None


def extract_metadata(html_text: str) -> dict:
    """抽 title/author/published_at/language；缺失时字段为空字符串或空数组"""
    title = (
        _first_group(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)["\']', html_text)
        or _first_group(r'<meta[^>]+name=["\']og:title["\'][^>]+content=["\']([^"\']+)["\']', html_text)
        or _first_group(r'<meta[^>]+name=["\']twitter:title["\'][^>]+content=["\']([^"\']+)["\']', html_text)
        or _first_group(r"<title[^>]*>([^<]+)</title>", html_text)
        or ""
    )
    title = html_lib.unescape(title).strip()

    author_raw = (
        _first_group(r'<meta[^>]+name=["\']author["\'][^>]+content=["\']([^"\']+)["\']', html_text)
        or _first_group(r'<meta[^>]+property=["\']article:author["\'][^>]+content=["\']([^"\']+)["\']', html_text)
        or ""
    )
    authors = []
    if author_raw:
        for a in re.split(r"[,;、]", author_raw):
            a = html_lib.unescape(a).strip()
            if a:
                authors.append(a)

    published = (
        _first_group(r'<meta[^>]+property=["\']article:published_time["\'][^>]+content=["\']([^"\']+)["\']', html_text)
        or _first_group(r'<meta[^>]+name=["\']pubdate["\'][^>]+content=["\']([^"\']+)["\']', html_text)
        or _first_group(r'<meta[^>]+name=["\']date["\'][^>]+content=["\']([^"\']+)["\']', html_text)
        or _first_group(r'<meta[^>]+itemprop=["\']datePublished["\'][^>]+content=["\']([^"\']+)["\']', html_text)
        or _first_group(r'<time[^>]+datetime=["\']([^"\']+)["\']', html_text)
        or ""
    )
    if published:
        m = re.match(r"(\d{4})-(\d{2})-(\d{2})", published)
        if m:
            published = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"

    language = _first_group(r'<html[^>]+lang=["\']([a-zA-Z\-]+)["\']', html_text) or ""
    if language:
        language = language.split("-")[0].lower()

    return {
        "title": title,
        "original_title": title,
        "author": authors,
        "published_at": published,
        "language": language,
    }


# ============================================================
# HTML 清洗 + 正文抽取
# ============================================================
def strip_noise(html_text: str) -> str:
    """删除 script/style/noscript/nav/header/footer/aside/form/iframe/template/svg 及 HTML 注释"""
    html_text = HTML_COMMENT_RE.sub("", html_text)
    prev = None
    while prev != html_text:  # 循环消灭嵌套
        prev = html_text
        html_text = NOISE_TAG_RE.sub("", html_text)
    return html_text


def extract_main_content(html_text: str) -> str:
    """按 <main> / <article>（取最长）/ [role=main] / <body> 兜底顺序抽正文"""
    m = re.search(r"<main\b[^>]*>.*?</main>", html_text, re.IGNORECASE | re.DOTALL)
    if m:
        return m.group(0)
    articles = re.findall(r"<article\b[^>]*>.*?</article>", html_text, re.IGNORECASE | re.DOTALL)
    if articles:
        return max(articles, key=len)
    m = re.search(r'<(\w+)[^>]+role=["\']main["\'][^>]*>.*?</\1>', html_text, re.IGNORECASE | re.DOTALL)
    if m:
        return m.group(0)
    m = re.search(r"<body\b[^>]*>(.*?)</body>", html_text, re.IGNORECASE | re.DOTALL)
    if m:
        return f"<div>{m.group(1)}</div>"
    return html_text


# ============================================================
# 图片抽取 + 下载
# ============================================================
def parse_img_attrs(attrs_str: str) -> dict:
    return {m.group(1).lower(): html_lib.unescape(m.group(3)) for m in ATTR_RE.finditer(attrs_str)}


def pick_img_src(attrs: dict):
    """按优先级选 src：data-src > data-original > src > srcset 首 URL；跳过 data: URI

    修 A：src 提到 srcset 之前——srcset URL 内可能含逗号（Cloudinary 变换参数
    `w_320,c_limit,f_auto,q_auto:good`），简单 split(',') 会切碎；改用正则抽首个绝对 URL
    """
    for key in ("data-src", "data-original", "src"):
        v = attrs.get(key)
        if v and not v.startswith("data:"):
            return v
    srcset = attrs.get("srcset")
    if srcset:
        m = re.match(r"(https?://\S+?)(?:\s+\d+[wx])?(?:$|,)", srcset)
        if m and not m.group(1).startswith("data:"):
            return m.group(1)
    return None


def guess_ext(url: str, content_type):
    """按 Content-Type 优先，回退 URL 后缀，兜底 .bin"""
    if content_type:
        base = content_type.split(";")[0].strip().lower()
        if base in MIME_EXT_MAP:
            return MIME_EXT_MAP[base]
    path = urllib.parse.urlparse(url).path
    ext = Path(path).suffix.lower()
    if ext in ALLOWED_IMG_EXTS:
        return ".jpg" if ext == ".jpeg" else ext
    return ".bin"


def download_image(url: str, target_stem: Path, max_bytes: int, ua: str, referer: str | None = None):
    """返回 (成功?, 详情 dict)。修 B：加 Referer 头绕过 CDN 防盗链（qbitai 类）"""
    try:
        headers = {"User-Agent": ua, "Accept": "image/*,*/*;q=0.8"}
        if referer:
            headers["Referer"] = referer
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=IMAGE_TIMEOUT_SEC) as resp:
            content_type = resp.headers.get("Content-Type")
            content_length_hdr = resp.headers.get("Content-Length")
            if content_length_hdr and int(content_length_hdr) > max_bytes:
                return False, {"reason": "too_large", "size_bytes": int(content_length_hdr)}
            data = resp.read(max_bytes + 1)
            if len(data) > max_bytes:
                return False, {"reason": "too_large", "size_bytes": len(data)}
            ext = guess_ext(url, content_type)
            if ext == ".bin":
                return False, {"reason": "unknown_content_type", "content_type": content_type}
            target = target_stem.with_suffix(ext)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            return True, {"local_path": target, "size_bytes": len(data), "content_type": content_type}
    except urllib.error.HTTPError as e:
        return False, {"reason": f"http_{e.code}"}
    except urllib.error.URLError as e:
        return False, {"reason": f"url_error: {e.reason}"}
    except socket.timeout:
        return False, {"reason": "timeout"}
    except Exception as e:
        return False, {"reason": f"unexpected: {type(e).__name__}: {e}"}


def process_images(html_text, base_url, out_dir, target_id, date, max_bytes, ua):
    """扫图 → 下载 → rewrite <img src> 为本地相对路径 → 返回 (rewritten_html, manifest)"""
    manifest = []
    assets_dir = out_dir / "_assets" / date
    matches = list(IMG_TAG_RE.finditer(html_text))
    # (start, end, new_tag)，最后从后往前 apply 避免 offset 漂移
    replacements = []

    for n, m in enumerate(matches, start=1):
        attrs = parse_img_attrs(m.group(1))
        src_raw = pick_img_src(attrs)
        alt = attrs.get("alt", "")
        entry = {"n": n, "alt_text": alt}

        if not src_raw:
            entry.update({"status": "no_src", "src_url": None, "local_path": None})
            manifest.append(entry)
            continue

        if src_raw.startswith("data:"):
            entry.update({"status": "skipped_data_uri", "src_url": src_raw[:80], "local_path": None})
            manifest.append(entry)
            continue

        abs_url = urllib.parse.urljoin(base_url, src_raw)
        entry["src_url"] = abs_url
        target_stem = assets_dir / f"{target_id}-{n:03d}"
        ok, info = download_image(abs_url, target_stem, max_bytes, ua, referer=base_url)

        if ok:
            rel = str(info["local_path"].relative_to(out_dir))
            new_tag = (
                f'<img src="{html_lib.escape(rel)}" '
                f'alt="{html_lib.escape(alt)}" '
                f'data-original-src="{html_lib.escape(abs_url)}"/>'
            )
            entry.update({
                "status": "saved",
                "local_path": rel,
                "size_bytes": info["size_bytes"],
                "content_type": info.get("content_type"),
            })
        else:
            new_tag = (
                f'<img src="{html_lib.escape(abs_url)}" '
                f'alt="{html_lib.escape(alt)}" '
                f'data-fallback-reason="{html_lib.escape(info["reason"])}"/>'
            )
            entry.update({"status": "failed", "local_path": None, **info})

        replacements.append((m.start(), m.end(), new_tag))
        manifest.append(entry)

    for start, end, new in reversed(replacements):
        html_text = html_text[:start] + new + html_text[end:]

    return html_text, manifest


# ============================================================
# 主流程
# ============================================================
def now_iso() -> str:
    tz = dt.timezone(dt.timedelta(hours=8))
    return dt.datetime.now(tz).replace(microsecond=0).isoformat()


def parse_args():
    p = argparse.ArgumentParser(description="Fetch HTML + download images for 60-Originals layer")
    p.add_argument("url", help="Target URL to fetch")
    p.add_argument("--out-dir", required=True, help="60-Originals 目录（assets 写入 _assets/DATE/）")
    p.add_argument("--id", required=True, help="Target id (YYYY-MM-DD-HHMM-slug)")
    p.add_argument("--date", required=True, help="YYYY-MM-DD, 用于 _assets 分区")
    p.add_argument("--timeout", type=int, default=30, help="HTML fetch timeout seconds (默认 30)")
    p.add_argument("--max-image-bytes", type=int, default=5 * 1024 * 1024, help="每张图上限 bytes（默认 5MB）")
    p.add_argument("--ua-mode", choices=["browser", "project"], default="browser", help="UA 风格")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    ua = UA_BROWSER if args.ua_mode == "browser" else UA_PROJECT
    out_dir = Path(args.out_dir)

    html_text, err = fetch_html(args.url, args.timeout, ua)

    # ─── Jina Reader 兜底 ───
    # 触发场景：CF 挑战（403）/ rate limit（429）/ 5xx 挑战（503）/ timeout
    if err in JINA_TRIGGER_ERRORS:
        md_body, md_title, md_pub, jina_err = fetch_via_jina(args.url)
        if jina_err is None:
            # 归一化 published_time 到 YYYY-MM-DD
            published_norm = ""
            if md_pub:
                m = re.match(r"(\d{4})-(\d{2})-(\d{2})", md_pub)
                if m:
                    published_norm = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
            result = {
                "url": args.url,
                "title": md_title,
                "original_title": md_title,
                "author": [],
                "published_at": published_norm,
                "language": "",  # Jina 不给 lang meta，交 agent 从正文推断
                "cleaned_html": "",
                "cleaned_markdown": md_body,
                "images_attempted": 0,
                "images_saved": 0,
                "images": [],
                "fetched_at": now_iso(),
                "fetch_channel": "jina",
                "fetch_channel_note": f"direct {err}; jina ok",
                "error": None,
            }
            print(json.dumps(result, ensure_ascii=False))
            return 0
        # Jina 也挂，把两级 error 都带出去让 agent 走 Fallback A/B
        err = f"{err}; {jina_err}"

    if err:
        result = {
            "url": args.url,
            "title": "",
            "original_title": "",
            "author": [],
            "published_at": "",
            "language": "",
            "cleaned_html": "",
            "cleaned_markdown": "",
            "images_attempted": 0,
            "images_saved": 0,
            "images": [],
            "fetched_at": now_iso(),
            "fetch_channel": "direct",
            "fetch_channel_note": err,
            "error": err,
        }
        print(json.dumps(result, ensure_ascii=False))
        return 1

    # ─── direct 通道正常流程 ───
    meta = extract_metadata(html_text)
    cleaned = strip_noise(html_text)
    main_content = strip_noise(extract_main_content(cleaned))

    rewritten, images = process_images(
        main_content,
        args.url,
        out_dir,
        args.id,
        args.date,
        args.max_image_bytes,
        ua,
    )

    result = {
        "url": args.url,
        **meta,
        "cleaned_html": rewritten,
        "cleaned_markdown": "",
        "images_attempted": len(images),
        "images_saved": sum(1 for i in images if i["status"] == "saved"),
        "images": images,
        "fetched_at": now_iso(),
        "fetch_channel": "direct",
        "fetch_channel_note": "direct ok",
        "error": None,
    }
    print(json.dumps(result, ensure_ascii=False))

    if images and all(i["status"] != "saved" for i in images):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
