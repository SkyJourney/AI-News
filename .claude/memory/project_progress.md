---
name: project_progress
description: AInews 各阶段进度、当前状态、待办——避免重复已完成工作；后续方向以 ROADMAP.md 为权威基准
type: project
last_updated: 2026-07-01
commit: 9b48c6a
---

# AInews 项目进度

> 维护原则：阶段按"功能里程碑"划分，不按时间线流水账。已落地内容写"What + Why"，避免与代码现状脱节。
> **权威基准**：Sprint 1/2/3 待办与执行流水以 `.claude/skills/ai-news/ROADMAP.md` 为准；本文件维护"里程碑历史 + 当前状态快照 + ROADMAP 摘要"。

## 当前状态（2026-07-01）

- **管道版本**：v2.4（IPC Write 中转架构稳定）
- **commit 数**：30+，Base = `9b48c6a`
- **MVP 状态**：✅ **已达成**——2026-06-27 → 2026-07-01 连续 5 天跑通，7-01 跑次 20 Zettel / 9 Topic / 完整 digest
- **调度状态**：✅ **已自动化**——Mac mini 定时任务 + Claude 非交互会话跑通，无需 launchd 独立配置
- **vault 状态**：14 alive 源 + 1 degraded；5 天 Daily/Zettel/Topic/Digest 已写入；Log 完整
- **Sprint 1 全部完成**：F1.1-F1.5 + A4' + F1.6 Phase 3.5 试跑（sampling 11 条真跑：10/11 覆盖率 91% / 6 完美 / 3 openai Fallback B / 1 hf-papers 翻译 bug 现场 / 1 arxiv API stalled 崩溃）+ 4 bug fix（news-originalizer.md Step 4/6/8 + 常见错误清单 + SKILL.md Phase 3.5 retry 机制）全部就绪
- **F1.6 未跑的 Phase 4/5**：writer/digester 编排文档 F1.4 已定型 + F1.2.4 单元测过，为避免覆盖今天真实 20 Zettel/9 Topic 产出未在 F1.6 真跑；下次 /ai-news 正常触发时会自动测
- **60-Originals/ 首批产出**：10 篇 + 89 图（作为 F1 首次真跑证据保留）
- **Sprint 3 · F2.0 完成**（2026-07-01，commit tbd）：**采用 Quartz 5**——三候选 POC 得分 Quartz 38 / Astro 30 / Hugo 26；`web/poc-quartz/` 骨架就绪、`web/poc-astro/` 与 `web/poc-hugo/` 待清理；F2.1-F2.7 因 Quartz 内置省 ~2 天。报告 `.claude/skills/ai-news/notes/F2.0-poc-report.md`
- **F2.0 副产品**：vault 内容 bug `60-Originals/2026-07-01-0901-pessimism-s-paradox-...md` YAML `original_title` 含冒号未加引号已修；news-originalizer.md 需补"含冒号强制引号"约束（Sprint 1 收尾 or Sprint 2）
- **下一步**：Sprint 2 · B1 digester 重构评估 + A9' writer 降级二评估（~2h）；或 Sprint 3 剩余 F2.1-F2.7（~2-3 天，Quartz 内置节省 2 天）

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
- **scripts/test-fetcher.sh**：单源调试入口
- **fetcher 三类全加 `low_confidence` 字段**：下游 filter/cluster/writer 用该字段决策严格度
- **filter-criteria.md §5 Tags 规范**：4 类 tag（技术领域/公司/事件类型/来源 tier），小写 kebab-case

### Stage 6 — 跨日内容串联（commit `8756e50`）
- vault 根 **MOC.md**：动静分离（静态人维护、动态走 Bases）
- writer Daily 加 **"📍 昨日回顾"段**：Glob 昨日 + Read TL;DR，列延续/反差/完成三类跨日链
- frontmatter 加 `previous_daily` 字段

### Stage 7 — 记忆体系规范化（commit `d729cc9`）
- 旧记忆归档到 `_archive/`，按 memory-sync 标准重建 5 件套

### Stage 8 — v2 流程上线（commit `f72e37c`）
- **Phase 5 Digest 集成**：新增 `news-digester` subagent，写 `30-Digests/YYYY-MM-DD.md` 分享版（去 wikilink、URL 展开）
- **00-Inbox 缓存激活**：fetch/filtered/cluster JSON 落盘，支持 `--from-cache` flag 跳过上游 phase
- **40-Deep-Dives 预留**：为未来 weekly/monthly digester 保留目录
- 决策依据见 [[decisions#D12]]

### Stage 9 — v2.1 → v2.4 边界 bug 根治（commit `9e050c2` → `08cffbb`）
- **v2.1** `9e050c2`：IPC 文件契约 + cluster is_new 严格判定 + webfetch 相对日期优先
- **v2.2** `60ddde7`：跨日去重（_seen-urls.json）+ a16z 专项 script fetcher（新增 `news-fetcher-script`）
- **v2.3** `fb92607`：filter/cluster 解决 sonnet 32k 截断——`filter-inline.py` 主会话规则化 + cluster agent 精简 mappings 返回 + `cluster-merge.py` 拼装
- **v2.3** `beeffcd`：cluster agent `sonnet → haiku` + schema 加严
- **v2.4** `08cffbb`：4 个 fetcher subagent 改 Write per-source 中转（`00-Inbox/<date>-<hhmm>-fetch-<source>.json`），根治 3 类边界 bug（token 截断 / 时窗双源 / URL 编码），详见 [[decisions#D13]]

### Stage 10 — MVP 达成 + 调度自动化（commit `5efad3b` → `9b48c6a`）
- **6-27 → 7-01 连续 5 天跑通**：每天 20+ Zettel、6-9 Topic、完整 Digest 与 Log
- **调度**：Mac mini 系统定时任务 + Claude 非交互会话已跑通（**取代**了原 project_progress 里"V2 Desktop scheduled tasks"待办）
- **7-01 跑次**：20 Zettel / 9 Topic / digest（`5efad3b`）
- **ROADMAP 重写**（`d421e60`）：结束"MVP 阶段"，进入 **F1/F2 双主线**——见下节

---

## ROADMAP 摘要（权威见 `.claude/skills/ai-news/ROADMAP.md`）

> 本节是快照，具体任务拆解与状态以 ROADMAP.md 为准；两者变化时**双向同步**（见 [[feedback#F10]]）。

### Sprint 1 · F1 · 60-Originals 全量离线化（~7.5h）
- 加 vault 层 `60-Originals/`，每天抓 10-Daily + 30-Digests 全部条目原文
- haiku 翻译外文 / 中文按模板规整 / 图片三级降级（本地下载 → 描述 → PDF 占位）
- 新增 subagent `news-originalizer` + Phase 3.5 编排
- 10/20/40/50 全链路改双链 `[[60-Originals/<id>]]`
- 任务：F1.1-F1.6 + A4'（cluster 兜底升级）

### Sprint 2 · F1 后评估（~2h）
- B1：digester 输入结构变化后重构评估
- A9'：writer 降级二判（F1 后 writer 责任变小）

### Sprint 3 · F2 · Vault 前端站点（~2-3 天，压缩自 4-5 天）
- Mac mini 本地 docker compose + nginx，端口 40801
- 私有化部署，后续接内网穿透到公网
- **框架 = Quartz 5**（2026-07-01 F2.0 POC 决策，见 [[decisions#D15]]）
- 新增 Phase 7 Publish，skill 跑完自动 rebuild
- 任务：F2.0 ✅ / F2.1-F2.7（含 A7 边角条组件合并、A8 全流程 Log 模板化合并）
- F2.3/F2.4/F2.5 大幅缩水（wikilink/backlinks/graph/search/dark-mode/RSS/OG 全部 Quartz 内置）

### 持续 · 边角优化
- A8'（全流程 Log 模板化，与 F2.6 合并）
- 其他按 ROADMAP.md「合并说明」表消化

---

## 已观测脆弱点（仍需关注）

| 脆弱点 | 状态 | 应对 |
|---|---|---|
| fetcher 主观拒绝外部源 | 已加约束（commit ddda56a + adc4e48） | 新增 fetcher 类型复用同模式 |
| Zettel 同分钟 ID 冲突 | 已加顺延 1 分钟逻辑 | 多次跑同日仍要留意 |
| meta-ai-blog 80+ 天无更新 | 标 `reliability: degraded` | 跟踪是否死透，决定是否入 blacklist |
| arXiv 限流 | scripts/arxiv-fetch.py 内置 3 秒/次 | 不要在主会话直接 curl |
| cluster agent 偶尔漏 mappings | v2.4 有 `agent_missing_urls` 兜底 + F1 时升级为 source 默认表（A4'） | Sprint 1 收尾修 |
| digester 单次 9 分钟 | 输入结构在 F1 后会变，评估延后 | Sprint 2 B1 |

## 相关记忆
- [[project_overview]] — 全局架构与组件职责
- [[decisions]] — 各阶段决策理由（含 D12 v2、D13 v2.4、D14 F1/F2 主线）
- [[feedback#F10]] — progress ↔ ROADMAP 双向同步约定
- [[reference#R9]] — ROADMAP.md 路径指针
