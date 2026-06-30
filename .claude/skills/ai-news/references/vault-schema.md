# Vault 落盘协议（skill 内部参考）

> 本文件是 `/ai-news` 内 fetcher/cluster/writer subagent 的**自包含落盘约定**——因为 subagent 启动时不读 vault 根的 `SCHEMA.md`，所以这里完整镜像一份。
> 与 vault 根 `/Volumes/Projects/AInews/SCHEMA.md` 同步维护：改一处必须改另一处。

最后同步：2026-06-29

---

## 1. vault 目录用途

| 目录 | `/ai-news` 谁写 | 写什么 |
|---|---|---|
| `00-Inbox/` | 主会话 Phase 1 + news-filter + news-cluster | **Phase 间 IPC 中间产物**：fetch.json / filtered.json / cluster.json，一跑一组。subagent 输出大 JSON 直接 Write 到这里，主会话只传文件路径，规避 subagent 32k token 输出上限 |
| `10-Daily/` | news-writer | 当日简报，一天一文件（含 wikilink，vault 内部档案） |
| `20-Topics/` | news-cluster + news-writer | 主题文件（append 模式） |
| `30-Digests/` | news-digester | 当日分享/打印版（去 wikilink、URL 展开），一天一文件 |
| `40-Deep-Dives/` | (v2 weekly digester 预留) | 预留给 v2 周报/月报；当前不写，等 ≥7 天 30-Digests/ 历史 |
| `50-Zettel/` | news-writer | 原子卡，一题一卡 |
| `90-Archive/` | (不写) | 人工归档 |
| `99-Log/` | 主会话（Phase 6） + Phase 0 死链报告 | 运行日志 |

### Phase 间 IPC 流（v2.1 文件契约）

```
Phase 1 fetcher × N → 合并 batch JSON → 主会话 Write 00-Inbox/<date>-<hhmm>-fetch.json
Phase 2 news-filter   → Read fetch.json → Write 00-Inbox/<date>-<hhmm>-filtered.json → 主输出 {filtered_path, stats}
Phase 3 news-cluster  → Read filtered.json + existing_topics 列表 → Write 00-Inbox/<date>-<hhmm>-cluster.json → 主输出 {cluster_path, stats}
Phase 4 news-writer   → Read cluster.json → 写 10-Daily/20-Topics/50-Zettel → 主输出 {daily_path, zettel_paths, topic_paths, ...}
Phase 5 news-digester → Read cluster.json (+ 可选 zettel/daily) → 写 30-Digests/ → 主输出 {digest_path, ...}
```

- 三种 IPC 文件 HHMM 相同（绑定到同一跑次）
- 失败可人工读 inbox 中间文件 debug
- `--from-cache=<filename>` 模式：filename 可指任意一种（`*-fetch.json` 跳过 Phase 1；`*-filtered.json` 跳过 Phase 1+2；`*-cluster.json` 跳过 Phase 1+2+3）

⚠️ **10-Daily 与 30-Digests 是同一份 cluster 输出的两个渲染视图**——writer 与 digester 并列消费 Phase 3 的 `topics` JSON，互不派生。前者面向 vault 内部 PKM（双链、概念回溯），后者面向外部分享（自包含、可印）。

---

## 2. 文件命名（强约定）

| 类型 | 模式 | 示例 |
|---|---|---|
| Phase 1 Fetch 缓存 | `00-Inbox/YYYY-MM-DD-HHMM-fetch.json` | `00-Inbox/2026-06-29-0816-fetch.json` |
| Phase 2 Filter 中间产物 | `00-Inbox/YYYY-MM-DD-HHMM-filtered.json` | `00-Inbox/2026-06-29-0816-filtered.json` |
| Phase 3 Cluster 中间产物 | `00-Inbox/YYYY-MM-DD-HHMM-cluster.json` | `00-Inbox/2026-06-29-0816-cluster.json` |
| 跨日去重索引 | `00-Inbox/_seen-urls.json`（单例，跨跑维护） | 见 §6.4 |
| Daily 简报 | `10-Daily/YYYY-MM-DD.md` | `10-Daily/2026-06-29.md` |
| Zettel 原子卡 | `50-Zettel/YYYYMMDDHHmm-<slug>.md` | `50-Zettel/202606291430-gpt5-multimodal.md` |
| Topic 主题 | `20-Topics/<slug>.md` | `20-Topics/model-releases.md` |
| Digest 分享版 | `30-Digests/YYYY-MM-DD-digest.md` | `30-Digests/2026-06-29-digest.md` |
| 运行日志 | `99-Log/YYYY-MM-DD-run.md` | `99-Log/2026-06-29-run.md` |
| 死链报告 | `99-Log/YYYY-MM-DD-source-deadcheck.md` | `99-Log/2026-06-29-source-deadcheck.md` |

**HHMM 同跑绑定原则**：同一跑次产生的 `fetch.json / filtered.json / cluster.json` 三个 IPC 文件**必须共用同一 HHMM**——这是 Phase 链跨阶段定位中间产物的唯一锚。主会话 Phase 1 落 fetch.json 时锁定 HHMM，传给后续所有 phase。

**Zettel 时间戳 ID 规则**：`YYYYMMDDHHmm`（12 位，分钟级），用本地时区（Asia/Shanghai）。多张卡同分钟时往后顺延 1 分钟。

**slug 规则**：小写连字符、ASCII、不超过 50 字符；从条目标题取关键词，去掉停用词。

---

## 3. Frontmatter 必填字段

### Daily 简报
```yaml
---
created: 2026-06-27 18:00:00
status: published
entry_count: 12          # 当日纳入条目数
sources_alive: 10        # 成功抓的源数
sources_dead: 2          # 死掉的源数
topics: [model-releases, safety, opensource]
tags: [daily-digest, llm, safety]    # daily-digest + 当日主要技术领域 tag（详见 filter-criteria §5）
previous_daily: 2026-06-26           # 若昨日 Daily 存在则填，便于反向跳转
---
```

### Zettel 原子卡
```yaml
---
created: 2026-06-27 18:00:00
status: draft
source: openai-rss       # 必须是 sources.md 内的 name
source_url: https://openai.com/news/xxx
topic: model-releases    # 引用或创建 20-Topics/<slug>.md
tags: [llm, multimodal]
---
```

### Topic 主题（append 模式，首次创建写 frontmatter，后续 append 不动 frontmatter）
```yaml
---
created: 2026-06-27 18:00:00
updated: 2026-06-27 18:00:00
entry_total: 1           # 累计纳入条目数（每次 append 后 writer 更新）
---
```

### 运行日志
```yaml
---
created: 2026-06-27 18:00:00
run_duration_seconds: 87
sources_attempted: 12
sources_alive: 10
sources_dead: 2
entries_fetched: 47
entries_after_dedup: 38
entries_after_filter: 25
zettel_written: 8
---
```

---

## 4. Wikilink 规范

| 引用 | 写法 | 示例 |
|---|---|---|
| 跨目录引 Zettel | 时间戳 ID（**不用标题**） | `[[202606271430-gpt5-multimodal]]` |
| 引 Topic | slug | `[[model-releases]]` |
| 引 Daily | 日期 | `[[2026-06-27]]` |
| 引 vault 外资源（sources.md 等） | Markdown 链接，不用 wikilink | `[sources.md](.claude/skills/ai-news/references/sources.md)` |

**Daily 简报中典型一段写法**：
```markdown
## 🤖 模型发布

- **GPT-5 多模态版本** ([[202606271430-gpt5-multimodal]])
  来自 [[openai-rss]]，强调 vision-audio 端到端。
  → 详见 [[model-releases]]
```

---

## 5. 落盘前自检清单（每个 writer subagent 必跑）

写文件前自检：
1. 目录正确？（§1）
2. 文件名符合 §2 模式？（特别是 Zettel 时间戳 ID 是 12 位本地时区分钟）
3. frontmatter 字段齐全？（§3 按文件类型）
4. wikilink 用了时间戳 ID 而非标题？（§4）
5. `source:` 字段引用的 name 在 [sources.md](sources.md) 内？
6. Topic 文件首次创建用 Write、后续 append 用 Edit（**绝不重写 Topic 文件**，会丢历史）

任何一项不满足，停下不写，把问题写入 99-Log。

---

## 6. IPC 中间文件 JSON Schema（v2.4）

### 6.1.a `fetch-<source_name>.json`（v2.4 新增 — per-source 中转，Phase 1.1 fetcher Write）

每个 fetcher subagent Write 自己抓取的 per-source 中转文件，schema 与总 fetch.json 内 `fetchers[]` 数组单元一致（**不含** tier/perspective，主会话 fetch-merge 阶段从 sources.md 注入）：

```json
{
  "source_name": "openai-rss",
  "fetched_at": "2026-06-27T18:00:00+08:00",
  "entry_count": 19,
  "entries": [
    { "title": "...", "url": "...", "published": "...", "raw_summary": "...", "low_confidence": false }
  ],
  "error": null
}
```

抓取失败时仍 Write 该文件，`entries: []` + `error: "<reason>"`，让主会话归 failures。

**约定**：
- 文件名锁定 `00-Inbox/<target_date>-<hhmm>-fetch-<source_name>.json`，HHMM 由主会话 Phase 1 开头锁定后传入 fetcher
- 该文件**不入 git**（`.gitignore` 排除 `00-Inbox/*-fetch-*.json`），保留作单源 debug
- 多次 retry 会覆盖同一 path

### 6.1.b `fetch.json`（Phase 1 输出 / Phase 2 输入，由 fetch-merge.py 拼装）

主会话 Phase 1.3 调 `scripts/fetch-merge.py` 扫所有 per-source 中转文件、按 sources.md 注入 tier/perspective、合并为总 fetch.json：

```json
{
  "batch_id": "YYYY-MM-DD-HH:MM",
  "target_date": "YYYY-MM-DD",
  "fetched_at": "ISO 8601 with tz",
  "fetchers": [
    { "source_name": "...", "tier": 1, "perspective": "research", "entry_count": N, "entries": [...] }
  ],
  "failures": [{ "source_name": "...", "error": "..." }],
  "retries": [{ "source_name": "...", "original_error": "...", "retry_status": "success|fail" }],
  "stats": { "sources_attempted": N, "sources_with_data": N, "sources_empty": N, "sources_failed": N, "entries_total": N, "first_fail_retried": N, "retry_success": N }
}
```

**v2.4 设计原因**：v2.3 fetcher subagent 用 assistant 文本回报 entries，触发 LLM 输出 token 上限（arxiv 20 篇 / the-batch 15 条 / a16z 15 条历史重灾区），主会话只能拿到样本几条 + 文字说明，**真实抓取数据反复丢失**。改 per-source Write 中转后无截断（fetcher 文件 IO 无 token 上限），主会话靠 path Read 取真实数据。同时 fetcher 主输出瘦身为 `{output_path, source_name, entry_count, error}` ~150 字符，与 cluster v2.3 范式一致。

### 6.2 `filtered.json`（Phase 2 输出 / Phase 3 输入）

```json
{
  "batch_id": "YYYY-MM-DD-HH:MM",
  "target_date": "YYYY-MM-DD",
  "kept": [
    { "title": "...", "url": "...", "published": "...", "raw_summary": "...", "source_name": "...", "low_confidence": false, "also_reported_by": ["..."], "language": "en|zh" }
  ],
  "discarded": [
    { "title": "...", "url": "...", "source_name": "...", "reason": "..." }
  ],
  "stats": { "input_count": N, "after_dedup": N, "after_filter": N, "discarded_count": N }
}
```

### 6.3 `cluster.json`（Phase 3 输出 / Phase 4+5 输入）

```json
{
  "batch_id": "YYYY-MM-DD-HH:MM",
  "target_date": "YYYY-MM-DD",
  "existing_topics_snapshot": ["model-releases", "..."],  // 主会话注入的 vault 现状快照
  "topics": [
    {
      "slug": "model-releases",
      "is_new": false,
      "entry_count": N,
      "entries": [
        { "title": "...", "url": "...", "source_name": "...", "published": "...", "raw_summary": "...", "low_confidence": false, "also_reported_by": [...], "zettel_worthy": true, "rationale": "..." }
      ]
    }
  ],
  "stats": { "input_count": N, "topic_count": N, "new_topic_count": N, "zettel_worthy_count": N }
}
```

**契约关键点**：
- 三种文件**保留完整字段**（不裁剪），下游 phase 直接消费，无需主会话回填
- `existing_topics_snapshot` 由主会话在 Phase 3 起 cluster 前注入（`ls 20-Topics/*.md`），cluster 用它判定 `is_new = !snapshot.includes(slug)`
- subagent Write 后**只**返回 `{filtered_path|cluster_path, stats, errors}` 三件套，主会话不再传 JSON 内容

### 6.4 `_seen-urls.json`（跨日去重索引，单例 / 跨跑维护）

由 news-filter Phase 2 读 + 写，news-writer Phase 4 完成后回填 `zettel_id` / `daily_date`。**滚动窗口 30 天**——超出窗口的 URL 在 filter 读入时清理（删除节点），防文件膨胀。

```json
{
  "schema_version": "1",
  "last_updated": "2026-06-29 14:00:00",
  "window_days": 30,
  "urls": {
    "https://openai.com/index/previewing-gpt-5-6-sol": {
      "first_seen_date": "2026-06-27",
      "first_seen_run": "2026-06-27-1530",
      "title": "Previewing GPT-5.6 Sol",
      "source_name": "openai-rss",
      "kept_in_daily": "2026-06-27",
      "zettel_id": "202606271430-gpt5-6-sol",
      "raw_summary_excerpt": "OpenAI previews GPT-5.6 Sol, a next-generation model with stronger capabilities in coding, science, and cybersecurity..."
    }
  }
}
```

**字段说明**：

| 字段 | 由谁写 | 用途 |
|---|---|---|
| `first_seen_date` / `first_seen_run` | filter（首次进 kept 时） | 距 target_date 比较，超 7 天则不再视为重复 |
| `title` / `source_name` | filter | 跨日 debug 时辨识 |
| `kept_in_daily` | filter | 标记"这条曾被某天 Daily 收录"——用于 writer 在新 Daily 写"延续主题"时反查 |
| `zettel_id` | writer（Phase 4 完成回填） | 写新 Daily 时可直接 wikilink 旧 Zettel |
| `raw_summary_excerpt` | filter | 前 200 字截断，方案 Y 词汇重叠豁免比对用 |

**filter 的跨日去重决策表**（详见 `filter-criteria.md §1.5`）：

| 命中 _seen-urls 的 URL | 距今天数 | 决策 |
|---|---|---|
| 同一 URL 完全相同 | ≤ 7 天 | 默认 `discarded`，reason: `seen-on-<first_seen_date>` |
| 同一 URL 完全相同 | ≤ 7 天 + 词汇重叠 ≤ 0.6 | **保留**并标 `language` 或 `re_coverage: true`（方案 Y 豁免） |
| 同一 URL 完全相同 | > 7 天 | 视为新条目正常入 kept |
| 同事件不同 URL（标题 ≥ 0.85 相似） | ≤ 7 天 | 同 URL 一致：默认丢，词汇重叠 ≤ 0.6 触发豁免保留 |

**重要约束**：
- `_seen-urls.json` 是 vault 共享状态，**绝不能**被 cluster / writer / digester 写入（避免竞态）；只允许 filter（读写）+ writer Phase 4 回填 `zettel_id` 字段
- writer 回填 `zettel_id` 时用 Edit 精确替换该 URL 对应节点的 `zettel_id` 字段，不整体覆盖文件
- 若文件不存在（首次跑或被人工删除）→ filter 自动创建空 schema 后继续
