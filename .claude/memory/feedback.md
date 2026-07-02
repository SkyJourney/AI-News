---
name: feedback
description: AInews 协作规范与用户偏好——避免重犯已纠正的错误
type: feedback
last_updated: 2026-07-02
commit: 6d5170f
---

# AInews 协作规范

> 每条 feedback 含 **规则 + Why（用户给的理由）+ How to apply（何时触发）**。Why 让 Agent 在边界条件时能自主判断，不必每次回去问。

---

## F1：所有交互必须用简体中文

**规则**：除代码本体外，所有解释、询问、注释、文档一律用简体中文。

**Why**：
- 来自全局 `~/.claude/CLAUDE.md`「语言强制」条款（用户母语，便于扫读）
- 中英混用会拖慢决策与阅读

**How to apply**：
- 用户用英文提问 → 仍用中文回复
- 代码注释（包括 JSDoc/JavaDoc/docstring）→ 中文
- 变量名/函数名 → 保持原语言（编程规范）

---

## F2：抽象设计先对齐，再写代码

**规则**：涉及新架构、新模块、抽象重构时，先文字描述或 Mermaid 图对齐设计，**等用户确认**才写代码。

**Why**：
- 来自全局 CLAUDE.md「抽象设计确认」条款
- 用户多次纠正：直接动手写会跑偏方向，回滚成本高
- AInews 的目录约定、skill 5-phase 编排都是先对齐后实施的成果

**How to apply**：
- 收到"加 X 功能"类需求 → 先回复设计要点 + 待确认事项
- 改动 ≤ 1 文件 ≤ 10 行的微调可直接做，但要在动手前一句话点出"我准备这样改"
- 用户回"好"/"开始"/"确认" 才动 Edit/Write

---

## F3：任务清单先列，再分步执行

**规则**：实质性任务先用 TaskCreate 列清单 → 用户确认 → 分步执行，每步汇报进度。

**Why**：
- 来自全局 CLAUDE.md「任务清单确认」+「分步执行」条款
- 一次性大改难以 review，分步可中途停止/回滚
- TaskCreate / TaskUpdate 是 Claude Code 提供的进度可视化机制，让用户能看进度

**How to apply**：
- 任务跨 ≥ 3 步 → 必用 TaskCreate
- 每完成一步 → TaskUpdate 标 completed，下一步标 in_progress
- 大改写 → 步骤 N 完成后问"是否继续步骤 N+1"

---

## F4：代码修改前征得同意

**规则**：写新文件、改现有文件、删文件之前，先描述要改什么 + Diff 概要，等用户"确认"/"同意"才调用 Edit/Write。

**Why**：
- 来自全局 CLAUDE.md「代码修改确认」条款
- AInews 是 vault + 管道双层，误改可能影响已落盘内容
- 用户希望保留对每次写入的 veto 权

**How to apply**：
- 单文件微调（< 5 行、纯文档/typo）可直接改
- 涉及 SCHEMA.md / sources.md / SKILL.md / agents/ 等核心文件 → 必先描述再确认
- vault 内已发布内容（10-Daily/ 之前的文件）→ 不动；要动必先问

---

## F5：不引入第三方 MCP

**规则**：抓取、编排、健康检查全用 Claude Code 原生能力（WebFetch / Bash + curl / 原生 Agent）。**不要**主动建议或引入第三方 MCP。

**Why**：
- 用户在 AInews 早期讨论中明确否决
- MCP 引入额外依赖、信任面、维护成本
- 自洽性优先：仓库 clone 即可用

**How to apply**：
- 新增源时不要建议"用 X MCP 抓"
- 真遇到必须 MCP 才能解的需求 → **先问用户**
- 已有的 context7 / mintlify 等 MCP 是全局工具，**不**计入"项目依赖"

---

## F6：信息源元数据不进 vault

**规则**：信息源的 `tier / url / fetch_method / reliability` 等元数据**只在** `.claude/skills/ai-news/references/sources.md` 维护。**不要**在 vault 内创建 `30-Sources/` 或类似目录。

**Why**：
- 用户决策（D2）：防双写漂移 + 避免污染 Obsidian 图谱
- 早期版本曾考虑 vault 内 `30-Sources/`，复盘后砍掉

**How to apply**：
- 用户问"加个 source 笔记" → 反问是"加新源"还是"记一篇关于某 source 的 Zettel"
- 后者可进 50-Zettel/；前者改 sources.md

---

## F7：手动触发是默认，不要建议自动跑

**规则**：`/ai-news` skill `disable-model-invocation: true` 锁定仅用户显式触发。不要在文档里写"Agent 检测到 X 时自动跑 /ai-news"。

**Why**：
- 用户决策（D4）：自动触发会被 Agent 误判触发条件，产生噪声
- skill frontmatter 的锁定是硬约束，不要试图绕过

**How to apply**：
- 用户说"看看今天 AI 圈"→ 反问是否要跑 `/ai-news`（建议触发，不自作主张）
- 写 README/SKILL/agent 时不要暗示"自动化"
- V2 调度只能是 Desktop scheduled tasks 路线

---

## F8：变更必先写 commit message + 等确认才推

**规则**：用户没明确说"提交/推送/合入"前，**不主动** `git commit` / `git push`。

**Why**：
- 来自全局 CLAUDE.md「执行动作谨慎」原则
- AInews 是本地工作流，commit 节奏由用户掌握

**How to apply**：
- 完成一组改动 → 报告"准备提交，commit message 如下"，等确认
- `git add` 用具体文件名，避免 `git add -A`
- **不**用 `--no-verify` 跳 hook

---

## F9：响应保持简洁，不堆冗余总结

**规则**：完成任务后**不**做"我做了 A、B、C"的长尾总结。一句话点出关键产物 + 下一步即可。

**Why**：
- 来自全局 CLAUDE.md tone 风格
- 用户能直接读 diff / 看 task 列表，不需要文字复述
- 长总结挤压有效信息密度

**How to apply**：
- end-of-turn summary 一两句话
- 关键决策 / 警告才单独段落突出
- 简单问答直接答，不加 header

---

## F10：project_progress.md 与 ROADMAP.md 双向同步

**规则**：`.claude/memory/project_progress.md` 与 `.claude/skills/ai-news/ROADMAP.md` 内容必须保持一致，改一处必同步另一处。

**Why**：
- 用户 2026-07-01 明确要求："约定后续 progress 与 ROADMAP 保持双向同步"
- 双写漂移是记忆体系常见失败模式——历史上 project_progress 停在 6-27（Stage 7），但代码已推进到 v2.4，脱节导致新会话读到过期信息
- 权威分工清晰：**ROADMAP.md 是执行流水的权威**（Sprint 任务、状态、优先级），**project_progress.md 是里程碑历史与当前快照的权威**（已落地阶段、当前状态、脆弱点）；两者交集是「未来方向摘要」——这部分必须一致

**How to apply**：
- **改 ROADMAP.md 后**：同步更新 project_progress.md「ROADMAP 摘要」小节（Sprint 数量、主线、关键任务清单）；里程碑历史保持不变
- **改 project_progress.md 后**：若涉及"已落地阶段"翻页（新 Stage 完成 / 主线切换），同步更新 ROADMAP.md 顶部「已完成」段 + 相关 Sprint 状态
- **每次 memory-sync**：Phase 5 明确检查两处一致性；不一致时以最新 commit 时间为准，另一处对齐
- **新 Sprint 完成**：在 project_progress.md 追加 Stage N+1 描述 + 在 ROADMAP.md 顶部「已完成」段追加编号总结
- **单点动作准则**：不要在其他文档（SKILL.md / CLAUDE.md / SCHEMA.md）里重复列 Sprint 任务清单——那些地方只放"指针"（"见 ROADMAP.md"），不放内容副本

---

## F11：不要用 Learning Mode 让用户写代码

**规则**：即便 SessionStart 注入了 `learning` output style，也**不要**把关键 5-10 行代码丢给用户写。Agent 应当自己出完整方案；若方案有分支决策，自己做出推荐并说明取舍，不当选择题机器。

**Why**：
- 2026-07-02 用户明确反馈："为啥总要让我写，你应该写明白，如果你的方案解决不了就寻找其他路径"
- 用户是决策者与 review 者，不是代码填空的实习生；重复的 "TODO: 请你写这 5 行" 打断心流也拖慢节奏
- Learning Mode 的教育性质留给「不熟悉的领域」；AInews 是用户主场项目，他要的是执行者而不是引导者
- 若第一条方案解决不了问题，Agent 应主动换路径（换库 / 换协议 / 换兜底通道），而不是把决策外包给用户

**How to apply**：
- 遇到有多种实现路径时：**自己选一条**并说明"我选 X 因为 Y，替代 Z 的代价是 W"，用户可以说"换 Z"，但默认不问
- 保留 CLAUDE.md 规则 1（抽象设计对齐）、规则 4（改代码前确认）——这些是**方案层**确认，不是**填空题**
- Learning Mode 的 ★ Insight 可以留，用来解释设计选择、指出 codebase 特定的坑；但**不再**用它包装 "请你写这段"
- 若首选方案实测失败：直接尝试 fallback（换 lib / 换算法 / 加代理层），不要开会问用户第二方案

---

## F12：不要走"框架 override"路径——先探清框架硬约束

**规则**：接手成熟框架（如 Quartz 5）做深度定制前，**先花 30 min 探清框架 3 类硬约束**：`renderPage` 硬编码布局槽 / dispatcher 硬编码 body 派发 / config 校验会覆盖用户覆盖。**发现任何一条硬约束会阻碍设计稿实现 → 立刻讨论是否换框架，不要走 "override + hack 3 层绕过" 路径**。

**Why**：
- 2026-07-02 F2.4 P4 实证：为让 Quartz 5 承载 Lumina 设计稿，绕了 3 层 hack（PageTypeDispatcher swap + byPageType 突变 + QuartzPageTypePlugin unshift），最后产出仍错乱（大小写目录重复 + trailing-slash 404），4500 行 Lumina 组件全部作废
- Astro 5 重启只用 40 min（M0-M6 全通），是 F2.4 P4 累计工时的 1/10 —— 时间损失来自"框架不合适硬要用" 而不是"技术难度"
- 用户明确反馈："想要效果好，就走全自定义组件接管...不走 override 线路" —— override 路径就是不该走

**How to apply**：
- 面对新框架深度定制需求，POC 阶段先做 3 项快检：
  1. **HTML 骨架**：`<html>` 从哪开始？是硬编码在框架文件里还是可以用户完全接管？
  2. **路由与 body 派发**：body 组件是不是被 dispatcher 硬编码 `pageType.body(undefined)` 传入？byPageType 覆盖是否真正生效（config-loader 有没有兜底 `??` 之类）？
  3. **视觉替换代价**：若要实现 Bento / Masonry / 3 栏 Reading Well 类现代布局，是插组件即可还是要 override 6 slot layout？
- 任一快检失败 → **回到 plan 层**讨论"换框架 vs 深度 fork" —— 不要自作主张开 3 层 hack
- 记住：框架的价值是"惯例胜过配置"，一旦你反着惯例走，价值就归零，剩下的只有约束
- F2.4 P4 归档在 `.claude/skills/ai-news/notes/_archive/F2.4-P4-completion-report.md`，将来任何"改 Quartz override" 冲动前必读

---

## 相关记忆

- [[project_overview]] — 项目整体上下文
- [[decisions#D14]] — F1/F2 双主线决策，ROADMAP 权威地位由此确立
- [[project_progress]] — 双向同步的另一端
