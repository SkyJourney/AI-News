---
name: project_progress
description: AInews 各阶段进度、当前状态、待办——避免重复已完成工作
type: project
last_updated: 2026-06-27
commit: d729cc9
---

# AInews 项目进度

> 维护原则：阶段按"功能里程碑"划分，不按时间线流水账。已落地内容写"What + Why"，避免与代码现状脱节。

## 当前状态（2026-06-27）

- **管道版本**：v1（手动触发跑通 2 次，待 V2 调度）
- **commit 数**：12 个，Base = `d729cc9`
- **vault 状态**：14 alive 源 + 1 degraded；首批 Daily/Zettel/Topic 已写入
- **基础设施**：Bases 视图 + 单测脚本 + MOC + 跨日链全部就绪
- **下一步**：跑稳 ≥ 3 天后，启用 Desktop scheduled tasks（V2）

## 已落地阶段

### Stage 1 — Vault 骨架（commit `8b063c0` → `c0ffb2a`）

- 建立 7 层目录 + SCHEMA.md 根公约
- 决定"vault 内不存源元数据"，砍掉 `30-Sources/` 目录
- 信息源登记移交 skill `references/sources.md` 单一权威

### Stage 2 — Skill + 6 subagent（commit `c1b3944`）

- 创建 `/ai-news` skill：5 phase 编排（Preflight → Fetch → Filter → Cluster → Write → Log）
- 6 个原生 subagent 落地：fetcher-{rss,api,webfetch} + filter + cluster + writer
- `disable-model-invocation: true` 锁定仅手动触发
- 起手就过两次完整跑（commit `80355ad` + `4f8ca85`）

### Stage 3 — Pipeline 健壮性（commit `ddda56a` → `adc4e48`）

- fetcher-rss 不再假设 WebFetch 返回 raw XML（修幻觉拒绝）
- fetcher-webfetch 加"不要因外部因素主观拒绝"约束
- Phase 1 first-fail retry 1 次（雪崩保护：> 3 个失败不 retry）
- arXiv 失败时 HF Daily Papers 回退
- 新增投资视角源（a16z / Air Street Press / 量子位 / State of AI）

### Stage 4 — 记忆系统首版（commit `a2984c4`）

- 创建 `.claude/memory/` 体系
- 归档调研快照到 `_archive/`
- 刷新 README + CLAUDE.md，明确入口与索引

### Stage 5 — 工程基础设施（commit `fb0e170`）

- **3 个 Obsidian Bases 视图**：按主题 / 按 source / Daily 时间线+健康监控
- **scripts/test-fetcher.sh**：单源调试入口（修过 bash 3.2 中文紧跟变量名 unbound 坑）
- **fetcher 三类全加 `low_confidence` 字段**：下游 filter/cluster/writer 用该字段决策严格度
- **filter-criteria.md §5 Tags 规范**：4 类 tag（技术领域/公司/事件类型/来源 tier），小写 kebab-case

### Stage 6 — 跨日内容串联（commit `8756e50`）

- vault 根 **MOC.md**：Map of Content 总览入口；动静分离（静态人维护、动态走 Bases）
- writer Daily 加 **"📍 昨日回顾"段**：Glob 昨日 + Read TL;DR，列延续/反差/完成三类跨日链
- frontmatter 加 `previous_daily` 字段，形成时间链

### Stage 7 — 记忆体系规范化（commit `d729cc9` → 当前）

- 旧记忆文件（architecture / vault-cli-facts）归档到 `_archive/snapshot-2026-06-27.md`
- 按 memory-sync skill 标准重建：project_overview / project_progress / decisions / feedback / reference

## 待办（按优先级）

### 高 — 跑稳与调度

1. **连续跑 ≥ 3 天**手动 `/ai-news`，观察：
   - retry 是否真触发、是否成功
   - low_confidence 字段下游决策效果
   - meta-ai-blog degraded 状态是否要升级为 blacklist
2. **V2 调度切换**：Desktop scheduled tasks，每天 9:03 local（cron `3 9 * * *`，避开整点 jitter）
   - ❌ 不走 Cloud Routines（fresh clone 无法访问本地 vault）
   - ❌ 不走 `/loop`（7 天过期，仅调试用）

### 中 — 数据沉淀

3. **跨多日 Log 趋势统计脚本**（待 ≥ 7 天数据后再写）
4. **Zettel 原子化粒度复盘**：按多日使用感受调整 cluster 的 `zettel_worthy` 阈值

### 低 — 探索性

5. **00-Inbox/ 启用**：未消化条目缓冲区，目前 v1 直接走 fetcher → filter 没有 Inbox 中转
6. **40-Deep-Dives/ 与 `deep-research` skill 联动**：人工选题 + AI 协助深挖

## 已观测脆弱点（仍需关注）

| 脆弱点 | 状态 | 应对 |
|---|---|---|
| fetcher 主观拒绝外部源 | 已加约束（commit ddda56a + adc4e48） | 新增 fetcher 类型需复用同模式 |
| Zettel 同分钟 ID 冲突 | 已加顺延 1 分钟逻辑 | 多次跑同日时仍要留意 |
| meta-ai-blog 80+ 天无更新 | 标 `reliability: degraded` | 跟踪是否真的死透，决定移入 blacklist |
| arXiv 限流 | scripts/arxiv-fetch.py 内置 3 秒/次 | 不要在主会话直接 curl |

## 相关记忆

- [[project_overview]] — 全局架构与组件职责
- [[decisions]] — 各阶段决策理由（解释 "为何这样选"）
- [[reference]] — 调试入口与外部资源
