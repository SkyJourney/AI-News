---
name: decisions
description: AInews 关键架构决策与理由——避免重复讨论已决事项，新会话基于既定路径继续
type: project
last_updated: 2026-07-01
commit: 9b48c6a
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

## D12：v2 流程上线 — Phase 5 Digest 集成 + 00-Inbox 缓存层

**决策**（2026-06-28）：在 Write 与 Log 之间插入 Phase 5 Digest，原 Phase 5/6 顺延为 6/7；激活 `00-Inbox/` 作为 fetch JSON 缓存层；预留 `40-Deep-Dives/` 给 v2 weekly digester。

**Why**：
- **Daily 是 vault 内部档案，Digest 是给外人看的**——10-Daily/ 含 wikilink/Zettel ID/Bases 字段，没 Obsidian 看不全；30-Digests/ 去链接、URL 展开、章节自包含，可独立分享/打印
- **digester 必须与 writer 并列消费 cluster 输出，不能从 Daily 二次解析**——writer 渲染 Daily 时会漏 URL（"未升级 Zettel"条目只标 source_name 不挂链接），digester 从 Daily 反推会信息有损；v1 试跑就出现 GPT-5 免疫学 source 张冠李戴、合成"AI 行业人才流动监测"元条目等 6 类问题
- **00-Inbox 激活解决重跑/调试成本**——纯内存流意味着调试 filter/cluster/writer/digester 时必须重 fetch（~25 分钟）；落盘 inbox JSON + `--from-cache` flag 后，下次跑同日只需 ~15 分钟
- **40-Deep-Dives 不删而预留**——周报/月报需要 ≥7 天 30-Digests/ 历史数据才有意义，当前还不到时候；显式标注预留比保留为空目录更清晰

**How to apply**：
- 新加 Phase 必须**同时**改 SKILL.md（编排）+ subagent system prompt（执行）+ SCHEMA.md/vault-schema.md（约定），三处双向同步
- 给"分享版"渲染层（digester / 未来 weekly）输入设计原则：**接 cluster 这一层的结构化数据，不接已渲染层**——避免渲染层之间互相依赖造成信息有损
- 新增 digester 类 subagent system prompt 必含"事实性硬约束"段（禁止合成 / source_name 严格 / URL 必填 / 去重自检 / 字数上限），v1 试跑暴露这些是 LLM 总结类任务的共性失败模式
- 调试任何下游 phase → 先用 `/ai-news --from-cache=<inbox.json>` 跳过 Phase 1，对上游源友好
- 周报启用阈值：积累 ≥7 天 30-Digests/ 后写 news-weekly-digester subagent + SKILL.md 加 Phase 5.5（或 Phase 8）

---

## D13：v2.4 — Fetcher IPC 改 Write 中转，根治 token 截断 + 时窗双源 + URL 编码 bug

**决策**（2026-06-30）：三个长期边界 bug 一次性根治：
1. **Bug 3（fetcher 文本截断）**：4 个 fetcher subagent 改 Write per-source 中转文件 `00-Inbox/<date>-<hhmm>-fetch-<source>.json`，主输出仅返 `{output_path, source_name, entry_count, error}`；新增 `scripts/fetch-merge.py` 由主会话调用合并为总 fetch.json
2. **Bug 2（fetcher 7d 时窗与 §2.5 14d 阈值冲突）**：4 个 fetcher prompt 删除"过滤 7 天前"步骤，时窗判定**单一权威**在 filter-inline.py §2.5
3. **Bug 1（cluster URL `&` → `&amp;` 编码）**：cluster-merge.py 加 `html.unescape(url)` 防御反转义，不信任 agent 输出格式

**Why**：
- **Bug 3 是 v2.3 IPC 设计的核心瓶颈**——fetcher 用 assistant 文本回报 entries，触发 LLM 输出 token 上限（arxiv 20 篇 × 500 字摘要 ≈ 7-8k tokens；the-batch 15 长 issue 同问题；a16z 15 条 entry 多字段同问题），主会话只能拿到"样本几条 + 文字说明已抓 N 条"。**真实抓取数据反复永久丢失**（git log 多次复现）。v2.4 复用 cluster v2.3 已验证的"agent 出精简返回 + 文件作真实数据传递"模式，agent Write 文件无 token 上限，主会话靠 path Read 拿真实数据。
- **Bug 2 是 v1 残留**——fetcher prompt"7d 过滤"在 v2.3 引入 §2.5 后没同步删，导致 7-14d 窗口的有效内容（如 openai 6-16 deployment-simulation、the-batch 5-29 issue-355）被 fetcher 提前剔，没机会进 §2.5 统一判定。DRY 原则要求时窗判定单源。
- **Bug 1 是 LLM 训练数据偏置**——cluster agent 把 URL 里 `&` 误转 HTML 实体 `&amp;`（jiqizhixin URL 含 `?type=2&query=...` 几乎每次中招），污染下游 _seen-urls 回填。`html.unescape()` 一行兜底所有 HTML 实体（&amp; / &lt; / &gt; / &#39;），不依赖 LLM 服从 prompt 约束。
- **三个 bug 捆绑改**——Bug 2 跟 Bug 3 都在 fetcher prompt 修改范围内（一次性改完避免回归）；Bug 1 在 cluster-merge.py 是独立小修。

**How to apply**：
- **Phase 1 编排变化**：HHMM 从 Phase 1 末锁定提前到 Phase 1 开头（spawn fetcher 前主会话必须知道 per-source path）；spawn fetcher 时 prompt 必含 `output_path` 字段；收 agent 返回 `{output_path, count, error}` 后跑 fetch-merge.py 合并
- **per-source 中转文件不入 git**（.gitignore 排除 `00-Inbox/*-fetch-*.json`），保留作单源 debug；总 fetch.json / filtered.json / cluster.json 仍入 git（catch-up `--from-cache` 模式依赖）
- **新增 fetcher 类型**（如未来 v2.5 加 RSSHub 备份源）→ 复用 v2.4 同款 system prompt 模板：tools 含 Write、输入含 output_path、不做时窗过滤、Write 完整 JSON + 主输出精简、URL 不转义约束
- **fetcher 失败时仍 Write 文件**（带 error 字段 + entries:[]）让 fetch-merge.py 统一归 failures，避免文件缺失走"per_source_missing"路径
- **fetcher retry** 直接覆盖原 path（无需特殊处理）
- **如未来某 fetcher 大量 entry 不再适配文本 prompt** → 不需要改架构，本设计已无 token 上限
- **不要把 fetcher 主输出格式回退到带 entries 数组**——会重新触发 Bug 3
- **不要给 cluster-merge.py 加"严格 url 校验失败就 abort"** —— 已有 unknown_urls / missing_urls 兜底足够，agent 偶有错产出归 errors[] 不阻断

**对应改动 commit**：`08cffbb`（v2.4 主提交）

---

## D14：MVP 后续按 F1 + F2 双主线，ROADMAP.md 为权威跟踪基准

**决策**（2026-07-01）：v2.4 MVP 达成后，后续开发以两条主线推进：
1. **F1 · 60-Originals 全量离线化**——vault 新增 `60-Originals/` 层，每天抓 10-Daily + 30-Digests 上全部条目原文，haiku 翻译外文/规整中文，10/20/40/50 全链路改双链引用
2. **F2 · Vault 前端站点**——Mac mini 本地 docker compose + nginx（端口 40801），私有化部署，后续接内网穿透；框架 POC 3 选 1 实施时定

**Why**：
- **F1 让 vault 自包含**——不再依赖外部 URL，未来外链失效或被删也不丢内容；下游 digester / 前端展示层都直接消费本地全文，一致性更高
- **F2 让 vault 对外可展**——GitHub 做内容管理 + 前端页面做呈现，对外效果显著优于让人直接翻 markdown 文件；私有化部署避开 GitHub Pages 依赖，Mac mini 已有稳定运行环境
- **F1 → F2 顺序**——F1 产出的 60-Originals 是 F2 详情页的天然数据源；反序则 F2 只能挂外链，做完还要回改
- **调度已达成不再是主线**——Mac mini cron + Claude 非交互跑通，取消原 D4 的"V2 Desktop scheduled tasks"待办
- **老 A4-A9 编号列表退役**——按 F1/F2 主线做过合并/升级/延后（详见 ROADMAP.md「合并说明」表），单独维护会与主线脱节

**How to apply**：
- **`.claude/skills/ai-news/ROADMAP.md` 是权威跟踪基准**——所有 Sprint 任务清单、执行状态、优先级调整只改 ROADMAP，不散落到其他文档
- **project_progress.md 与 ROADMAP.md 双向同步**——见 [[feedback#F10]]；project_progress 只维护快照 + 里程碑历史，不与 ROADMAP 内容冲突
- **新决策接续 D14 之后编号**（D15, D16...），本条不再被覆盖
- **F1/F2 落地节奏**：F1 完成后先跑 3 天观察 → Sprint 2 评估 → 再启 F2；不并行做以免上下文断裂
- **不启用第三个主线**——除非用户显式提出，且要评估是否挤压 F1/F2

**对应改动 commit**：`d421e60`（ROADMAP.md 重写）

---

## 相关记忆

- [[project_overview]] — 决策对应的实施位置
- [[project_progress]] — 决策对应的阶段时间线
- [[feedback]] — 协作规范（部分决策由用户反馈驱动）
