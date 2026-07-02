#!/usr/bin/env python3
"""arxiv-fetch.py — arXiv API 限流抓取，输出 JSON（替代 Atom XML）

约束：
- 严格 3 秒/次限流（arXiv API 礼仪：https://info.arxiv.org/help/api/tou.html）
- 默认抓 cat:cs.AI + cat:cs.LG，sortBy=submittedDate，descending

使用：
    ~/miniconda3/envs/ai-news/bin/python3 arxiv-fetch.py --cats cs.AI cs.LG --max 20 --since-days 1

输出（stdout）：
    {"entries":[{"id","title","authors","summary","published","arxiv_id","pdf_url","abs_url"},...],
     "fetched_at":"...","query":{...}}
"""

import argparse
import datetime as dt
import json
import re
import sys
import time
import urllib.parse
import urllib.request

ARXIV_API = "http://export.arxiv.org/api/query"
RATE_LIMIT_SEC = 3.0
USER_AGENT = "AInews-skill/1.0 (https://github.com/local/ainews)"


def build_query(cats: list[str], max_results: int, since_days: int) -> str:
    search_query = " OR ".join(f"cat:{c}" for c in cats)
    params = {
        "search_query": search_query,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "max_results": str(max_results),
    }
    return f"{ARXIV_API}?{urllib.parse.urlencode(params)}"


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def parse_atom(xml_text: str) -> list[dict]:
    entries: list[dict] = []
    for block in re.findall(r"<entry>(.*?)</entry>", xml_text, re.DOTALL):
        def get(tag: str) -> str:
            m = re.search(rf"<{tag}>(.*?)</{tag}>", block, re.DOTALL)
            return (m.group(1).strip() if m else "")

        entry_id = get("id")
        arxiv_id = entry_id.rsplit("/", 1)[-1].split("v")[0] if entry_id else ""
        authors = [a.strip() for a in re.findall(r"<author>\s*<name>(.*?)</name>", block)]
        pdf_url = ""
        m_pdf = re.search(r'<link[^>]+title="pdf"[^>]+href="([^"]+)"', block)
        if m_pdf:
            pdf_url = m_pdf.group(1)

        entries.append({
            "id": entry_id,
            "arxiv_id": arxiv_id,
            "title": re.sub(r"\s+", " ", get("title")),
            "authors": authors,
            "summary": re.sub(r"\s+", " ", get("summary")),
            "published": get("published"),
            "abs_url": entry_id,
            "pdf_url": pdf_url,
        })
    return entries


def filter_since(entries: list[dict], since_days: int) -> list[dict]:
    if since_days <= 0:
        return entries
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=since_days)
    out = []
    for e in entries:
        try:
            pub = dt.datetime.fromisoformat(e["published"].replace("Z", "+00:00"))
            if pub >= cutoff:
                out.append(e)
        except Exception:
            out.append(e)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cats", nargs="+", default=["cs.AI", "cs.LG"])
    ap.add_argument("--max", type=int, default=20, dest="max_results")
    ap.add_argument("--since-days", type=int, default=1)
    args = ap.parse_args()

    url = build_query(args.cats, args.max_results, args.since_days)

    time.sleep(RATE_LIMIT_SEC)
    try:
        xml = fetch(url)
    except Exception as e:
        print(json.dumps({"error": str(e), "url": url}), file=sys.stderr)
        return 1

    entries = parse_atom(xml)
    entries = filter_since(entries, args.since_days)

    out = {
        "entries": entries,
        "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "query": {
            "cats": args.cats,
            "max": args.max_results,
            "since_days": args.since_days,
        },
    }
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
