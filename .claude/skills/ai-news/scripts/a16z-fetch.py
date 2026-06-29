#!/usr/bin/env python3
"""a16z-fetch.py — a16z News & Content 列表页抓取 + 详情页日期回填

为什么有这个脚本：
- a16z 经典 RSS feed/ 已死约 2 年
- /news-content/ 列表页 HTML 中没有 entry 自身的发布日期，只有 CSS class `bg-tag-new` 标记最新一批
- WebFetch 工具取页面级 schema.org datePublished 会错——那是页面整体创建时间（如 2026-01-15），不是各 entry 的真实日期
- 真实日期藏在每个 announcement 详情页的 schema.org datePublished

策略：
1. curl 列表页拿全部 entries 元数据（title / url / category / is_new_tagged）
2. 对前 N 条 entries 逐个 curl 详情页拿真实 datePublished（串行 + 0.5s 礼仪间隔）
3. 输出统一 JSON 给 news-fetcher-script subagent

使用：
    python3 a16z-fetch.py [--max N] [--detail-limit N]
    # 默认 max=15（列表页前 15 条），detail-limit=15（全部拉详情）

输出（stdout）：
    {"entries":[{title, url, category, is_new_tagged, published, published_source}],
     "fetched_at":"...","stats":{...}}
"""

import argparse
import datetime as dt
import json
import re
import sys
import time
import urllib.request
from typing import List, Dict, Optional, Tuple, Set

LIST_URL = "https://a16z.com/news-content/"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 AInews-bot/1.0"
DETAIL_RATE_LIMIT_SEC = 0.5  # 详情页串行间隔（礼仪）


def fetch(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def parse_list_page(html: str, limit: int) -> List[Dict]:
    """从列表页 HTML 抽出 entries。每个 entry 是一个 <div ... data-feed-item> 块。

    去重：列表页同条目可能出现两次（一次在 The Latest 区，一次在分类列表区），按 URL dedup 保留首次。
    """
    entries: List[Dict] = []
    seen_urls: Set[str] = set()

    # 切分每个 data-feed-item 块（用 data-feed-item 属性作锚点，截到下一个 data-feed-item 或文档末尾）
    blocks = re.split(r'<div [^>]*data-feed-item[^>]*>', html)[1:]  # 第 0 段是 data-feed-item 前的内容

    for raw_block in blocks:
        # 一个块结束在下一个 data-feed-item 之前，或在某个保险锚（如 <footer 或 <script id="footer-data"）
        # 简单做法：取前 3000 字符已经覆盖一个完整 card
        block = raw_block[:3000]

        # 抽 URL（第一个 <a href="..."> 即标题链接）
        url_m = re.search(r'<a href="(https?://a16z\.com/[^"]+)"', block)
        if not url_m:
            continue
        url = url_m.group(1).rstrip("/")
        # 跳过非文章链接（如 /author/ 或 /tag/ 之类）
        if any(skip in url for skip in ['/author/', '/tag/', '/category/', '/page/']):
            continue
        if url in seen_urls:
            continue
        seen_urls.add(url)

        # 抽标题（<a> 标签内文本，去前后空白）
        title_m = re.search(r'<a href="' + re.escape(url) + r'/?"[^>]*>\s*(.+?)\s*</a>', block, re.DOTALL)
        title = title_m.group(1).strip() if title_m else "(no title)"
        title = re.sub(r'\s+', ' ', title)  # 合并连续空白
        # 去 HTML 实体（用 html.unescape 处理所有命名/数字实体）
        import html as _html
        title = _html.unescape(title)

        # 抽 category（<span class="... text-[var(--post-eyebrow)]..."> 内文本）
        cat_m = re.search(r'text-\[var\(--post-eyebrow\)\][^>]*>\s*(.+?)\s*<', block)
        category = cat_m.group(1).strip() if cat_m else None

        # 是否含 bg-tag-new 角标
        is_new_tagged = bool(re.search(r'bg-tag-new[^>]*>\s*new\s*<', block, re.IGNORECASE))

        entries.append({
            "title": title,
            "url": url,
            "category": category,
            "is_new_tagged": is_new_tagged,
        })

        if len(entries) >= limit:
            break

    return entries


def fetch_detail_published(url: str) -> Tuple[Optional[str], Optional[str]]:
    """从 announcement / 文章详情页提取 schema.org datePublished。

    返回：(published_iso, error_str)
    """
    try:
        html = fetch(url, timeout=20)
    except Exception as e:
        return None, f"fetch_failed: {e}"

    # schema.org JSON-LD datePublished（可能出现多次，取第一个非 page-level 的）
    # a16z 的 article 类 schema 与 webpage 类 schema 都有 datePublished，但 article 类是 entry 自身日期
    matches = re.findall(r'"datePublished":\s*"([^"]+)"', html)
    if not matches:
        return None, "no_datePublished_in_html"

    # 取最早出现的——通常是 article 的 datePublished
    # （a16z 页面：Article schema datePublished 在前，Yoast WebPage datePublished 在后）
    published = matches[0]
    return published, None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max", type=int, default=15, dest="max_entries", help="列表页解析前 N 条")
    ap.add_argument("--detail-limit", type=int, default=15, help="详情页拉取前 N 条（≤ max）")
    args = ap.parse_args()

    fetched_at = dt.datetime.now(dt.timezone.utc).isoformat()

    # Step 1: 抓列表页
    try:
        list_html = fetch(LIST_URL)
    except Exception as e:
        print(json.dumps({"error": f"list_fetch_failed: {e}", "url": LIST_URL}, ensure_ascii=False), file=sys.stderr)
        return 1

    entries = parse_list_page(list_html, args.max_entries)

    # Step 2: 串行抓详情页拿 datePublished
    detail_count = min(args.detail_limit, len(entries))
    detail_failed = 0
    for i, e in enumerate(entries[:detail_count]):
        if i > 0:
            time.sleep(DETAIL_RATE_LIMIT_SEC)  # 礼仪间隔
        published, err = fetch_detail_published(e["url"])
        e["published"] = published
        e["published_source"] = "detail_page_schema_org" if published else None
        if err:
            e["detail_error"] = err
            detail_failed += 1

    # 未抓详情的 entries（超出 detail_limit 的）published 留 null
    for e in entries[detail_count:]:
        e["published"] = None
        e["published_source"] = "skipped_detail_fetch"

    out = {
        "source_name": "a16z-news-content",
        "fetched_at": fetched_at,
        "list_url": LIST_URL,
        "entries": entries,
        "stats": {
            "list_parsed": len(entries),
            "detail_fetched": detail_count,
            "detail_failed": detail_failed,
            "new_tagged_count": sum(1 for e in entries if e.get("is_new_tagged")),
        },
    }
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
