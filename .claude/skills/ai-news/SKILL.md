---
description: |
  AI 资讯每日聚合管道。触发：用户输入 /ai-news、或要求"跑一遍 AI 新闻"、"今天 AI 圈发生了什么"、"更新 AInews vault"、"抓取最新论文/AI 动态"。
  并发抓取 references/sources.md 注册的 12 个源（RSS/API/WebFetch 三路）→ 去重过滤 → 主题聚类 → 写入 10-Daily/ 简报 + 50-Zettel/ 原子卡 → 99-Log/ 留运行记录。
  仅在 AInews vault (/Volumes/Projects/AInews) 内有效。
disable-model-invocation: true
allowed-tools: Bash, Read, WebFetch, Agent
argument-hint: "[--date=YYYY-MM-DD] [--dry-run]"
paths: /Volumes/Projects/AInews/**
---

# /ai-news — AI 资讯聚合管道

你正在编排一条 5 阶段的资讯流水线。**你只负责调度，不负责具体抓取/过滤/写盘**——这些都委派给 `.claude/agents/` 里的 6 个 subagent。

## 参数解析

从 `$ARGUMENTS` 解析：
- `--date=YYYY-MM-DD` → 目标日期（默认今天，用 `date +%F` 取本地日）
- `--dry-run` → 只跑 Phase 0，不执行 Fetch/Filter/Cluster/Write

把解析结果记成 `TARGET_DATE` 和 `DRY_RUN` 两个变量，后续 phase 用。

---

## Phase 0 — Preflight（主会话内联，必做）

按顺序执行，任一失败就停下报错并写 Log，不进入 Phase 1。

### 0.1 复验：读 references/

并行 Read：
- `${CLAUDE_SKILL_DIR}/references/sources.md` — 12 个源完整清单
- `${CLAUDE_SKILL_DIR}/references/blacklist.md` — 死源黑名单（确认不抓任何黑名单内源）
- `${CLAUDE_SKILL_DIR}/references/vault-schema.md` — 落盘约定（writer 也会读，主会话先读一遍便于调度）
- `${CLAUDE_SKILL_DIR}/references/filter-criteria.md` — 过滤/聚类标准（filter/cluster 也会读）

### 0.2 源活性 + 时效检查

执行：
```bash
bash ${CLAUDE_SKILL_DIR}/scripts/source-health.sh
```

解析返回的 JSON：
- `alive` → 进入 Phase 1 的源池
- `dead` → 从本次跑剔除，写入 `99-Log/${TARGET_DATE}-source-deadcheck.md`（含 status 码与建议"考虑改 reliability 或移入 blacklist.md"）
- 同时遍历 sources.md 内每个源的 `last_verified`，距 `TARGET_DATE` > 30 天的标 `stale: true`，在 Log 里列出（仍尝试抓取，不剔除）

### 0.3 保护门

若 `alive` 源数 < 3 → 停下问用户"今日仅 N 个源 alive，是否继续"，不要硬抓。

若 `DRY_RUN=true` → 输出一份 Phase 0 简报给用户后**直接退出**，不进入 Phase 1。简报格式：
```
Phase 0 dry-run @ 2026-06-27
- references 全部 readable
- alive: 10 / dead: 2 / stale: 1
- dead 源：[...]
- stale 源：[...]
```

---

## Phase 1 — Fetch（并发）

按每个 alive 源的 `fetch_method` 路由到对应 subagent。**在一条消息内并发起多个 Agent 调用**（同时 spawn，不要串行 await）：

| fetch_method | subagent | 一次调用范围 |
|---|---|---|
| `rss` | `news-fetcher-rss` | 一个源一个 Agent 实例 |
| `api` | `news-fetcher-api` | 一个源一个 Agent 实例 |
| `webfetch` | `news-fetcher-webfetch` | 一个源一个 Agent 实例 |

调用时传入该源的 frontmatter（name / url / notes / fetch_method）作为 prompt 输入，例如：
> "抓取信息源 openai-rss（url=https://openai.com/news/rss.xml, notes=官方一手）。按你的 system prompt 输出 JSON。"

### 软失败处理
- 任一 subagent 返回 `error` 字段非空 → 先标记为 first-fail，进入 retry（见下）
- 60s 内未返回 → 视为超时，标记为 first-fail，进入 retry
- 同一源在最近 2 次**完整跑**（不是单跑内 retry）都失败 → 在 Phase 5 Log 里 append 建议"将该源 reliability 改为 degraded"

### Phase 1 retry 机制

收到所有 Phase 1 输出后，对每个 first-fail 的 source：
- **若 error 字段是 "unknown api source" 或类似不可恢复错误** → 不重试，直接进 failures
- **若是 WebFetch/timeout/parse 类可能偶发的错误** → **重 spawn 一次同类型 subagent**（同 prompt、同 source 描述）
- 同时只对**少量**（≤3 个）first-fail 源做 retry，避免雪崩；超过 3 个失败说明可能是系统性问题（如网络），不 retry 直接进 failures 并在 Phase 5 Log 标"考虑暂停本次跑"
- retry 仍 error → 进入 failures（最终失败）
- retry 成功 → entries 用 retry 结果，在 Phase 5 Log 标"该源首次失败 retry 成功，原因：<retry 前 error>"

注意：**retry 不针对 `entry_count: 0`**（那是源真没新内容，不是失败），仅针对 `error` 字段非空。

### Phase 1 收尾

把所有 subagent 输出合并为 batch 结构，给 Phase 2 准备：
```json
{
  "batch_id": "<TARGET_DATE>-<HH:MM>",
  "fetchers": [
    { "source_name": "openai-rss", "entries": [...] },
    ...
  ],
  "failures": [
    { "source_name": "meta-ai-blog", "error": "..." }
  ]
}
```

---

## Phase 2 — Filter

起 1 个 `news-filter` subagent，把 Phase 1 的 batch JSON 作为输入。

subagent 会先 Read filter-criteria.md，然后输出 `{kept[], discarded[], stats{}}`。直接把 kept 数组带入 Phase 3。

---

## Phase 3 — Cluster

起 1 个 `news-cluster` subagent，输入 Phase 2 的 `kept` 数组 + `batch_id`。

subagent 输出 `{topics[]}`，每个 topic 含 `slug` / `is_new` / `entries[]`（每条标了 `zettel_worthy` 与 `rationale`）。带入 Phase 4。

---

## Phase 4 — Write

起 1 个 `news-writer` subagent，输入 Phase 3 的 `topics` + `target_date=${TARGET_DATE}`。

subagent 会 Read vault-schema.md 后写盘到 `10-Daily/`、`20-Topics/`、`50-Zettel/`，返回 `{daily_path, zettel_paths, topic_paths, topics_created, topics_appended, zettel_count, errors}`。

### Writer 错误处理
- `errors` 非空 → 不阻断，但要在 Phase 5 Log 里完整列出
- 若 `zettel_count == 0` 但 input 有 zettel_worthy 条目 → 异常，报警让用户检查

---

## Phase 5 — Log（主会话内联）

写 `99-Log/${TARGET_DATE}-run.md`：

```markdown
---
created: <ISO 8601 +08:00>
run_duration_seconds: <Phase 0 → Phase 4 总耗时>
sources_attempted: <Phase 0 alive 源数>
sources_alive: <Phase 1 成功源数>
sources_dead: <Phase 0 dead + Phase 1 失败>
entries_fetched: <Phase 1 entries 总数>
entries_after_dedup: <Phase 2 stats.after_dedup>
entries_after_filter: <Phase 2 stats.after_filter>
zettel_written: <Phase 4 zettel_count>
---

# Run @ <TARGET_DATE> <HH:MM>

## 阶段耗时
- Phase 0 Preflight: Xs
- Phase 1 Fetch (concurrent): Xs
- Phase 2 Filter: Xs
- Phase 3 Cluster: Xs
- Phase 4 Write: Xs

## 各源详情
| source | tier | status | entries | note |
|---|---|---|---|---|
| openai-rss | 1 | alive | 5 | — |
| meta-ai-blog | 3 | failed | 0 | timeout |
| ... |

## 产出
- Daily: [[<TARGET_DATE>]]
- 新增 Zettel: <N> 张
- 新增 Topic: <list>
- 追加 Topic: <list>

## 警告 / 建议
- 源 `meta-ai-blog` 已连续 2 次失败，建议将 reliability 改为 degraded
- 源 `xxx` last_verified 已超 30 天，建议手动复验后更新字段
```

---

## 失败兜底

- 任一 Phase 异常死掉 → 立刻写 Phase 5 Log（标 `partial: true`）后报错给用户，**不静默吞掉**
- 不要"为了凑数"伪造条目；宁可在 Daily 里写"今日有效条目过少（N 条），可能上游源批量故障"
- subagent 长时间无响应（> 60s）→ 视为超时，跳过该 subagent 不阻断其他

---

## 调度说明（V2 候选，未实施）

本 skill 是手动触发（`disable-model-invocation: true`）。V2 自动化推荐 Claude Code **Desktop scheduled tasks**：

- 路径：Claude Code Desktop GUI → Scheduled Tasks → New
- prompt：`/ai-news`
- 推荐 cadence：每天 9:03 local（cron `3 9 * * *`；避开整点 jitter）
- ❌ 不用 Cloud Routines：云端 fresh clone，无法访问本地 /Volumes/Projects/AInews vault
- ❌ 不用 `/loop` 长期跑：7 天会自动过期，仅适合调试期连续观察

待手动跑稳后再切换。

---

## 字段引用速查

| 资源 | 路径 |
|---|---|
| 信息源清单 | `${CLAUDE_SKILL_DIR}/references/sources.md` |
| 死源黑名单 | `${CLAUDE_SKILL_DIR}/references/blacklist.md` |
| Vault 落盘协议 | `${CLAUDE_SKILL_DIR}/references/vault-schema.md` |
| 过滤标准 | `${CLAUDE_SKILL_DIR}/references/filter-criteria.md` |
| 源健康检查 | `${CLAUDE_SKILL_DIR}/scripts/source-health.sh` |
| arXiv 抓取 | `${CLAUDE_SKILL_DIR}/scripts/arxiv-fetch.py` |
| 6 个 subagent | `.claude/agents/news-{fetcher-rss,fetcher-api,fetcher-webfetch,filter,cluster,writer}.md` |
