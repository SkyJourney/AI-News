#!/usr/bin/env python3
"""arxiv-fulltext.py — arxiv 论文全文抓取（F1 · 60-Originals 层）

arxiv URL 分流 + subprocess 调 fetch-with-assets.py + arxiv API metadata 补齐。
KISS 原则：不重造 HTML 抓取轮子，只写 arxiv 特化的分流与元数据补齐逻辑。

三级降级：
  1. arxiv 官方 HTML: https://arxiv.org/html/<id>       ← 2023+ 论文通常有
  2. ar5iv 社区镜像: https://ar5iv.labs.arxiv.org/html/<base_id>
  3. arxiv API 摘要兜底: 只输出 title/authors/abstract + PDF 链接

约束：
- fcntl.flock 跨进程串行 arxiv 请求 + 请求后 sleep(3)（arxiv 3s 礼仪）
- 复用 fetch-with-assets.py（subprocess），共享清洗/图片下载逻辑

使用：
    ~/miniconda3/envs/ai-news/bin/python3 arxiv-fulltext.py <arxiv_id_or_url> \\
      --out-dir /Volumes/Projects/AInews/60-Originals \\
      --id 2026-07-01-0816-attention-is-all-you-need \\
      --date 2026-07-01 \\
      [--timeout 30]

<arxiv_id_or_url> 接受：
    2606.30645v1 / 2606.30645
    http://arxiv.org/abs/2606.30645v1
    https://arxiv.org/pdf/2606.30645v1
    https://huggingface.co/papers/2606.29308

exit code:
    0 = 成功（含 fallback 到 API 摘要）
    1 = fatal（arxiv ID 解析失败 / arxiv API 也不可用）

输出（stdout）：JSON，字段与 fetch-with-assets.py 一致 + arxiv 特有字段
"""

import argparse
import datetime as dt
import fcntl
import html as html_lib
import json
import re
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Tuple, Optional, Dict

# ============================================================
# 常量
# ============================================================
ARXIV_API = "http://export.arxiv.org/api/query"
LOCK_PATH = "/tmp/ainews-arxiv-fulltext.lock"
RATE_LIMIT_SEC = 3.0
USER_AGENT = "AInews-skill/1.0 (arxiv-fulltext; https://github.com/local/ainews)"

FETCH_WITH_ASSETS = Path(__file__).parent / "fetch-with-assets.py"

# arxiv ID 匹配：YYYY.NNNNN (可选 vN)；旧格式 category/YYMMNNN 暂不支持
ARXIV_ID_RE = re.compile(r"(\d{4}\.\d{4,5})(v\d+)?")


# ============================================================
# ID 解析
# ============================================================
def parse_arxiv_id(input_str: str) -> Tuple[Optional[str], Optional[str]]:
    """从任意输入抽 canonical arxiv ID。返回 (full_id_with_v, base_id_no_v)"""
    m = ARXIV_ID_RE.search(input_str)
    if not m:
        return None, None
    base_id = m.group(1)
    version = m.group(2) or ""
    full_id = base_id + version
    return full_id, base_id


# ============================================================
# arxiv 限流（跨进程 flock）
# ============================================================
_lock_fd = None


def acquire_rate_limit_lock():
    """获取跨进程互斥锁——脚本入口调用一次"""
    global _lock_fd
    _lock_fd = open(LOCK_PATH, "a")
    fcntl.flock(_lock_fd.fileno(), fcntl.LOCK_EX)


def release_rate_limit_lock():
    """请求完成后先 sleep(3) 再释放锁——保证下一次 arxiv 请求间隔"""
    global _lock_fd
    if _lock_fd is not None:
        time.sleep(RATE_LIMIT_SEC)
        fcntl.flock(_lock_fd.fileno(), fcntl.LOCK_UN)
        _lock_fd.close()
        _lock_fd = None


# ============================================================
# arxiv API 元数据
# ============================================================
def fetch_arxiv_api_meta(arxiv_id: str, timeout: int) -> dict:
    """调 arxiv API 拿 title/authors/abstract/published；失败返回空字段"""
    empty = {"title": "", "author": [], "published_at": "", "abstract": "", "api_error": None}
    url = f"{ARXIV_API}?{urllib.parse.urlencode({'id_list': arxiv_id})}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            xml = resp.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, urllib.error.HTTPError, socket.timeout) as e:
        empty["api_error"] = f"api_{type(e).__name__}: {e}"
        return empty

    # entry 段
    entry_m = re.search(r"<entry>(.*?)</entry>", xml, re.DOTALL)
    if not entry_m:
        empty["api_error"] = "api_no_entry"
        return empty
    entry = entry_m.group(1)

    def take(pat: str) -> str:
        m = re.search(pat, entry, re.DOTALL)
        return html_lib.unescape(m.group(1).strip()) if m else ""

    title = re.sub(r"\s+", " ", take(r"<title>(.*?)</title>"))
    summary = re.sub(r"\s+", " ", take(r"<summary>(.*?)</summary>"))
    published = take(r"<published>(\d{4}-\d{2}-\d{2})")
    authors = [
        html_lib.unescape(m.group(1).strip())
        for m in re.finditer(r"<author>\s*<name>(.*?)</name>", entry, re.DOTALL)
    ]
    return {
        "title": title,
        "author": authors,
        "published_at": published,
        "abstract": summary,
        "api_error": None,
    }


# ============================================================
# 调 fetch-with-assets.py
# ============================================================
def try_fetch_html_via_subprocess(
    url: str, out_dir: str, target_id: str, date: str, timeout: int
) -> Optional[Dict]:
    """subprocess 调 fetch-with-assets.py；成功返回 dict，失败返回 None"""
    try:
        result = subprocess.run(
            [
                sys.executable,
                str(FETCH_WITH_ASSETS),
                url,
                "--out-dir", out_dir,
                "--id", target_id,
                "--date", date,
                "--timeout", str(timeout),
                "--ua-mode", "project",  # arxiv/ar5iv 用署名 UA（尊重）
            ],
            capture_output=True,
            text=True,
            timeout=timeout + 60,  # 给图片下载留余量
        )
        data = json.loads(result.stdout)
        return data if data.get("error") is None else None
    except (subprocess.TimeoutExpired, json.JSONDecodeError, subprocess.SubprocessError):
        return None


# ============================================================
# 主流程
# ============================================================
def now_iso() -> str:
    tz = dt.timezone(dt.timedelta(hours=8))
    return dt.datetime.now(tz).replace(microsecond=0).isoformat()


def build_fallback_result(
    full_id: str, meta: dict, source_url: str, notice: str
) -> dict:
    """arxiv HTML 都失败时的兜底：只有 abstract + PDF 链接"""
    pdf_url = f"https://arxiv.org/pdf/{full_id}"
    abstract_html = html_lib.escape(meta.get("abstract", ""))
    title_html = html_lib.escape(meta.get("title", ""))
    cleaned_html = (
        f"<article>"
        f"<h1>{title_html}</h1>"
        f"<p><strong>Abstract:</strong> {abstract_html}</p>"
        f'<p><em>arxiv HTML 版本不可用；请查看 <a href="{html_lib.escape(pdf_url)}">PDF</a></em></p>'
        f"</article>"
    )
    return {
        "url": source_url,
        "title": meta.get("title", ""),
        "original_title": meta.get("title", ""),
        "author": meta.get("author", []),
        "published_at": meta.get("published_at", ""),
        "language": "en",
        "cleaned_html": cleaned_html,
        "images_attempted": 0,
        "images_saved": 0,
        "images": [],
        "fetched_at": now_iso(),
        "error": None,
        "arxiv_id": full_id,
        "abstract": meta.get("abstract", ""),
        "pdf_url": pdf_url,
        "source_html_url": None,
        "fallback_notice": notice,
    }


def parse_args():
    p = argparse.ArgumentParser(description="arxiv 论文全文抓取（HTML/PDF 双通道）")
    p.add_argument("input", help="arxiv ID 或 URL")
    p.add_argument("--out-dir", required=True, help="60-Originals 目录（assets 写入 _assets/DATE/）")
    p.add_argument("--id", required=True, help="Target id (YYYY-MM-DD-HHMM-slug)")
    p.add_argument("--date", required=True, help="YYYY-MM-DD, 用于 _assets 分区")
    p.add_argument("--timeout", type=int, default=30, help="HTML fetch timeout seconds (默认 30)")
    return p.parse_args()


def main() -> int:
    args = parse_args()

    full_id, base_id = parse_arxiv_id(args.input)
    if not full_id:
        result = {
            "url": args.input,
            "title": "", "original_title": "", "author": [], "published_at": "",
            "language": "", "cleaned_html": "", "images_attempted": 0,
            "images_saved": 0, "images": [],
            "fetched_at": now_iso(),
            "error": "arxiv_id_parse_failed",
            "arxiv_id": None, "abstract": "", "pdf_url": None,
            "source_html_url": None, "fallback_notice": None,
        }
        print(json.dumps(result, ensure_ascii=False))
        return 1

    # ============================================================
    # 全局限流锁（覆盖所有 arxiv 网络请求）
    # ============================================================
    acquire_rate_limit_lock()
    try:
        # 元数据先拿（API 稳定，不算大流量）
        meta = fetch_arxiv_api_meta(full_id, args.timeout)

        # 依次尝试 arxiv 官方 HTML → ar5iv
        candidates = [
            (f"https://arxiv.org/html/{full_id}", "arxiv_html_official"),
            (f"https://ar5iv.labs.arxiv.org/html/{base_id}", "arxiv_html_ar5iv"),
        ]
        html_result: Optional[Dict] = None
        tried_urls: list[str] = []
        for url, label in candidates:
            tried_urls.append(url)
            data = try_fetch_html_via_subprocess(
                url, args.out_dir, args.id, args.date, args.timeout
            )
            if data is not None:
                html_result = data
                html_result["source_html_url"] = url
                html_result["_source_label"] = label
                break
    finally:
        release_rate_limit_lock()

    # ============================================================
    # 结果组装
    # ============================================================
    if html_result:
        # HTML 成功——用 API 元数据补齐 title/author/published（arxiv HTML 版元数据常不全）
        if not html_result.get("title") and meta.get("title"):
            html_result["title"] = meta["title"]
            html_result["original_title"] = meta["title"]
        if not html_result.get("author") and meta.get("author"):
            html_result["author"] = meta["author"]
        if not html_result.get("published_at") and meta.get("published_at"):
            html_result["published_at"] = meta["published_at"]
        html_result["language"] = html_result.get("language") or "en"
        html_result["arxiv_id"] = full_id
        html_result["abstract"] = meta.get("abstract", "")
        html_result["pdf_url"] = f"https://arxiv.org/pdf/{full_id}"
        html_result["fallback_notice"] = None
        html_result.pop("_source_label", None)
        print(json.dumps(html_result, ensure_ascii=False))
        return 0

    # HTML 全失败——检查 API 是否也失败
    if meta.get("api_error"):
        result = build_fallback_result(
            full_id, meta,
            source_url=f"https://arxiv.org/abs/{full_id}",
            notice=f"arxiv HTML 版和 ar5iv 都不可用；arxiv API 也失败：{meta['api_error']}",
        )
        result["error"] = "all_channels_failed"
        print(json.dumps(result, ensure_ascii=False))
        return 1

    # HTML 全失败但 API 有效——走摘要兜底
    notice = f"arxiv HTML 版和 ar5iv 都不可用（尝试 URL: {', '.join(tried_urls)}）；仅提供摘要 + PDF 链接"
    result = build_fallback_result(
        full_id, meta,
        source_url=f"https://arxiv.org/abs/{full_id}",
        notice=notice,
    )
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
