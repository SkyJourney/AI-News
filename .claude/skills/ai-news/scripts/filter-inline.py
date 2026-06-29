#!/usr/bin/env python3
"""
filter-inline.py — Phase 2 主会话内联过滤脚本（v2.3）

规则化跑：
  §1.1 同跑 URL 去重（normalize + tier 偏好）
  §2   信噪过滤（关键词黑名单 + keep signal 覆盖 + low_confidence 兜底）
  §2.5 时效过滤（published 距 target > 14 天 → discard，所有 source 一律）
  §1.5 跨日去重（_seen-urls.json + Jaccard 0.6 豁免 + 30 天窗口清理）

设计原因：v2.1 把 news-filter agent 主输出精简到 stats，但 agent 写 filtered.json
时仍要在脑子里构造大 JSON（89 条 × ~300 字 = 25-30k 字符）触发 sonnet 32k 上限。
v2.3 把整个 filter 改成纯函数式规则脚本，主会话内联跑 < 5 秒。

判断标准的权威仍是 references/filter-criteria.md。本脚本是它的可执行实现，
逻辑修改时两边必须同步（人工 review 时仍以 filter-criteria.md 为准）。

CLI:
  python3 filter-inline.py \\
    --fetch=00-Inbox/2026-06-29-1052-fetch.json \\
    --out=00-Inbox/2026-06-29-1052-filtered.json \\
    --seen-urls=00-Inbox/_seen-urls.json \\
    --target-date=2026-06-29 \\
    --batch-id=2026-06-29-10:52

stdout 输出精简 JSON（filtered_path / seen_urls_path / stats / errors），主会话读 stats。
"""

import argparse
import json
import re
import sys
from datetime import datetime, date
from pathlib import Path


# ============ §1.5 URL normalize ============

def normalize_url(url: str) -> str:
    """对应 filter-criteria.md §1.5 normalize 规则。"""
    if not url:
        return ""
    u = url.lower()
    u = re.sub(r"^https?://", "", u)
    u = re.sub(r"^www\.", "", u)
    u = re.sub(r"[?#].*$", "", u)
    return u.rstrip("/")


# ============ §2 信噪规则 ============

# 默认丢弃模式（每类一组中英正则；命中即 discard，除非有 keep signal 覆盖）
DISCARD_PATTERNS = {
    "funding_pr": [
        r"\braises?\s+\$\s*\d+\s*[kmb]\b",
        r"\b(closes?|completes?)\s+series\s+[a-z]\b",
        r"\bseries\s+[a-z]\s+(round|funding)\b",
        r"\bvaluation\s+(reaches|of|at|hits)\b",
        r"\$\d+\s*(million|billion|m|b)\s+(round|funding|raise)\b",
        r"融资.{0,8}(亿|千万|百万|轮)",
        r"估值.{0,8}(亿|百亿)",
        r"完成.{0,8}轮(融资)?",
    ],
    "hiring": [
        r"\bwe\s*('|’)?\s*re\s+hiring\b",
        r"\bwe\s+are\s+hiring\b",
        r"\bjoin\s+(our|the)\s+team\b",
        r"\bcareers?\s+at\b",
        r"\bopen\s+roles?\b",
        r"招聘|急聘|内推",
    ],
    "event": [
        r"\bregister\s+now\b",
        r"\brsvp\b",
        r"\bconference\s+(announcement|registration)\b",
        r"\bsave\s+the\s+date\b",
        r"报名(参|入会|链接)|参会通知|嘉宾(阵容|邀请)",
    ],
    "ad_sponsor": [
        r"\bsponsored\s+by\b",
        r"\bpromoted\s+post\b",
        r"\b#sponsored\b",
        r"赞助内容|推广文章|商务合作",
    ],
    "vc_softpost": [
        # a16z 等 VC 的投资软文 / IR 公告 / 行业 podcast 类
        r"^\s*investing\s+in\s+\w",
        r"\binvestor\s+relations\b",
        r"\blate\s+stage\s+venture\b",
        r"投资了\b",
    ],
    # 二手编译：太脆弱，先不规则化（容易误丢），靠 cluster 二次判
}

# 强保留信号（hit 任一 → keep，覆盖一切 discard 规则）
KEEP_SIGNALS = [
    r"\barxiv\.org\b",
    r"\bgithub\.com\b",
    r"\bhuggingface\.co\b",
    r"\bbenchmark\b",
    r"\beval(uation)?\s+(score|result)",
    r"\bopen[\s-]?source\b",
    r"\bsota\b|state[\s-]of[\s-]the[\s-]art",
    r"\b(eu\s+ai\s+act|nist|fcc|executive\s+order)\b",
    r"\b(red[\s-]team|alignment|safety|interpretability)\b",
    r"开源|论文|预印本|基准|评测|对齐|可解释性|安全研究",
]


def assess_signal_noise(entry: dict, tier: int) -> tuple:
    """
    返回 (decision, reason, low_confidence)
      decision: 'keep' | 'discard'
      reason  : str | None
      low_confidence: bool
    """
    text = ((entry.get("title") or "") + " " + (entry.get("raw_summary") or "")).lower()

    # 1) keep signal 强保留（覆盖一切丢弃）
    for pat in KEEP_SIGNALS:
        if re.search(pat, text, re.IGNORECASE):
            return ("keep", None, False)

    # 2) 检查 discard 模式
    for category, patterns in DISCARD_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, text, re.IGNORECASE):
                # 融资 PR 的"顶级 VC + $100M + AI 头部"豁免 → low_confidence 留给 cluster
                if category == "funding_pr":
                    return ("keep", None, True)
                return ("discard", f"noise:{category}", False)

    # 3) tier3 + 短摘要 + 无 keep signal → low_confidence 让 cluster 二次判
    summary_len = len(entry.get("raw_summary") or "")
    if tier == 3 and summary_len < 50:
        return ("keep", None, True)

    # 4) 默认保留
    return ("keep", None, False)


# ============ §1.1 同跑 URL 去重 ============

def dedupe_intra(entries: list) -> tuple:
    """
    返回 (kept, discarded)
    同 URL 命中时保留 tier 更低（更一手）的那条，另一条 discarded；
    把被丢条目的 source 收到 kept 条目的 also_reported_by 数组。
    """
    seen: dict = {}  # normalized_url -> entry
    discarded: list = []

    for e in entries:
        nurl = normalize_url(e.get("url", ""))
        if not nurl:
            continue
        if nurl in seen:
            old = seen[nurl]
            old_tier = old.get("_tier", 9)
            new_tier = e.get("_tier", 9)
            if new_tier < old_tier:
                # 新的更一手 → 替换
                discarded.append({
                    "title": old.get("title"),
                    "url": old.get("url"),
                    "source_name": old.get("source_name"),
                    "reason": f"duplicate of {e.get('url')} (tier {new_tier} preferred)",
                })
                arb = list(set(e.get("also_reported_by", []) + [old.get("source_name")]))
                e["also_reported_by"] = sorted(s for s in arb if s)
                seen[nurl] = e
            else:
                discarded.append({
                    "title": e.get("title"),
                    "url": e.get("url"),
                    "source_name": e.get("source_name"),
                    "reason": f"duplicate of {old.get('url')} (tier {old_tier} preferred)",
                })
                arb = list(set(old.get("also_reported_by", []) + [e.get("source_name")]))
                old["also_reported_by"] = sorted(s for s in arb if s)
        else:
            seen[nurl] = e

    return list(seen.values()), discarded


# ============ §1.5 跨日去重 ============

ZH_STOP = set("的了和是在对与也有不将为被把从就都还要这那是个其")
EN_STOP = {
    "the", "a", "an", "of", "to", "in", "and", "is", "for", "on",
    "with", "by", "at", "from", "as", "that", "this", "it", "are",
    "be", "or", "was", "were", "has", "have", "had",
}


def tokenize_for_jaccard(text: str) -> set:
    if not text:
        return set()
    tokens: set = set()
    for w in re.findall(r"[a-zA-Z]+", text.lower()):
        if w not in EN_STOP and len(w) > 1:
            tokens.add(w)
    for ch in re.findall(r"[一-鿿]", text):
        if ch not in ZH_STOP:
            tokens.add(ch)
    return tokens


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def dedupe_cross_day(kept: list, seen_urls: dict, target_date: str) -> tuple:
    """
    返回 (final_kept, cross_day_discarded, re_coverage_count)
    决策表见 filter-criteria.md §1.5。
    """
    lookup = {normalize_url(k): (k, v) for k, v in seen_urls.items()}
    final_kept: list = []
    cross_day_discarded: list = []
    re_cov = 0
    target = date.fromisoformat(target_date)

    for e in kept:
        nurl = normalize_url(e.get("url", ""))
        if nurl not in lookup:
            final_kept.append(e)
            continue
        _, node = lookup[nurl]
        try:
            first_seen = date.fromisoformat(node["first_seen_date"])
        except Exception:
            final_kept.append(e)
            continue
        days = (target - first_seen).days
        if days > 7:
            final_kept.append(e)
            continue
        # ≤ 7 天 → 检查 Jaccard 豁免
        a = tokenize_for_jaccard(e.get("raw_summary"))
        b = tokenize_for_jaccard(node.get("raw_summary_excerpt", ""))
        overlap = jaccard(a, b)
        if overlap <= 0.6 and a and b:
            e["re_coverage"] = True
            e["previously_kept_in_daily"] = node["first_seen_date"]
            re_cov += 1
            final_kept.append(e)
        else:
            cross_day_discarded.append({
                "title": e.get("title"),
                "url": e.get("url"),
                "source_name": e.get("source_name"),
                "reason": f"seen-on-{node['first_seen_date']} (overlap={overlap:.2f})",
            })

    return final_kept, cross_day_discarded, re_cov


# ============ 主流程 ============

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", required=True, help="fetch.json 绝对路径")
    ap.add_argument("--out", required=True, help="filtered.json 绝对路径")
    ap.add_argument("--seen-urls", required=True, help="_seen-urls.json 绝对路径")
    ap.add_argument("--target-date", required=True, help="YYYY-MM-DD")
    ap.add_argument("--batch-id", required=True, help="YYYY-MM-DD-HH:MM")
    args = ap.parse_args()

    fetch_path = Path(args.fetch)
    out_path = Path(args.out)
    seen_path = Path(args.seen_urls)
    target_date = args.target_date
    batch_id = args.batch_id
    run_id = batch_id.replace(":", "")  # 2026-06-29-1052

    errors: list = []

    # 1. Read fetch.json，扁平化 entries 并附加 source_name + _tier
    try:
        fetch = json.loads(fetch_path.read_text(encoding="utf-8"))
    except Exception as ex:
        print(json.dumps({"error": f"failed to read fetch.json: {ex}"}), file=sys.stderr)
        sys.exit(1)

    all_entries: list = []
    for fetcher in fetch.get("fetchers", []):
        src = fetcher.get("source_name")
        tier = fetcher.get("tier", 2)
        for e in fetcher.get("entries", []):
            e["source_name"] = src
            e["_tier"] = tier
            all_entries.append(e)
    input_count = len(all_entries)

    # 2. Read _seen-urls.json（损坏 → 备份后空 schema）
    seen_urls: dict = {}
    if seen_path.exists():
        try:
            seen_data = json.loads(seen_path.read_text(encoding="utf-8"))
            seen_urls = seen_data.get("urls", {})
        except Exception as ex:
            backup = seen_path.with_suffix(
                f".broken-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            )
            try:
                backup.write_bytes(seen_path.read_bytes())
                errors.append(f"seen_urls_corrupted: backed up to {backup.name} ({ex})")
            except Exception:
                errors.append(f"seen_urls_corrupted_and_backup_failed: {ex}")

    # 2.5 窗口清理：删除 > 30 天的节点
    target = date.fromisoformat(target_date)
    pruned = 0
    kept_seen: dict = {}
    for k, v in seen_urls.items():
        try:
            fs = date.fromisoformat(v.get("first_seen_date", "1970-01-01"))
            if (target - fs).days <= 30:
                kept_seen[k] = v
            else:
                pruned += 1
        except Exception:
            kept_seen[k] = v  # 解析不了的节点保守留下
    seen_urls = kept_seen

    # 3. §1.1 同跑去重
    kept_after_intra, intra_discarded = dedupe_intra(all_entries)
    after_intra_dedup = len(kept_after_intra)

    # 4. §2 信噪过滤 + §2.5 时效过滤（published 距 target > 14 天 → discard）
    kept_after_filter: list = []
    noise_discarded: list = []
    stale_discarded = 0
    for e in kept_after_intra:
        # §2.5 时效——优先判（廉价、覆盖广），所有 source 一律 14 天
        pub_str = (e.get("published") or "")[:10]
        try:
            pub_date = date.fromisoformat(pub_str)
            age_days = (target - pub_date).days
            if age_days > 14:
                noise_discarded.append({
                    "title": e.get("title"),
                    "url": e.get("url"),
                    "source_name": e.get("source_name"),
                    "reason": f"stale:{age_days}d_old",
                })
                stale_discarded += 1
                continue
        except Exception:
            # published 解析失败 → 不丢（保守），但记 low_confidence
            e["low_confidence"] = True

        # §2 信噪
        decision, reason, low_conf = assess_signal_noise(e, e.get("_tier", 2))
        if decision == "keep":
            # 不覆盖上面 published 解析失败时已设的 low_confidence=True
            if low_conf:
                e["low_confidence"] = True
            else:
                e.setdefault("low_confidence", False)
            kept_after_filter.append(e)
        else:
            noise_discarded.append({
                "title": e.get("title"),
                "url": e.get("url"),
                "source_name": e.get("source_name"),
                "reason": reason,
            })
    after_filter = len(kept_after_filter)

    # 5. §1.5 跨日去重
    final_kept, cross_discarded, re_cov = dedupe_cross_day(
        kept_after_filter, seen_urls, target_date
    )
    after_cross_day = len(final_kept)

    # 6. 补全 kept 字段 + 清掉内部辅助字段
    for e in final_kept:
        e.setdefault("also_reported_by", [])
        e.setdefault("low_confidence", False)
        e.setdefault("re_coverage", False)
        e.setdefault("previously_kept_in_daily", None)
        title_head = (e.get("title") or "")[:50]
        e["language"] = "zh" if any("一" <= c <= "鿿" for c in title_head) else "en"
        e.pop("_tier", None)  # 内部辅助字段，不写到 filtered.json

    # 7. Write filtered.json
    all_discarded = intra_discarded + noise_discarded + cross_discarded
    output = {
        "batch_id": batch_id,
        "target_date": target_date,
        "kept": final_kept,
        "discarded": all_discarded,
        "stats": {
            "input_count": input_count,
            "after_intra_dedup": after_intra_dedup,
            "after_filter": after_filter,
            "after_cross_day": after_cross_day,
            "discarded_count": len(all_discarded),
            "stale_discarded": stale_discarded,
            "cross_day_discarded": len(cross_discarded),
            "cross_day_re_coverage_kept": re_cov,
            "seen_urls_pruned": pruned,
        },
        "errors": errors,
    }
    try:
        out_path.write_text(
            json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    except Exception as ex:
        print(json.dumps({"error": f"failed to write filtered.json: {ex}"}), file=sys.stderr)
        sys.exit(2)

    # 8. 回写 _seen-urls.json
    for e in final_kept:
        url_orig = e.get("url")
        if not url_orig:
            continue
        if e.get("re_coverage"):
            # 既有 URL → kept_in_daily 数组追加 target_date（不更新 first_seen_date）
            nu = normalize_url(url_orig)
            for k, v in seen_urls.items():
                if normalize_url(k) == nu:
                    arr = v.setdefault("kept_in_daily", [])
                    if target_date not in arr:
                        arr.append(target_date)
                    break
        else:
            # 全新 URL → 创建节点
            seen_urls[url_orig] = {
                "first_seen_date": target_date,
                "first_seen_run": run_id,
                "title": e.get("title", ""),
                "source_name": e.get("source_name", ""),
                "kept_in_daily": [target_date],
                "zettel_id": None,  # writer Phase 4 回填
                "raw_summary_excerpt": (e.get("raw_summary") or "")[:200],
            }

    seen_output = {
        "schema_version": "1",
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "window_days": 30,
        "urls": dict(sorted(seen_urls.items())),
    }
    try:
        seen_path.write_text(
            json.dumps(seen_output, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    except Exception as ex:
        errors.append(f"seen_urls_write_failed: {ex}")

    # 9. stdout 精简 JSON 给主会话
    print(json.dumps({
        "filtered_path": str(out_path),
        "seen_urls_path": str(seen_path),
        "stats": output["stats"],
        "errors": errors,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
