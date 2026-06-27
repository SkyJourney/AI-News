---
name: feedback
description: AInews 协作规范与用户偏好——避免重犯已纠正的错误
type: feedback
last_updated: 2026-06-27
commit: d729cc9
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

## 相关记忆

- [[project_overview]] — 项目整体上下文
- [[decisions]] — 由 feedback 演化出的具体技术决策
