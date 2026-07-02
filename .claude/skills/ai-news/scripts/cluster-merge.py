#!/usr/bin/env python3
"""
cluster-merge.py — Phase 3 主会话辅助脚本（v2.3）

news-cluster agent 输出精简 mappings 数组（每条 url + topic_slug + is_new
+ zettel_worthy + rationale），本脚本用 mappings + filtered.json 的 kept 字段
合成完整 cluster.json（schema 见 vault-schema §6.3）。

设计原因：v2.1/v2.2 cluster agent 要在脑子里构造完整 cluster.json（含 38 条 entries
全部字段 + zettel_worthy/rationale）≈ 23K 字符，加思考链接近 sonnet 32k 上限。
v2.3 把 agent 工作瘦身为"判断 + 解释"（不到 5K 输出），主会话内联 merge 字段。

CLI:
  ~/miniconda3/envs/ai-news/bin/python3 cluster-merge.py \\
    --filtered=00-Inbox/2026-06-29-1052-filtered.json \\
    --out=00-Inbox/2026-06-29-1052-cluster.json \\
    --target-date=2026-06-29 \\
    --batch-id=2026-06-29-10:52 \\
    --existing-topics=model-releases,safety-alignment,... \\
    --mappings-stdin

stdin: agent 输出的精简 JSON
  {"mappings": [{url, topic_slug, is_new, zettel_worthy, rationale}, ...],
   "errors": [...]}

stdout: 精简 cluster stats JSON 给主会话 Phase 6 Log
"""

import argparse
import html
import json
import sys
from collections import OrderedDict
from pathlib import Path


# A4': 按 source_name 查默认 topic 兜底表——依据 sources.md 里 14 个源的性质。
# 使用场景：cluster agent 漏 mappings 时，主会话按 source 分配合理的默认 topic，
# 而不是全部塞进 'applications'——F1 后所有 kept 条目都要绑 topic 才能有效双链。
# 未列的 source 走 'applications' fallback（保底不丢数据）。
SOURCE_DEFAULT_TOPIC = {
    # Tier 1 主力（模型/产品发布）
    "openai-rss": "model-releases",
    "anthropic-news": "model-releases",
    "deepmind-rss": "model-releases",
    "meta-ai-blog": "model-releases",
    # 学术源（论文）
    "arxiv-api": "research-papers",
    "huggingface-daily-papers": "research-papers",
    "state-of-ai": "research-papers",       # 年度综述/报告归学术层
    # 分析类 / 行业动态
    "import-ai": "industry-moves",
    "interconnects": "industry-moves",
    "the-batch": "industry-moves",
    # 中文行业
    "qbitai": "industry-moves",
    "jiqizhixin": "industry-moves",
    # 投资视角
    "air-street-press": "funding-investment",
    "a16z-news-content": "funding-investment",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--filtered", required=True, help="filtered.json 绝对路径")
    ap.add_argument("--out", required=True, help="cluster.json 绝对路径")
    ap.add_argument("--target-date", required=True)
    ap.add_argument("--batch-id", required=True)
    ap.add_argument("--existing-topics", required=True,
                    help="逗号分隔 slug 列表，cluster agent 拿到的同一份")
    ap.add_argument("--mappings-stdin", action="store_true",
                    help="从 stdin 读 agent 输出 JSON（必传）")
    args = ap.parse_args()

    errors: list = []

    # 1. Read filtered.json kept
    try:
        filtered = json.loads(Path(args.filtered).read_text(encoding="utf-8"))
        kept = filtered.get("kept", [])
    except Exception as ex:
        print(json.dumps({"error": f"failed to read filtered.json: {ex}"}), file=sys.stderr)
        sys.exit(1)

    # 2. Read agent mappings from stdin
    try:
        agent_out = json.loads(sys.stdin.read())
    except Exception as ex:
        print(json.dumps({"error": f"failed to parse agent stdin: {ex}"}), file=sys.stderr)
        sys.exit(1)

    mappings = agent_out.get("mappings", [])
    errors.extend(agent_out.get("errors", []))

    # 3. Build url → entry lookup（filtered.json 唯一权威，agent 不允许自造 entries）
    url_to_entry = {e["url"]: e for e in kept if e.get("url")}

    # 4. 字段兼容：agent 偶尔返回 slug 代替 topic_slug，统一吸收
    for m in mappings:
        if "topic_slug" not in m and "slug" in m:
            m["topic_slug"] = m.pop("slug")

    # 4.5. URL HTML 实体反转义（v2.4，防御 agent 偶尔把 & 误写成 &amp; / &#39; 等，
    #      污染 cluster.json 后导致 writer 查 _seen-urls 匹配不上 → seen_urls_missing_url）
    for m in mappings:
        if m.get("url"):
            m["url"] = html.unescape(m["url"])

    # 5. 校验：mappings 中的 url 都该在 filtered.json kept 里
    unknown_urls = [m["url"] for m in mappings if m.get("url") not in url_to_entry]
    if unknown_urls:
        errors.append(f"agent_unknown_urls:{len(unknown_urls)}_count")

    # 5. 校验：filtered.json kept 应该全部被映射（不允许 agent 漏条目）
    mapped_urls = {m["url"] for m in mappings if m.get("url")}
    missing_urls = [u for u in url_to_entry if u not in mapped_urls]
    if missing_urls:
        errors.append(f"agent_missing_urls:{len(missing_urls)}_count")
        # A4': 按 source_name 查默认 topic 兜底表，未列走 applications fallback
        # F1 后所有 kept 条目都要绑 topic 才能有效双链，兜底重要性提升到 P-中
        for u in missing_urls:
            entry = url_to_entry[u]
            source_name = entry.get("source_name") or ""
            default_topic = SOURCE_DEFAULT_TOPIC.get(source_name, "applications")
            mappings.append({
                "url": u,
                "topic_slug": default_topic,
                "is_new": False,
                "zettel_worthy": False,
                "rationale": f"(auto-assigned by cluster-merge: agent missed; source={source_name} → {default_topic})",
            })

    # 6. existing_topics 校验 is_new（兜底纠正 agent 错判）
    existing = set(s.strip() for s in args.existing_topics.split(",") if s.strip())
    mismatched_slugs: set = set()
    for m in mappings:
        slug = m.get("topic_slug")
        if not slug:
            continue
        correct_is_new = slug not in existing
        agent_is_new = m.get("is_new")
        if agent_is_new is None:
            # agent 漏字段——静默兜底，不报 errors
            m["is_new"] = correct_is_new
        elif agent_is_new != correct_is_new:
            # agent 给了值但错——记 errors（按 slug 去重）
            mismatched_slugs.add(slug)
            m["is_new"] = correct_is_new
    for slug in sorted(mismatched_slugs):
        errors.append(f"cluster_is_new_mismatch:{slug}")

    # 7. 按 topic_slug 分组 entries（OrderedDict 保 topic 首次出现序）
    topics: "OrderedDict[str, dict]" = OrderedDict()
    for m in mappings:
        slug = m.get("topic_slug")
        url = m.get("url")
        if not slug or url not in url_to_entry:
            continue
        entry = dict(url_to_entry[url])  # copy
        entry["zettel_worthy"] = bool(m.get("zettel_worthy", False))
        entry["rationale"] = (m.get("rationale") or "")[:200]
        if slug not in topics:
            topics[slug] = {
                "slug": slug,
                "is_new": bool(m.get("is_new", slug not in existing)),
                "entries": [],
            }
        topics[slug]["entries"].append(entry)

    # 8. 计算 entry_count + 整理 topics 数组
    topics_list = []
    for slug, t in topics.items():
        t["entry_count"] = len(t["entries"])
        topics_list.append(t)

    # 9. Build cluster.json
    stats = {
        "input_count": len(kept),
        "topic_count": len(topics_list),
        "new_topic_count": sum(1 for t in topics_list if t["is_new"]),
        "zettel_worthy_count": sum(1 for t in topics_list for e in t["entries"]
                                   if e.get("zettel_worthy")),
    }
    cluster = {
        "batch_id": args.batch_id,
        "target_date": args.target_date,
        "existing_topics_snapshot": sorted(existing),
        "topics": topics_list,
        "stats": stats,
        "errors": errors,
    }
    try:
        Path(args.out).write_text(
            json.dumps(cluster, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    except Exception as ex:
        print(json.dumps({"error": f"failed to write cluster.json: {ex}"}), file=sys.stderr)
        sys.exit(2)

    # 10. stdout 精简 stats 给主会话
    topics_summary = [
        {
            "slug": t["slug"],
            "is_new": t["is_new"],
            "entry_count": t["entry_count"],
            "zettel_worthy": sum(1 for e in t["entries"] if e.get("zettel_worthy")),
        }
        for t in topics_list
    ]
    print(json.dumps({
        "cluster_path": args.out,
        "stats": stats,
        "topics_summary": topics_summary,
        "errors": errors,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
