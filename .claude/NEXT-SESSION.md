# /ai-news v2.2 重跑 handoff（2026-06-29）

> 上一会话因 context 满 + 多次重启决定，把所有改动 commit 后切换会话。本文件给下一会话接上下文。
> **任务完成后请删除本文件**（不入 vault 长期记忆）。

---

## 上下文一句话

v2.1 → v2.2 升级**已完成代码改动并 commit**，准备**重跑 6-29 验证**：
1. v2.1：filter/cluster 改文件 IPC 契约 + cluster `is_new` 严格判定 + webfetch Date precedence rules
2. v2.2：跨日去重（`_seen-urls.json` 索引 + 30 天窗口 + URL normalize + Jaccard 0.6 豁免）+ a16z 专项脚本 fetcher

---

## 当前 git 状态

```
最新 commit: <本次 v2.2 commit hash>
分支: main
已 push: 否（重跑成功后再 push）

vault 状态：6-29 已被回退到 v2.1 跑之前
  - 10-Daily/2026-06-29.md          # 已删
  - 30-Digests/2026-06-29-digest.md # 已删
  - 50-Zettel/202606291400-..1403   # 4 张已删
  - 20-Topics/*.md                  # 已 git checkout 到 6-29 之前的版本
  - 20-Topics/opensource-tools.md   # 已删（v2.1 新建的）

inbox：
  - 00-Inbox/2026-06-29-1052-fetch.json   # v2.2 真数据，14 源 89 条
  - 00-Inbox/_seen-urls.json              # 不存在，待重新预填
```

---

## 下一步要做的（按顺序）

### Step A · 预填 `_seen-urls.json` 引导文件

**目标**：扫 6-27 + 6-28 Daily（**不含 6-29**——因为 6-29 已被清空，待重跑生成）抽出 URL 作引导，让本次重跑的跨日去重能命中 6-27/6-28 已记录的条目。

**关键修正**（上一会话踩坑）：上一次预填脚本扫了 6-29 Daily 又"剔除 6-29 节点"——结果**把 anthropic 这种首次出现在 6-28 的 URL 也错标成 first_seen_date=6-29 然后剔了**，导致跨日去重对 anthropic 失效。**这次不要扫 6-29**。

```bash
python3 << 'EOF'
import re, json
from datetime import datetime
from pathlib import Path

VAULT = Path("/Volumes/Projects/AInews")
DAILIES = [VAULT / "10-Daily/2026-06-27.md", VAULT / "10-Daily/2026-06-28.md"]

# 扫 50-Zettel frontmatter 拿 source_url → zettel_id 映射
zettel_index = {}
for zf in (VAULT / "50-Zettel").glob("*.md"):
    text = zf.read_text(encoding="utf-8")
    if not text.startswith("---"): continue
    fm_end = text.find("\n---", 4)
    if fm_end < 0: continue
    fm = text[4:fm_end]
    url_m = re.search(r'^source_url:\s*(\S+)', fm, re.M)
    source_m = re.search(r'^source:\s*(\S+)', fm, re.M)
    if not url_m: continue
    zid = zf.stem.split("-")[0] if zf.stem[:12].isdigit() else zf.stem
    title_m = re.search(r'^title:\s*(.+)$', fm, re.M)
    zettel_index[url_m.group(1).strip()] = {
        "zettel_id": zid,
        "title": title_m.group(1).strip() if title_m else zf.stem,
        "source_name": source_m.group(1).strip() if source_m else "unknown",
    }

# 扫 Daily 抽 [原文](url) 链接
seen = {}
pat = re.compile(r'\[原文\]\((\S+?)\)')
for daily in DAILIES:
    if not daily.exists(): continue
    date_str = daily.stem
    text = daily.read_text(encoding="utf-8")
    for url in pat.findall(text):
        if url not in seen:
            zinfo = zettel_index.get(url, {})
            seen[url] = {
                "first_seen_date": date_str,
                "first_seen_run": f"{date_str}-pre-v22-bootstrap",
                "title": zinfo.get("title", "(from daily, no zettel)"),
                "source_name": zinfo.get("source_name", "unknown"),
                "kept_in_daily": [date_str],
                "zettel_id": zinfo.get("zettel_id"),
                "raw_summary_excerpt": "",
            }
        else:
            if date_str not in seen[url]["kept_in_daily"]:
                seen[url]["kept_in_daily"].append(date_str)

output = {
    "schema_version": "1",
    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "window_days": 30,
    "bootstrap_note": "2026-06-29 v2.2 重跑前引导，扫 6-27/6-28 Daily（**不含 6-29**，因 6-29 待重跑）。raw_summary_excerpt 全空→不触发 Jaccard 豁免→命中的全丢。",
    "urls": dict(sorted(seen.items())),
}
(VAULT / "00-Inbox/_seen-urls.json").write_text(json.dumps(output, ensure_ascii=False, indent=2))
print(f"预填 {len(seen)} 节点；含 zettel_id={sum(1 for v in seen.values() if v['zettel_id'])}")
EOF
```

### Step B · Phase 1（可选——可 from-cache 跳过）

**选择 1**：`--from-cache=2026-06-29-1052-fetch.json` 复用上一会话 v2.2 已抓的 89 条数据（a16z 走了新脚本拿到真日期，HF 8 条新论文都在）

**选择 2**：重新跑 Phase 1（14 源并发，含新 `news-fetcher-script` agent 跑 a16z）。略慢但全新数据，验证 fetcher-script agent 端到端 spawn 是否正常

我推荐**选择 1**，省 5 分钟也避免 a16z 网站可能更新带来的差异。

### Step C · Phase 2 Filter

**关键教训**：上一会话 filter agent 跑了 32 分钟 token 超 32k 截断——根因是调用 prompt 塞了大量"特别注意"细节，agent 走偏没调 Write。

**这次的 prompt 规则**：

```
极简调用 prompt，只 4 行：
- fetch_path: <path>
- out_path: <path>
- seen_urls_path: <path>
- target_date: 2026-06-29 / batch_id: 2026-06-29-XXXX

按 system prompt 9 步执行。第一个工具调用必须是 Read filter-criteria.md，
最后两个工具调用必须是 Write filtered.json 和 Write _seen-urls.json。
返回的 JSON 必须 ≤500 字（不含 kept/discarded 数组）。
```

**预期产出**（基于 1052 fetch.json + 正确预填的 _seen-urls 17 节点）：
- input 89 → 同跑去重 ≈ 86 → §2 信噪 ≈ 46 → §1.5 跨日 ≈ 25-30
- a16z 0 kept（15 条全是 VC 软文/国防/Consumer 评论/14 天外）—— 正常
- HF Daily Papers 8 条全保
- anthropic 应被跨日去重掉 **8-10 条**（如果预填正确，6-28 Daily 含 10 条 anthropic URL）
- qbitai 8 条（新增 6-29 太空算力 + 6-28 抱抱脸/DSpark/前端工程师/OCR + 6-27 GPT-5.6/一人公司/BrowserBC）

### Step D - F · Phase 3 / 4 / 5

照 SKILL.md 编排。Phase 3 cluster 要先 ls 20-Topics/ 注入 existing_topics（注意 `opensource-tools.md` 已删，所以这次又是 `is_new: true` 新建）。

### Step G · Phase 6 / 7

Phase 6 Log 标"v2.2 首次成功跑通"。Phase 7 git 提交所有产出。

---

## 上一会话已修复的具体问题清单（避免重蹈）

| 问题 | 修法 |
|---|---|
| filter agent 输出 32k token 截断 | system prompt 已改文件 IPC；**调用 prompt 必须极简，强制 Write 在前** |
| cluster `is_new` 误判 | SKILL Phase 3 注入 existing_topics 已实现 |
| webfetch agent 误读 a16z 日期为 6 个月前 | a16z 改走 `news-fetcher-script` + `a16z-fetch.py`（脚本拿详情页 datePublished） |
| _seen-urls 预填扫 6-29 导致跨日去重 anthropic 失效 | **这次预填只扫 6-27 + 6-28** |
| URL normalize www / 非 www 不一致 | filter §1.5 已实现 normalize 后匹配 |
| Phase 1 retry 域名安全校验 | 已知偶发，新 fetcher-script 不受影响 |

---

## 关键架构决策回顾

- **方案 A（_seen-urls 索引）** 跨日去重：vs 扫 vault frontmatter / 扫历史 fetch.json
- **方案 Y（Jaccard 0.6 豁免）** 二次报道：vs 一律丢 / 一律保留
- **方案 1（覆盖 + git diff）** 重跑：vs 测试目录 / git revert
- **`fetch_method: script`** 新类型 vs 复用 `api`：a16z 不是 API 而是 HTML 解析，新建更清晰

---

## 跑完后做什么

1. git diff `/private/tmp/claude-501/.../scratchpad/v21-snapshot/` 看 v2.1 daily vs v2.2 daily 差异（v21 snapshot 已备份）
2. git commit "feat(ai-news): v2.2 跨日去重 + a16z script — 重跑 6-29"
3. git push origin main
4. **删除本文件** `.claude/NEXT-SESSION.md`

---

## 风险提示

- `_seen-urls.json` 一旦写错，跨日去重会全乱（要么过度丢、要么完全失效）。预填后**先手工 spot-check** 几条 URL 的 first_seen_date 再跑 filter
- filter agent 仍可能 token 超限——若再次截断，**立即降级**为主会话内联 Python 跑（上一会话已写过原型，可复用）
