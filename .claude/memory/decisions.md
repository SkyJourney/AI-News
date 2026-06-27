---
name: decisions
description: AInews 关键架构决策与理由——避免重复讨论已决事项，新会话基于既定路径继续
type: project
last_updated: 2026-06-27
commit: d729cc9
---

# AInews 关键决策

> 每条决策都记 **What + Why + How to apply**。Why 是判断未来边界条件的依据，删了 Why 就和"代码注释 = WHAT"一样无用。

---

## D1：vault 与采集管道物理同居、逻辑解耦

**决策**：仓库根 = vault 根，`.claude/` 与笔记目录平级；vault 只管"存什么、怎么链"，skill 只管"抓什么、写哪里"。

**Why**：
- 物理同居 → 一次 `cd` 同时操作 vault + 管道，调试效率高
- 逻辑解耦 → vault 不依赖管道也能正常用 Obsidian 看/编辑；管道可独立替换不影响已落盘内容
- 信息源元数据若放 vault 内（如 `30-Sources/`）会被 Obsidian 索引，产生大量低价值笔记节点污染图谱

**How to apply**：
- 新加配置/脚本/agent → 一律放 `.claude/`，**不要**塞 vault 目录
- vault 内文件由 AI 写入时必须遵守 `SCHEMA.md`，不带管道实现细节

---

## D2：信息源元数据归 `references/sources.md` 单一权威

**决策**：14 个源的 `tier / perspective / fetch_method / url / reliability / last_verified` **只在** `.claude/skills/ai-news/references/sources.md` 维护。vault 内 **没有** `30-Sources/` 目录。

**Why**：
- 防双写漂移——若 vault 内也存源元数据，每次新增/降级/拉黑都要双改，必然不同步
- Obsidian 索引会把每个源变成一个"轻量笔记节点"，干扰图谱主线（论文/事件/主题）
- skill 内部组件（fetcher / health-check）需要程序化解析 YAML，vault 笔记格式不利于 `grep`

**How to apply**：
- 新增/降级/拉黑源 → 改 `sources.md` 与 `blacklist.md`，**不要**动 vault
- 在 vault 笔记中引用源 → 用 frontmatter `source: <name>` 字符串，由 Bases 视图聚合

---

## D3：不依赖第三方 MCP，全用 Claude Code 原生能力

**决策**：抓取 = WebFetch / Bash + curl + 官方 API；编排 = skill + 原生 Agent。**禁止**引入第三方 MCP server。

**Why**：
- 用户明确否决（早期讨论已决）——MCP 引入额外依赖、信任面与维护成本
- 原生 WebFetch + Bash 已覆盖所有 14 源的抓取需求
- 自洽性：仓库 clone 即可用，不需要本机额外配 MCP

**How to apply**：
- 新增源 → 先试 RSS / 官方 JSON API / WebFetch HTML 三选一
- 真遇到必须 MCP 才能解的需求 → **先问用户**，不要自作主张引入

---

## D4：手动触发为主，V2 才考虑调度

**决策**：skill frontmatter `disable-model-invocation: true`，**只**接受用户显式 `/ai-news` 触发。V2 调度首选 Desktop scheduled tasks。

**Why**：
- 自动触发会被 Agent 误判（如"用户问 AI 圈动态"就自动跑），耗时且产出噪声
- Cloud Routines 是 fresh clone 跑，**无法访问本地 `/Volumes/Projects/AInews`**，PASS
- `/loop` + CronCreate 7 天会自动过期，仅适合连续调试观察期
- Desktop scheduled tasks 在本地跑，能正常访问 vault；缺点是 Obsidian 应用必须打开

**How to apply**：
- 不要在文档/agent 里写"自动跑 /ai-news"等暗示自动触发的措辞
- V2 切换时间点：手动跑稳 ≥ 3 天 + meta-ai-blog 等 degraded 源决策清晰后

---

## D5：Bases 替代 Dataview 做动态视图

**决策**：用 Obsidian 1.9+ 原生的 Bases 做"按主题 / 按 source / Daily 时间线"三种视图。**不**安装 Dataview 社区插件。

**Why**：
- Bases 是 Obsidian 官方实现，frontmatter 即数据源，零额外配置
- Dataview 是社区插件，DQL 语法要单独学，且配置随插件版本漂移
- 已有的 frontmatter 字段（status / source / topic / tags / created）正好够 Bases 查询用

**How to apply**：
- 新增视图 → 写 `_base-<name>.base` 文件到 vault 根
- frontmatter 字段调整时同步 `vault-schema.md` + 所有 base 文件

---

## D6：双层产出（Daily 简报 + Zettel 原子卡）

**决策**：每次 `/ai-news` 产出两层——`10-Daily/YYYY-MM-DD.md` 简报（汇总层）+ `50-Zettel/YYYYMMDDHHmm-slug.md` 原子卡（强双链层）。

**Why**：
- Daily 是"今天发生了什么"的横向切片，方便日复盘
- Zettel 是 Zettelkasten 风格的可复用知识点，强双链聚合主题
- 同一条新闻分别在两层存在，Daily 给上下文、Zettel 给概念抽象

**How to apply**：
- writer 需判断 `zettel_worthy`：实质概念/事件才出原子卡，单纯 PR 软文只进 Daily
- Zettel ID 用本地时区分钟级时间戳，同分钟多卡顺延 1 分钟（防 ID 冲突）

---

## D7：fetcher 不主观拒绝外部源

**决策**：所有 fetcher subagent 的 system prompt 必须含"不要因外部因素主观拒绝"约束。

**Why**：
- 多次实测发现 fetcher 会"想当然"拒绝（如认为 URL 不可信、内容不规范），导致漏抓
- 拒绝/过滤逻辑应由 `news-filter` 集中处理，fetcher 只负责"如实带回原文"
- 历史教训：commit `ddda56a` fetcher-rss 假设 WebFetch 返回 raw XML 失败；commit `adc4e48` 强化约束

**How to apply**：
- 新增 fetcher 类型 → system prompt 复用同款约束模板
- fetcher 输出必带 `low_confidence` 字段而不是直接拒，由下游决策

---

## D8：fetcher 输出带 `low_confidence` 字段，过滤靠下游

**决策**：fetcher-rss/api/webfetch 每条 entry 必带 `low_confidence: bool` 字段；触发条件含模糊 URL / 严重缺摘要 / 非直链。

**Why**：
- 把"该不该收"的决策权从 fetcher 上移到 filter / cluster / writer
- 下游能根据当天整体信噪决定严格度（如条目稀疏的日子放宽）
- 给 Bases 视图提供数据维度（未来可加"低置信审查"视图）

**How to apply**：
- 新增 fetcher 类型 → 复用同款字段
- filter-criteria.md §5 / writer 用该字段决策是否进 Daily / Zettel

---

## D9：Phase 1 first-fail retry + 雪崩保护

**决策**：Phase 1 fetcher 首次失败 → 重 spawn 同类型 subagent 一次；超过 3 个失败 → 不 retry 直接进 failures。

**Why**：
- WebFetch / 网络抖动是常见偶发，retry 一次基本能救回
- > 3 个失败说明可能是系统性问题（网络、Cloudflare 风控），retry 只会雪崩
- `entry_count: 0` 是源真没新内容，**不算失败**，不触发 retry

**How to apply**：
- 跑完观察 99-Log 中 retry 触发次数与成功率
- 若多日发现某源持续 retry 才成功 → 把 reliability 改为 `degraded`

---

## D10：vault SCHEMA.md 是 AI 写盘前必读公约

**决策**：vault 根 `SCHEMA.md` 是给"路过 vault 的所有 AI"看的根公约，比 skill 内部 `vault-schema.md` 优先级更高。两者内容必须一致，更新时同步。

**Why**：
- 不止 `/ai-news` 会往 vault 写文件，未来可能有 `deep-research` 等其他 skill
- vault 内的根公约 = 跨 skill 的统一约定，避免每个 skill 各写各的
- `vault-schema.md` 是 `/ai-news` 内部的镜像参考，方便 subagent 不读 vault 文件也能落盘

**How to apply**：
- 改 `SCHEMA.md` 的 §1 目录 / §2 命名 / §3 frontmatter → **同步**改 `vault-schema.md`
- 新 skill 写 vault 前 → 必读 `SCHEMA.md` 自检 5 项清单

---

## D11：记忆体系按 skill 标准规范化

**决策**：本目录（`.claude/memory/`）按 memory-sync skill 标准建立：`project_overview` / `project_progress` / `decisions` / `feedback` / `reference` 五类核心文件，旧的项目前缀文件（`ainews-*`）归档到 `_archive/`。

**Why**：
- 标准命名 → 跨项目复用 skill 时模式一致，Agent 能基于固定文件名做条件加载策略
- 单一职责拆分 → 原 `ainews-project-architecture.md` 混合了事实+决策+进度，一改全连动
- 归档而非删除 → 保留历史快照能力，但不污染日常加载链

**How to apply**：
- 新增记忆条目 → 优先 append 到对应核心文件
- 单文件超过 ~300 行或主题混杂 → 拆出 `feedback_<topic>.md` / `synthesis_<topic>.md`
- 一次性调研结果落地到 skill 后 → 归档到 `_archive/<topic>-snapshot-<date>.md`

---

## 相关记忆

- [[project_overview]] — 决策对应的实施位置
- [[project_progress]] — 决策对应的阶段时间线
- [[feedback]] — 协作规范（部分决策由用户反馈驱动）
