---
description: |
  AI 资讯每日聚合管道。触发：用户输入 /ai-news、或要求"跑一遍 AI 新闻"、"今天 AI 圈发生了什么"、"更新 AInews vault"、"抓取最新论文/AI 动态"。
  并发抓取 references/sources.md 注册的 14 个源（RSS/API/WebFetch 三路）→ 去重过滤 → 主题聚类 → 写入 10-Daily/ 简报 + 50-Zettel/ 原子卡 + 30-Digests/ 分享版 → 99-Log/ 留运行记录。
  仅在 AInews vault (/Volumes/Projects/AInews) 内有效。
disable-model-invocation: true
allowed-tools: Bash, Read, WebFetch, Agent
argument-hint: "[--date=YYYY-MM-DD] [--dry-run] [--from-cache=<inbox-file>]"
---

# /ai-news — AI 资讯聚合管道

你正在编排一条 7 阶段的资讯流水线（Phase 0 Preflight + Phase 1-7）。**你只负责调度，不负责具体抓取/过滤/写盘/汇总**——这些都委派给 `.claude/agents/` 里的 7 个 subagent。

## 参数解析

从 `$ARGUMENTS` 解析：
- `--date=YYYY-MM-DD` → 目标日期（默认今天，用 `date +%F` 取本地日）
- `--dry-run` → 只跑 Phase 0，不执行 Fetch/Filter/Cluster/Write/Digest
- `--from-cache=<filename>` → 跳过抓取/中间 phase，按文件后缀路由：
  - `<date>-<hhmm>-fetch.json` → 跳过 Phase 1，从该 fetch 进 Phase 2
  - `<date>-<hhmm>-filtered.json` → 跳过 Phase 1+2，从该 filtered 进 Phase 3
  - `<date>-<hhmm>-cluster.json` → 跳过 Phase 1+2+3，从该 cluster 进 Phase 4+5
  - filename 不含路径前缀，主会话拼接 `00-Inbox/`；HHMM 同跑必须一致（见 vault-schema §2）

把解析结果记成 `TARGET_DATE`、`DRY_RUN`、`FROM_CACHE` 三个变量，后续 phase 用。本次跑的 HHMM 在 Phase 1 落 fetch.json 时锁定到变量 `HHMM`（或 `--from-cache` 从文件名解析），三种 IPC 文件共用同一 HHMM。

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
- 同一源在最近 2 次**完整跑**（不是单跑内 retry）都失败 → 在 Phase 6 Log 里 append 建议"将该源 reliability 改为 degraded"

### Phase 1 retry 机制

收到所有 Phase 1 输出后，对每个 first-fail 的 source：
- **若 error 字段是 "unknown api source" 或类似不可恢复错误** → 不重试，直接进 failures
- **若是 WebFetch/timeout/parse 类可能偶发的错误** → **重 spawn 一次同类型 subagent**（同 prompt、同 source 描述）
- 同时只对**少量**（≤3 个）first-fail 源做 retry，避免雪崩；超过 3 个失败说明可能是系统性问题（如网络），不 retry 直接进 failures 并在 Phase 6 Log 标"考虑暂停本次跑"
- retry 仍 error → 进入 failures（最终失败）
- retry 成功 → entries 用 retry 结果，在 Phase 6 Log 标"该源首次失败 retry 成功，原因：<retry 前 error>"

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

### Phase 1 落盘到 00-Inbox（IPC 起点）

锁定本跑次 HHMM，写一份原始 fetch JSON 到 `00-Inbox/${TARGET_DATE}-${HHMM}-fetch.json`：

```bash
mkdir -p /Volumes/Projects/AInews/00-Inbox
HHMM=$(date +%H%M)
FETCH_PATH="/Volumes/Projects/AInews/00-Inbox/${TARGET_DATE}-${HHMM}-fetch.json"
```

把 batch JSON 序列化 Write 到 `$FETCH_PATH`。这一步：

- **是 Phase 2-5 的 IPC 起点**——下游所有 phase 都从这个文件衍生中间产物（`*-filtered.json`、`*-cluster.json` 共用同一 HHMM）
- Write 失败不阻断 Phase 2（因为 filter 直接读 batch JSON 也行），但要在 Phase 6 Log 报警
- 与同日多次跑不冲突（文件名含 HHMM）
- 配套 `--from-cache=<filename>`：下次跑可指定 fetch/filtered/cluster 中任一文件，从对应 phase 起跑
- **不要清理旧 inbox**——人工决定 retention（vault 是 git 仓库，inbox 文件会被一起追踪，体积失控时手动 archive 或 gitignore）

若 `FROM_CACHE` 不为空 → 按文件后缀路由：
- `*-fetch.json` → 跳过 Phase 1.1-1.4，直接设 `FETCH_PATH=00-Inbox/${FROM_CACHE}`，HHMM 从文件名解析，进 Phase 2
- `*-filtered.json` → 跳过 Phase 1+2，设 `FILTERED_PATH=00-Inbox/${FROM_CACHE}`，进 Phase 3
- `*-cluster.json` → 跳过 Phase 1+2+3，设 `CLUSTER_PATH=00-Inbox/${FROM_CACHE}`，进 Phase 4+5

**所有 from-cache 模式下不再重复落盘**（避免污染缓存层）。

---

## Phase 2 — Filter

预计算 filtered path（HHMM 复用 Phase 1）：

```
FILTERED_PATH=/Volumes/Projects/AInews/00-Inbox/${TARGET_DATE}-${HHMM}-filtered.json
```

起 1 个 `news-filter` subagent，prompt 传：

- `fetch_path`: `$FETCH_PATH`（Phase 1 落盘的 fetch.json）
- `out_path`: `$FILTERED_PATH`
- `target_date`: `$TARGET_DATE`
- `batch_id`: `${TARGET_DATE}-${HH:MM}`

subagent 内部 Read filter-criteria.md + fetch.json → Write filtered.json → 主输出**仅**返回 `{filtered_path, stats, errors}`（不再回完整 kept/discarded 数组，规避 32k token 上限）。

主会话只读 stats 用于 Phase 6 Log；带 `FILTERED_PATH` 进入 Phase 3。

### Filter 错误处理
- `errors` 非空 → 不阻断，但 Phase 6 Log 完整列出
- 若 filtered.json Write 失败 → 检查 `out_path` 父目录可写性；失败重 spawn 一次，仍失败则 abort

---

## Phase 3 — Cluster

预计算 cluster path（HHMM 复用）：

```
CLUSTER_PATH=/Volumes/Projects/AInews/00-Inbox/${TARGET_DATE}-${HHMM}-cluster.json
```

**注入 vault 现状**（修复 cluster 历史上 `is_new` 误判）：

```bash
EXISTING_TOPICS=$(ls /Volumes/Projects/AInews/20-Topics/*.md 2>/dev/null | \
  xargs -n1 basename | sed 's/\.md$//' | grep -v '^agents$' | sort)
```

> `agents.md` 是 vault 内的 AI 行为约定文档，不是 topic 笔记，要排除。其他 `*.md` 都是 cluster 视野内的"已存在 topic"。

把数组化的 EXISTING_TOPICS 作为参数注入 cluster prompt——cluster 严格按"slug 在数组里 → is_new=false；不在 → is_new=true"判定。**不再让 cluster 凭印象推断**。

起 1 个 `news-cluster` subagent，prompt 传：
- `filtered_path`: `$FILTERED_PATH`
- `out_path`: `$CLUSTER_PATH`
- `existing_topics`: `[...]`（上面 ls 拿到的数组）
- `target_date`: `$TARGET_DATE`
- `batch_id`: `${TARGET_DATE}-${HH:MM}`

subagent Read filtered.json + filter-criteria §3 → Write cluster.json → 主输出**仅**返回 `{cluster_path, stats, topics_summary, errors}`（不再回完整 topics 数组）。

主会话读 stats + topics_summary 用于 Phase 6 Log；带 `CLUSTER_PATH` 进入 Phase 4 和 Phase 5（两者并列消费）。

---

## Phase 4 — Write

起 1 个 `news-writer` subagent，prompt 传：

- `cluster_path`: `$CLUSTER_PATH`
- `target_date`: `$TARGET_DATE`

subagent Read cluster.json + vault-schema.md + filter-criteria §5 → 写盘到 `10-Daily/`、`20-Topics/`、`50-Zettel/`，返回 `{daily_path, zettel_paths, topic_paths, topics_created, topics_appended, zettel_count, errors}`。

### Writer 错误处理
- `errors` 非空 → 不阻断，但要在 Phase 6 Log 里完整列出
- 若 `zettel_count == 0` 但 cluster 内有 `zettel_worthy: true` 条目 → 异常，报警让用户检查
- 若 errors 含 `cluster_is_new_mismatch:<slug>` → 在 Phase 6 Log 标"cluster `is_new` 与 vault 现状不一致：<slug>"（虽然 writer 已自动兜底纠正，但仍是 cluster 行为退化信号）

---

## Phase 5 — Digest

起 1 个 `news-digester` subagent，prompt 传：

- `cluster_path`: `$CLUSTER_PATH`（**主输入**，与 writer 同源消费 cluster.json）
- `target_date`: `$TARGET_DATE`
- `zettel_paths`: Phase 4 writer 返回的（可选辅助，取"关键洞察"丰富第 3 句）
- `daily_path`: Phase 4 writer 返回的（可选辅助，仅取 TL;DR 段判断重点）

**关键设计**：digester 与 writer **并列消费同一份 cluster.json**——不是从 writer 渲染的 Daily 二次解析（信息有损）。URL / source_name 等元数据直接从 cluster.json 的 `topics[].entries[]` 字段原样使用。

subagent 写盘到 `30-Digests/<target_date>-digest.md`（去 wikilink、URL 展开的可分享/可打印版本），返回 `{digest_path, items_summarized, zettel_read, topic_count, self_check, errors}`。

### Digester 错误处理
- `errors` 非空 → 不阻断，但要在 Phase 6 Log 里完整列出
- `self_check` 任一字段为 false → 主会话不重试 subagent（digester 内部已做自检），但在 Log 里高亮标"digest 自检失败：<具体项>"提示人工审 30-Digests 产物
- 若 `items_summarized` 显著少于 Phase 2 `entries_after_filter` 数（差距 >20%）→ 主会话报警，可能 digester 漏处理某些 topic

---

## Phase 6 — Log（主会话内联）

写 `99-Log/${TARGET_DATE}-run.md`：

```markdown
---
created: <YYYY-MM-DD HH:mm:ss>
run_duration_seconds: <Phase 0 → Phase 5 总耗时>
sources_attempted: <Phase 0 alive 源数>
sources_alive: <Phase 1 成功源数>
sources_dead: <Phase 0 dead + Phase 1 失败>
entries_fetched: <Phase 1 entries 总数>
entries_after_dedup: <Phase 2 stats.after_dedup>
entries_after_filter: <Phase 2 stats.after_filter>
zettel_written: <Phase 4 zettel_count>
digest_items: <Phase 5 items_summarized>
---

# Run @ <TARGET_DATE> <HH:MM>

## 阶段耗时
- Phase 0 Preflight: Xs
- Phase 1 Fetch (concurrent): Xs
- Phase 2 Filter: Xs
- Phase 3 Cluster: Xs
- Phase 4 Write: Xs
- Phase 5 Digest: Xs

## 各源详情
| source | tier | status | entries | note |
|---|---|---|---|---|
| openai-rss | 1 | alive | 5 | — |
| meta-ai-blog | 3 | failed | 0 | timeout |
| ... |

## 产出
- Daily: [[<TARGET_DATE>]]
- Digest: 30-Digests/<TARGET_DATE>-digest.md（<items_summarized> 条，可分享/打印）
- 新增 Zettel: <N> 张
- 新增 Topic: <list>
- 追加 Topic: <list>

## 警告 / 建议
- 源 `meta-ai-blog` 已连续 2 次失败，建议将 reliability 改为 degraded
- 源 `xxx` last_verified 已超 30 天，建议手动复验后更新字段
- digest 自检失败项：<若 Phase 5 self_check 任一为 false，列出来>
```

---

## Phase 7 — Git Sync（主会话内联）

**前置条件**——以下全部满足才执行：
- Phase 0–5 均无异常抛出
- Phase 4 writer 返回 `errors: []`
- Phase 5 digester 返回 `errors: []`（self_check 单项 false 不阻断，但全 false 视为严重异常需人工审）
- Phase 6 Log 已写盘且 `partial: false`

任一不满足 → 跳过本 phase，在 Log 末尾追加 `git_sync: skipped (reason=...)`，不报错。

### 7.1 校验 remote

```bash
git -C /Volumes/Projects/AInews remote get-url origin
```

- 无 origin → 跳过本 phase，Log 标 `git_sync: skipped (no origin)`
- URL ≠ `git@github.com:SkyJourney/AI-News.git` → 仅警告不擅自改，继续 push（用户可能换了 remote）

### 7.2 add + commit

只 add 本次跑产出的 5 类目录（不动 `.claude/` `SCHEMA.md` `_base-*.base` 等基础设施改动；那些应该由人工 commit）：

```bash
git -C /Volumes/Projects/AInews add \
  "10-Daily/${TARGET_DATE}.md" \
  "20-Topics/" \
  "30-Digests/${TARGET_DATE}-digest.md" \
  "50-Zettel/" \
  "99-Log/${TARGET_DATE}-run.md"
```

检查是否真有 staged 改动（catch-up 情况下可能跑两次同日跑出同一份内容）：

```bash
if git -C /Volumes/Projects/AInews diff --cached --quiet; then
  # 无改动 → 跳过 commit，仍尝试 push（可能上次有未推 commit）
  COMMIT_SHA="(no changes)"
else
  git -C /Volumes/Projects/AInews commit -m "$(cat <<EOF
chore(ai-news): ${TARGET_DATE} 自动跑 — ${ZETTEL_COUNT} 张 Zettel / ${TOPICS_TOTAL} Topic / digest

抓取 ${ENTRIES_FETCHED} → 去重 ${ENTRIES_AFTER_DEDUP} → 过滤后 ${ENTRIES_AFTER_FILTER}
失败源: ${FAILED_SOURCES:-无}
EOF
)"
  COMMIT_SHA=$(git -C /Volumes/Projects/AInews rev-parse --short HEAD)
fi
```

### 7.3 push

```bash
git -C /Volumes/Projects/AInews push origin main 2>&1
```

失败处理（**不重试不强推**）：
- 网络 / 认证错误 → Log 标 `push_failed: <error>`，本地 commit 保留
- `rejected (non-fast-forward)` → Log 标 `push_rejected: pull required`，依赖人工 `git pull --rebase`
- push 成功 → Log 标 `push: success`

### 7.4 在 Phase 6 Log 末尾追加

```markdown
## Git 同步
- commit: <COMMIT_SHA>
- pushed: success | skipped | failed (reason)
- remote: <origin url>
```

---

## 失败兜底

- 任一 Phase 异常死掉 → 立刻写 Phase 6 Log（标 `partial: true`）后报错给用户，**不静默吞掉**；Phase 7 不执行
- 不要"为了凑数"伪造条目；宁可在 Daily 里写"今日有效条目过少（N 条），可能上游源批量故障"
- subagent 长时间无响应（> 60s）→ 视为超时，跳过该 subagent 不阻断其他

---

## 调度配置（Desktop Scheduled Task — 已就绪）

本 skill 由 Claude Code **Desktop Scheduled Tasks** 自动触发，也支持手动 `/ai-news`。

| 字段 | 值 |
|---|---|
| Task ID | `ai-news-daily` |
| Cron | `0 9 * * *`（每天 09:00 本地时间）|
| Folder | `/Volumes/Projects/AInews` |
| Model | `claude-opus-4-7` |
| Permission Mode | `bypassPermissions`（自动化必需，否则会卡权限提示）|
| SKILL.md | `~/Claude/Scheduled/ai-news-daily/SKILL.md` 内容仅 `/ai-news` |
| Jitter | 启用（避开整点拥堵，自动延后几分钟）|

**前置条件**（持续保持）：
- macOS Desktop app 始终开启 + Settings → Desktop app → General 启用 "Keep computer awake"
- vault 目录可写、`git remote get-url origin` 可达（Phase 7 依赖）
- 首次 Run now 时把所有权限选 "always allow" 教 task 学权限

**手动触发模式**：
- `/ai-news` — 跑今天
- `/ai-news --date=YYYY-MM-DD` — 跑指定日期（catch-up / 回填）
- `/ai-news --dry-run` — 仅 Phase 0 健康检查

**不用以下方案**（已评估）：
- ❌ Cloud Routines（云端 fresh clone，无法访问本地 vault；且 fetch 内容写到云端 vault 再回推流程过重）
- ❌ `/loop` 长期跑（7 天会自动过期，仅适合调试期连续观察）
- ❌ launchd / cron + headless CLI（CLI 不原生支持 skill slash command 调用）

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
| 7 个 subagent | `.claude/agents/news-{fetcher-rss,fetcher-api,fetcher-webfetch,filter,cluster,writer,digester}.md` |
