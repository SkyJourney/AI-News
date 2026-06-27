# Memory Index
> _Last synced: 2026-06-27 | Base commit: `d729cc9`_

本目录是 **AInews 的项目记忆**，随仓库 git 管理。Obsidian 默认不索引 `.claude/` 隐藏目录，故不混入笔记图谱。新会话先读本目录了解项目上下文。

**原则**：记忆只留"跨会话需要知道的有效信息"——架构决策、当前状态、协作规范、外部引用。一次性调研结果落地到 skill 后归档到 `_archive/`。

## 必读（每次会话）

| 文件 | 描述 | 类型 | 引用 | Commit |
|------|------|------|------|--------|
| [project_overview.md](project_overview.md) | 项目定位、技术栈、目录结构、核心组件职责 | project | 4 | `d729cc9` |
| [project_progress.md](project_progress.md) | 阶段进度、当前状态、待办、已观测脆弱点 | project | 3 | `d729cc9` |
| [decisions.md](decisions.md) | 11 条关键架构决策与理由（What + Why + How） | project | 4 | `d729cc9` |
| [feedback.md](feedback.md) | 9 条协作规范（语言/确认流程/不引 MCP 等） | feedback | 2 | `d729cc9` |

## 按需加载

| 文件 | 描述 | 类型 | 引用 | Commit |
|------|------|------|------|--------|
| [reference.md](reference.md) | Obsidian CLI 边界 / vault 标识 / 调试脚本 / 信息源指针 | reference | 2 | `d729cc9` |
| [lint_report.md](lint_report.md) | memory-lint 最近一次执行报告 | lint | 0 | 自动生成 |

## 归档（`_archive/`，仅供历史溯源）

- `_archive/architecture-snapshot-2026-06-27.md` — 旧版 ainews-project-architecture（已规范化拆分到 project_overview / progress / decisions）
- `_archive/obsidian-cli-facts-snapshot-2026-06-27.md` — 旧版 obsidian-vault-cli-facts（已并入 [[reference#R1]] + [[reference#R2]]）
- `_archive/ainews-source-matrix-snapshot-2026-06-27.md` — 信息源 v1 实测调研快照（结论已落地 `sources.md` / `blacklist.md`）
