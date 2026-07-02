---
name: project_progress
description: AInews 各阶段进度、当前状态、待办——避免重复已完成工作；后续方向以 ROADMAP.md 为权威基准
type: project
last_updated: 2026-07-02
commit: 6bc9411
---

# AInews 项目进度

> 维护原则：阶段按"功能里程碑"划分，不按时间线流水账。已落地内容写"What + Why"，避免与代码现状脱节。
> **权威基准**：Sprint 1/2/3 待办与执行流水以 `.claude/skills/ai-news/ROADMAP.md` 为准；本文件维护"里程碑历史 + 当前状态快照 + ROADMAP 摘要"。

## 当前状态（2026-07-02）

- **管道版本**：v2.4（IPC Write 中转架构稳定）
- **commit 数**：56，Base = `6bc9411`
- **MVP 状态**：✅ **已达成**——2026-06-27 → 2026-07-02 连续 6 天跑通
- **调度状态**：✅ **已自动化**——Mac mini 定时任务 + Claude 非交互会话跑通
- **vault 状态**：14 alive 源 + 1 degraded；6 天 Daily/Zettel/Topic/Digest 已写入；Log 完整
- **Sprint 1 全部完成**：F1.1-F1.6 + A4' + F1 侧 news-writer 情形 E 补齐（复盘/未升级 Zettel 也挂原文双链，见 [[decisions#D16]] 副产品）
- **60-Originals 累计**：60+ 篇 · 图片资产 660+
- **Sprint 3 · F2 重启完成**（2026-07-02，commits `e992215` / `6bea330` / `6d5170f`）：**弃用 Quartz 5 · 迁 Astro 5 自主前端**（见 [[decisions#D16]]）——Quartz vendor 200+ 文件全删，`web/frontend/` 独立 Astro 5 项目上线，83 页 build 805ms，11/11 route 200，LAN `192.168.50.253:8801` 部署。F2.4 Lumina 视觉 tokens（49 CSS 变量 + 8 utility class + shell 组件）全部继承。完成报告 `.claude/skills/ai-news/notes/F2-astro-completion-report.md`；F2.4 P4 决策上下文归档 `.claude/skills/ai-news/notes/_archive/`
- **F2.7 + F2.8 完成**（2026-07-02，commits `412159b` / `a0d5b71` / `3d38682` / `6bc9411`）：本地部署（LAN-only）+ SKILL.md Phase 8 Publish；生产化 6/7 项（wikilink 断链检测 + hover 预览 · 深色模式 · Article Progress · 字体 self-host · Pagefind 全文搜索）逐批 build + Docker + Playwright 实测通过
- **F2.7 部署编排重构**（2026-07-02，commit tbd）：build 阶段判断 Docker 化是过度设计，改本地 `npm run build` + `rsync -a --delete` 到 `/Volumes/Docker/data/ainews/`；compose 文件挪出仓库到 `/Volumes/Docker/compose/ainews/`（与本机其他项目同构），只剩 nginx 一个常驻服务；`web/frontend/Dockerfile` + 仓库内 `docker-compose.yml`/`nginx.conf` 已删除
- **下一步（v2）**：Bases 视图迁移评估是否值得做（4 个 `.base` 文件本质是运营内部视图，非读者站点功能，暂缓）

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

### Stage 11 — F2 前端框架决策反转 · Quartz → Astro + 内容质量优化补丁 + F2.7/F2.8（commit `e992215` → `6bc9411`）
- **F2.0 → F2.4 归档**：F2.0 Quartz 5 POC 决策（见 [[decisions#D15]]）在 F2.4 P4 深度实证阶段被推翻——Quartz 5 架构性 3 层硬约束（renderPage 6-slot 硬编码 + dispatcher pageType.body 硬编码 + config-loader `??` 兜底）导致 override 路径 4500 行 Lumina 组件全废、build 产 216 HTML 大小写重复、trailing-slash 全 404
- **D16 F2 重启 Astro 5**（见 [[decisions#D16]]）：`web/frontend/` 独立项目，Preact islands + Tailwind 4 + 自建 remark-wiki-link + Content Collections + zod schema + backlinks 反向 map
- **Milestone 全通**（40 min 完成）：M0 干净回滚 → M1 项目骨架 → M2 vaultLoader → M3 Design tokens + Shell → M4 5 列表页 → M5 5 详情页 + / landing → M6 全站验证
- **实证结果**：83 页 build 805ms · 11/11 route 200 · LAN `192.168.50.253:8801` 部署
- **视觉资产**：F2.4 Lumina 49 CSS 变量 + 8 utility class + shell 组件全部继承到 `src/styles/tokens.css` 与 `src/components/shell/`
- **Sprint 1 副产品**：F2 build 时暴露 news-writer 情形 E 漏洞（复盘/未升级 Zettel 遗漏原文双链），已修 `.claude/agents/news-writer.md`（commit `6bea330`）
- **协作规范新增**：[[feedback#F11]] 不用 Learning Mode 让用户写代码 · [[feedback#F12]] 不走框架 override 路径（先探清框架 3 类硬约束）
- **F2.4 P4 归档**：`.claude/skills/ai-news/notes/_archive/F2.4-P4-completion-report.md` · `_archive/F2.4-tokens-lumina-to-quartz.md`
- **F2 Astro 完成报告**：`.claude/skills/ai-news/notes/F2-astro-completion-report.md`
- **F2 内容质量优化补丁**（commit `83c20b2`）：originals 图片资产接入 build 修复（`scripts/sync-assets.mjs`）· zettel 瀑布流嵌套 `<a>` 布局撕裂修复 · Zettel/Topic 历史内容批量回填（中文标题 59 篇 + 日期倒序重排 11 篇）· D17 conda 环境固定 · D18 域名级 UA override，详见 [[decisions#D17]] / [[decisions#D18]]
- **F2.7 本地 Docker 部署**（commit `412159b`）：内网穿透明确划出范围，收窄为纯 LAN 部署。首版新增 `web/frontend/Dockerfile` + `web/docker-compose.yml`（builder profile 只读挂载 vault 5 目录 + nginx 常驻）+ `web/nginx.conf`；SKILL.md 新增 **Phase 8 · Publish**（独立于既有 Phase 7 Git Sync，不依赖 push 结果）。本地验证 137 页 build 通过，`localhost:8801` / LAN `192.168.50.253:8801` 全路由 200
- **F2.7 部署编排重构**（commit tbd）：Docker builder 判断为过度设计（build 阶段容器化除环境隔离外无额外收益，却带来镜像 build/run 复杂度），撤销 `web/frontend/Dockerfile` + 仓库内 compose/nginx 配置。改为本地 Node 直接 `npm run build`（本机已有 Node 环境，见 `~/.claude/ENVIRONMENTS.md`）+ `rsync -a --delete` 同步进 `/Volumes/Docker/data/ainews/`；compose 编排搬到 `/Volumes/Docker/compose/ainews/`（与本机 `panwatch`/`fundval-live` 等项目同构的目录约定），只剩 `nginx:alpine` 一个常驻服务，只读挂载该数据目录。更新变成一次 rsync，nginx 容器不再需要因内容更新而重建
- **F2.8 生产化 6/7 项**（3 个独立 commit，逐批 build + Docker + Playwright 实测）：批次1 `a0d5b71` wikilink 断链检测（异步 `await getVaultCache()` 规避 astro.config.mjs 与 content.config.ts 两条 import 链各自独立模块实例的坑）+ hover 预览；批次2 `3d38682` 深色模式（`[data-theme='dark']` 全套 token + FOUC 防护 + document 级事件委托切换按钮）+ Article Progress + 字体 self-host（`@fontsource/*` + `material-symbols`）；批次3 `6bc9411` Pagefind 全文搜索（`createPortal` 挂 body 绕开 Header backdrop-filter 的 fixed 包含块问题，excerpt 高亮不用 `dangerouslySetInnerHTML` 改安全文本节点渲染）。Bases 视图迁移降为 v2 之后再评估

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

### Sprint 3 · F2 · Vault 前端站点（重启后 · 2026-07-02 主线基本收尾）
- **框架 = Astro 5**（2026-07-02 D16 反转 D15，见 [[decisions#D16]]）
- **已完成**（M0-M6 + 内容质量优化补丁 `83c20b2` + F2.7 本地部署 + F2.8 生产化 6/7 项）：`web/frontend/` Astro 5 项目 · Preact islands · Tailwind 4 · vaultLoader + backlinks 反向 map · 5 collection zod schema · Lumina 49 CSS tokens 继承（含深色模式覆盖）· 5 列表页 + 5 详情页 + / landing · LuminaBacklinks 分栏 · originals 图片资产 pipeline · conda 环境固定（D17）· 域名级 UA override（D18）· **F2.7** 本地 `npm run build` + `rsync --delete` 到 `/Volumes/Docker/data/ainews/` + `nginx:alpine`（`/Volumes/Docker/compose/ainews/`，LAN-only）+ SKILL.md Phase 8 Publish · **F2.8** wikilink 断链检测 + hover 预览 · 深色模式 · Article Progress · 字体 self-host · Pagefind 全文搜索 · 137 页 build 通过 · 本地/LAN `8801` 全路由 200
- **待做**：
  - Bases 视图迁移（4 个 `.base` 文件，运营内部视图性质，评估是否值得做）

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
