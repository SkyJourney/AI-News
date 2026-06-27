<!-- Last updated: 2026-06-27 | Commit: d729cc9 -->

# AInews

aliases: AInews, ai-news, AI 新闻, AI资讯, AI新闻

**AI 资讯 Obsidian vault + 采集管道**。仓库根同时是 vault 根与代码根：vault 层（`10-Daily/`、`50-Zettel/` 等）存知识，工具层（`.claude/skills/ai-news/` + `.claude/agents/`）跑采集。两层**物理同居、逻辑解耦**——vault 不依赖管道也能用 Obsidian 看，管道可独立替换而不动已落盘内容。

> Agent 的事实/状态/决策细节全部在 `.claude/memory/`。本文件只声明**全局硬约束**与**入口指针**。

---

## 入口指针

| 资源 | 路径 |
|---|---|
| 项目记忆索引 | `.claude/memory/MEMORY.md`（必读 4 件套 + 按需 reference + 历史归档） |
| vault 落盘根公约 | `SCHEMA.md`（写盘前 5 项自检） |
| 采集管道编排 | `.claude/skills/ai-news/SKILL.md`（5 phase：Preflight → Fetch → Filter → Cluster → Write → Log） |
| 信息源单一权威 | `.claude/skills/ai-news/references/sources.md` |
| 死源黑名单 | `.claude/skills/ai-news/references/blacklist.md` |
| 过滤/聚类/打标准则 | `.claude/skills/ai-news/references/filter-criteria.md` |
| vault 导航 MOC | `MOC.md`（人工维护静态结构 + Bases 动态视图） |
| 本机运行时清单 | `~/.claude/ENVIRONMENTS.md` |

---

## 全局硬约束（Agent 必守）

按优先级：

1. **vault ↔ 管道解耦**——配置/脚本/agent 一律放 `.claude/`，**不**塞进 `10-Daily/`、`20-Topics/` 等 vault 目录；vault 内文件不写管道实现细节。
2. **信息源元数据只在 `references/sources.md`**——vault 内**没有** `30-Sources/`，不要新建。新增/降级/拉黑源只改 `sources.md` + `blacklist.md`。
3. **不引入第三方 MCP**——抓取与编排只用 Claude Code 原生（WebFetch / Bash + curl / 原生 Agent / 官方 API）。真有需求**先问用户**。
4. **`/ai-news` 仅手动触发**——skill frontmatter `disable-model-invocation: true` 是硬约束；**不要**自作主张跑，也不要在文档里暗示自动化。
5. **vault 写盘前必读 `SCHEMA.md`**——5 项自检（目录正确 / 命名符合 / frontmatter 齐全 / wikilink 用时间戳 ID / source 已登记），任一不满足停下不写。
6. **`SCHEMA.md` ↔ `references/vault-schema.md` 双份同步**——前者给所有 AI 看，后者是 `/ai-news` 内部镜像，改一处必须同步另一处。
7. **arXiv 走脚本，不走主会话 curl**——`scripts/arxiv-fetch.py` 内置 3 秒限流（arXiv 礼仪），主会话直接 curl 会违规。

---

## 工作流速查

| 我要做 | 用什么 |
|---|---|
| 跑今天全流程 | `/ai-news` |
| 跑指定日期 | `/ai-news --date=YYYY-MM-DD` |
| 仅健康检查（不抓不写） | `/ai-news --dry-run` |
| 调试单个 fetcher | `bash .claude/skills/ai-news/scripts/test-fetcher.sh <source_name>` |
| 全源活性 | `bash .claude/skills/ai-news/scripts/source-health.sh` |
| 新加 / 改 / 拉黑源 | 改 `references/sources.md` + `blacklist.md`，**不动 vault** |
| 改 vault 目录约定 | 同步改 `SCHEMA.md` + `references/vault-schema.md` |
| 加新 Bases 视图 | 写 `_base-<name>.base` 到 vault 根，更新 MOC |

---

## 文件改动安全边界

按"是否需要事前确认"分级：

### 🟢 可直接改（< 5 行、纯文档/typo）

- README.md / MOC.md 的链接/说明微调
- 99-Log/ 内自动生成的日志
- 00-Inbox/ 缓冲区（v1 未启用）

### 🟡 改前先描述 + 等确认

- `SCHEMA.md` / `references/vault-schema.md`（vault 公约，影响所有 AI 写盘）
- `.claude/skills/ai-news/SKILL.md`（管道编排骨架）
- `.claude/agents/news-*.md`（6 个 subagent system prompt）
- `references/sources.md` / `blacklist.md` / `filter-criteria.md`（采集行为权威）
- `.claude/memory/` 内 5 件套（记忆体系，跨会话）

### 🔴 不动 / 改必先问

- `10-Daily/` / `20-Topics/` / `50-Zettel/` 内**已落盘的历史文件**（用户审阅的产出）
- `_archive/`（历史快照，只读）
- `.git/`、`.obsidian/`（系统配置）

### Git 操作

- **不**主动 `git commit` / `git push`（等用户明确说"提交"/"推送"）
- `git add` 用具体文件名，避免 `git add -A`
- **不**用 `--no-verify` / `--no-edit` 等绕过 hook 的标志

---

## 记忆体系（会话启动必读）

> **强制规则**：每次新会话启动时，必须先读取本项目的记忆体系索引，再按需加载关键记忆文件，然后才能开始处理用户请求。长会话中若上下文被压缩，同样需要重新加载。

### 读取流程

1. **读取索引**：`cat .claude/memory/MEMORY.md` — 获取记忆文件清单与最近更新状态（含 Base commit 锚点）
2. **必读文件**（每次会话必须加载）：
   - `project_overview.md` — 项目定位、技术栈、目录结构、核心组件职责
   - `project_progress.md` — 阶段进度、当前状态、待办、已观测脆弱点
   - `decisions.md` — 11 条关键架构决策与理由（What + Why + How）
   - `feedback.md` — 9 条协作规范（语言、确认流程、不引 MCP 等）
3. **按需加载**（与当前任务相关时加载）：
   - `reference.md` — Obsidian CLI 边界 / vault 标识 / 调试脚本 / 信息源指针（涉及 CLI、调试、源管理时）
4. **健康检查报告**（按需查看）：
   - `lint_report.md` — 最新一次 memory-lint 结果与待处理项
5. **归档备查**（仅历史溯源时）：
   - `_archive/architecture-snapshot-2026-06-27.md` — 旧版项目架构快照
   - `_archive/obsidian-cli-facts-snapshot-2026-06-27.md` — 旧版 CLI 边界快照
   - `_archive/ainews-source-matrix-snapshot-2026-06-27.md` — 信息源 v1 实测调研快照

### 记忆目录

```
.claude/memory/
├── MEMORY.md                # 索引（入口）
├── project_overview.md      # 项目总览（必读，type=project）
├── project_progress.md      # 阶段进度（必读，type=project）
├── decisions.md             # 架构决策（必读，type=project）
├── feedback.md              # 协作规范（必读，type=feedback）
├── reference.md             # 外部资源指针（按需，type=reference）
├── lint_report.md           # 健康检查报告（type=lint，自动生成）
└── _archive/                # 历史快照（仅溯源）
    ├── architecture-snapshot-2026-06-27.md
    ├── obsidian-cli-facts-snapshot-2026-06-27.md
    └── ainews-source-matrix-snapshot-2026-06-27.md
```

> 记忆文件是跨会话持久化的知识，优先级高于 Agent 的默认推断。若记忆内容与当前代码状态冲突，以代码为准并更新记忆。
