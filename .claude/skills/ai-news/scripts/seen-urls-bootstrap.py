#!/usr/bin/env python3
"""seen-urls-bootstrap.py — 从 vault 现有 60-Originals + 10-Daily/50-Zettel 反推 _seen-urls.json

场景：冷启动（新装环境 / _seen-urls.json 损坏 / 需要重建）时，从 vault 现有
内容反推跨日去重索引，避免 filter Phase 2 首次跑把已存在条目视为「新」
重复入库。

数据流：
1. Glob 60-Originals/*.md（跳过 _assets/）→ 主源，抽 frontmatter：
   source_url / source_name / published_at / title / id / fallback_notice
2. Glob 10-Daily/*.md → 找 [[<original_id>]] 双链 → kept_in_daily
3. Glob 50-Zettel/*.md → 找 [[<original_id>]] 双链 → zettel_id
4. 组装 _seen-urls.json（按 vault-schema §6.4 schema）
5. 应用 --window-days 过滤（超窗的丢）
6. Write JSON

约束：
- 纯 Python 标准库（无第三方依赖）
- 只读 vault，只 Write 一个 _seen-urls.json
- 默认拒绝覆盖已有文件（--force 才覆盖）

使用：
    python3 seen-urls-bootstrap.py \\
      --vault /Volumes/Projects/AInews \\
      --out /Volumes/Projects/AInews/00-Inbox/_seen-urls.json \\
      [--force] \\
      [--window-days 30] \\
      [--target-date YYYY-MM-DD]

exit code:
    0 = 成功
    1 = fatal（out 已存在但未指定 --force / 参数错）

输出（stdout）：JSON 汇总 {urls_written, sources_seen, window_days, ...}
"""

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path


# ============================================================
# frontmatter 解析（简易 YAML，不用 pyyaml）
# ============================================================
def parse_frontmatter(md_content: str) -> dict:
    """从 md 文本抽 YAML frontmatter dict——只支持简单类型：str/int/bool/null/list"""
    m = re.match(r"^---\n(.*?)\n---\n", md_content, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).split("\n"):
        line = line.rstrip()
        m2 = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if not m2:
            continue
        key, val = m2.group(1), m2.group(2).strip()
        if val == "null" or val == "":
            fm[key] = None
        elif val == "true":
            fm[key] = True
        elif val == "false":
            fm[key] = False
        elif val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            if not inner:
                fm[key] = []
            else:
                fm[key] = [x.strip().strip("'\"") for x in inner.split(",") if x.strip()]
        elif val.isdigit():
            fm[key] = int(val)
        else:
            fm[key] = val.strip("'\"")
    return fm


# ============================================================
# vault 扫描
# ============================================================
def collect_originals(vault_path: Path) -> dict:
    """扫 60-Originals/*.md（跳过 _assets 子目录）→ {original_id: frontmatter dict}"""
    originals = {}
    orig_dir = vault_path / "60-Originals"
    if not orig_dir.exists():
        return originals
    for md_path in orig_dir.glob("*.md"):
        if md_path.name.startswith("_"):
            continue
        content = md_path.read_text(encoding="utf-8", errors="replace")
        fm = parse_frontmatter(content)
        original_id = fm.get("id") or md_path.stem
        originals[original_id] = fm
    return originals


def find_backrefs(vault_path: Path, subdir: str, original_ids: set) -> dict:
    """在 subdir 下的 md 里找每个 original_id 被哪些文件引用 [[<id>]]

    返回 {original_id: [refs...]}——refs 是引用它的文件 stem（不含 .md）
    """
    refs = {oid: [] for oid in original_ids}
    dir_path = vault_path / subdir
    if not dir_path.exists():
        return refs
    for md_path in dir_path.glob("*.md"):
        content = md_path.read_text(encoding="utf-8", errors="replace")
        # 一次抽出所有 [[...]] 目标（性能：一次 findall 比循环 for oid + `in` 快）
        wikilinks = set(re.findall(r"\[\[([^\]|#]+)", content))
        for oid in original_ids & wikilinks:
            refs[oid].append(md_path.stem)
    return refs


def parse_date_hhmm_from_id(original_id: str) -> tuple:
    """从 `YYYY-MM-DD-HHMM-<slug>` 抽 (抓取日, HHMM)；解析失败返 ('', '0000')"""
    m = re.match(r"(\d{4}-\d{2}-\d{2})-(\d{4})-", original_id)
    return (m.group(1), m.group(2)) if m else ("", "0000")


# ============================================================
# 构造 _seen-urls.json
# ============================================================
def now_iso() -> str:
    tz = dt.timezone(dt.timedelta(hours=8))
    return dt.datetime.now(tz).replace(microsecond=0).isoformat()


def build_seen_urls(vault_path: Path, window_days: int, target_date: dt.date) -> dict:
    """按 vault-schema §6.4 schema 组装 _seen-urls.json"""
    originals = collect_originals(vault_path)
    original_ids = set(originals.keys())
    daily_refs = find_backrefs(vault_path, "10-Daily", original_ids)
    zettel_refs = find_backrefs(vault_path, "50-Zettel", original_ids)

    cutoff_date = target_date - dt.timedelta(days=window_days)
    urls = {}

    for oid, fm in originals.items():
        source_url = fm.get("source_url")
        if not source_url:
            # 常见于 fallback B 占位文件（url 抓不到）——跳过
            continue

        # first_seen 语义是「何时被本 pipeline 首次抓到」——用 id 里的抓取日/HHMM，
        # 不是 published_at（那是原文发布日，可能远早于抓取日）
        id_date, hhmm = parse_date_hhmm_from_id(oid)
        # id_date 缺失时用 fetched_at 前 10 位兜底
        if not id_date:
            fetched_at = fm.get("fetched_at") or ""
            id_date = fetched_at[:10] if fetched_at else ""

        if not id_date:
            continue

        # 窗口过滤基于抓取日（防 _seen-urls 无限膨胀）
        try:
            first_date = dt.datetime.strptime(id_date, "%Y-%m-%d").date()
            if first_date < cutoff_date:
                continue
        except ValueError:
            pass

        kept_in_daily = daily_refs[oid][0] if daily_refs.get(oid) else ""
        zettel_id = zettel_refs[oid][0] if zettel_refs.get(oid) else None

        # raw_summary_excerpt 用 title 前 200 字近似（filter 真实运行会写更好的）
        excerpt = (fm.get("title") or fm.get("original_title") or "")[:200]

        urls[source_url] = {
            "first_seen_date": id_date,
            "first_seen_run": f"{id_date}-{hhmm}",
            "title": fm.get("original_title") or fm.get("title", ""),
            "source_name": fm.get("source_name") or "unknown",
            "kept_in_daily": kept_in_daily,
            "zettel_id": zettel_id,
            "raw_summary_excerpt": excerpt,
        }

    return {
        "schema_version": "1",
        "last_updated": now_iso(),
        "window_days": window_days,
        "urls": urls,
    }


# ============================================================
# 主流程
# ============================================================
def parse_args():
    p = argparse.ArgumentParser(description="从 vault 现有 60-Originals 反推 _seen-urls.json")
    p.add_argument("--vault", required=True, help="vault 根路径")
    p.add_argument("--out", required=True, help="_seen-urls.json 输出路径")
    p.add_argument("--force", action="store_true", help="覆盖已有 _seen-urls.json")
    p.add_argument("--window-days", type=int, default=30, help="滚动窗口天数（默认 30）")
    p.add_argument("--target-date", help="窗口截断锚点日期 YYYY-MM-DD（默认今天）")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    vault_path = Path(args.vault)
    out_path = Path(args.out)

    if not vault_path.exists():
        print(json.dumps({"error": "vault_not_found", "vault": str(vault_path)}, ensure_ascii=False))
        return 1

    if out_path.exists() and not args.force:
        print(json.dumps({
            "error": "output_exists",
            "hint": "use --force to overwrite",
            "out_path": str(out_path),
        }, ensure_ascii=False))
        return 1

    if args.target_date:
        try:
            target_date = dt.datetime.strptime(args.target_date, "%Y-%m-%d").date()
        except ValueError:
            print(json.dumps({"error": "invalid_target_date", "value": args.target_date}, ensure_ascii=False))
            return 1
    else:
        target_date = dt.date.today()

    result = build_seen_urls(vault_path, args.window_days, target_date)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    sources_seen = len({v["source_name"] for v in result["urls"].values()})
    summary = {
        "urls_written": len(result["urls"]),
        "sources_seen": sources_seen,
        "window_days": args.window_days,
        "target_date": str(target_date),
        "out_path": str(out_path),
    }
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
