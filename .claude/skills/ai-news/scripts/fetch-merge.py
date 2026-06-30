#!/usr/bin/env python3
"""
fetch-merge.py — Phase 1 主会话辅助脚本（v2.4）

每个 fetcher subagent Write per-source 中转文件到
  00-Inbox/<target-date>-<hhmm>-fetch-<source_name>.json
本脚本扫这些文件，按 sources.md 注入 tier/perspective，合并为总
  00-Inbox/<target-date>-<hhmm>-fetch.json
schema 与 vault-schema §6.1 一致（fetchers[] / failures[] / stats）。

设计原因：v2.3 fetcher subagent 用 assistant 文本回报 JSON，对大数据源
（arxiv 20 条 / the-batch 15 条 / a16z 15 条）触发 LLM 输出 token 上限，
文本只列样本几条 + 文字说明，主会话只能落"看见的"数据。v2.4 复用 cluster v2.3
"agent 出精简返回 + 文件作真实数据传递"模式，让 fetcher Write 完整 JSON 到
中转文件，主会话 Read 文件无大小限制，根治截断 bug（arxiv/the-batch/a16z 历史重灾区）。

CLI:
  python3 fetch-merge.py \\
    --inbox-dir=/Volumes/Projects/AInews/00-Inbox \\
    --target-date=2026-06-30 \\
    --hhmm=0949 \\
    --out=/Volumes/Projects/AInews/00-Inbox/2026-06-30-0949-fetch.json \\
    --sources-md=/Volumes/Projects/AInews/.claude/skills/ai-news/references/sources.md \\
    --expected-sources=openai-rss,deepmind-rss,arxiv-api,...

stdout: 精简 stats JSON 给主会话 Phase 6 Log
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def parse_sources_md(path: Path) -> dict:
    """从 sources.md 抽 name -> {tier, perspective}。

    sources.md 是 markdown 文件，源元数据嵌在 ```yaml ... ``` 围栏内。
    用 regex 抽 ```yaml 块再切 `- name:` 段，stdlib 无 yaml 依赖。
    """
    text = path.read_text(encoding="utf-8")
    yaml_blocks = re.findall(r"```yaml\n(.*?)\n```", text, re.DOTALL)
    if not yaml_blocks:
        return {}
    content = "\n".join(yaml_blocks)
    blocks = re.split(r"^\s*- name:\s*", content, flags=re.MULTILINE)[1:]
    result: dict = {}
    for blk in blocks:
        name_m = re.match(r"(\S+)", blk)
        if not name_m:
            continue
        tier_m = re.search(r"^\s*tier:\s*(\d+)", blk, re.MULTILINE)
        persp_m = re.search(r"^\s*perspective:\s*(\S+)", blk, re.MULTILINE)
        result[name_m.group(1).strip()] = {
            "tier": int(tier_m.group(1)) if tier_m else 0,
            "perspective": persp_m.group(1).strip() if persp_m else "unknown",
        }
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inbox-dir", required=True)
    ap.add_argument("--target-date", required=True)
    ap.add_argument("--hhmm", required=True, help="本跑次 HHMM（与 fetcher Write 的文件名匹配）")
    ap.add_argument("--out", required=True, help="总 fetch.json 绝对路径")
    ap.add_argument("--sources-md", required=True, help="sources.md 路径（抽 tier/perspective）")
    ap.add_argument("--expected-sources", required=True,
                    help="逗号分隔本次预期跑的 source name 列表（Phase 0 alive 输出）")
    args = ap.parse_args()

    inbox = Path(args.inbox_dir)
    sources_meta = parse_sources_md(Path(args.sources_md))
    expected = [s.strip() for s in args.expected_sources.split(",") if s.strip()]

    fetchers: list = []
    failures: list = []
    errors: list = []

    for src in expected:
        per_path = inbox / f"{args.target_date}-{args.hhmm}-fetch-{src}.json"
        if not per_path.exists():
            failures.append({"source_name": src, "error": "per_source_file_missing"})
            errors.append(f"per_source_missing:{src}")
            continue
        try:
            per = json.loads(per_path.read_text(encoding="utf-8"))
        except Exception as ex:
            failures.append({"source_name": src, "error": f"per_source_parse_failed: {ex}"})
            errors.append(f"per_source_parse_failed:{src}")
            continue
        # 检查 fetcher 自报 error（fetcher 抓取失败时仍 Write 文件但带 error 字段）
        if per.get("error"):
            failures.append({"source_name": src, "error": per["error"]})
            continue
        meta = sources_meta.get(src, {"tier": 0, "perspective": "unknown"})
        entries = per.get("entries", [])
        fetchers.append({
            "source_name": src,
            "tier": meta["tier"],
            "perspective": meta["perspective"],
            "entry_count": len(entries),
            "entries": entries,
        })

    sources_with_data = sum(1 for f in fetchers if f["entry_count"] > 0)
    sources_empty = sum(1 for f in fetchers if f["entry_count"] == 0)
    entries_total = sum(f["entry_count"] for f in fetchers)

    batch_id = f"{args.target_date}-{args.hhmm[:2]}:{args.hhmm[2:]}"

    fetch = {
        "batch_id": batch_id,
        "target_date": args.target_date,
        "fetched_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "fetchers": fetchers,
        "failures": failures,
        "retries": [],
        "stats": {
            "sources_attempted": len(expected),
            "sources_with_data": sources_with_data,
            "sources_empty": sources_empty,
            "sources_failed": len(failures),
            "entries_total": entries_total,
            "first_fail_retried": 0,
            "retry_success": 0,
        },
    }

    try:
        Path(args.out).write_text(
            json.dumps(fetch, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    except Exception as ex:
        print(json.dumps({"error": f"failed to write fetch.json: {ex}"}), file=sys.stderr)
        sys.exit(2)

    print(json.dumps({
        "fetch_path": args.out,
        "stats": fetch["stats"],
        "failures": [f["source_name"] for f in failures],
        "errors": errors,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
