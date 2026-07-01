# Memory Index
> _Last synced: 2026-07-01 | Base commit: `9b48c6a`（MVP 达成 + ROADMAP 重写 F1/F2 双主线）· **F2.0 完成待 commit**（Quartz 5 决策，见 [[decisions#D15]]）_

本目录是 **AInews 的项目记忆**，随仓库 git 管理。Obsidian 默认不索引 `.claude/` 隐藏目录，故不混入笔记图谱。新会话先读本目录了解项目上下文。

**原则**：记忆只留"跨会话需要知道的有效信息"——架构决策、当前状态、协作规范、外部引用。一次性调研结果落地到 skill 后归档到 `_archive/`。

**权威分工**：
- **本目录** = 记忆体系（决策 / 进度快照 / 协作规范 / 外部指针）
- **`.claude/skills/ai-news/ROADMAP.md`** = 演化跟踪权威（Sprint 任务、执行流水、优先级）
- 两处「未来方向摘要」双向同步，见 [[feedback#F10]]

## 必读（每次会话）

| 文件 | 描述 | 类型 | 引用 | Commit |
|------|------|------|------|--------|
| [project_overview.md](project_overview.md) | 项目定位、技术栈、目录结构、8 个 subagent 职责、未来层指针 | project | 5 | `9b48c6a` |
| [project_progress.md](project_progress.md) | Stage 1-10 里程碑 + 当前状态（v2.4 MVP 达成）+ ROADMAP 摘要 | project | 4 | `9b48c6a` |
| [decisions.md](decisions.md) | 15 条架构决策（含 D14 F1/F2 双主线 + D15 F2 采用 Quartz 5） | project | 5 | `9b48c6a` (D15 待 commit) |
| [feedback.md](feedback.md) | 10 条协作规范（含 F10 progress ↔ ROADMAP 双向同步） | feedback | 3 | `9b48c6a` |

## 按需加载

| 文件 | 描述 | 类型 | 引用 | Commit |
|------|------|------|------|--------|
| [reference.md](reference.md) | Obsidian CLI 边界 / 调试脚本 / 信息源指针 / R9 ROADMAP 路径 | reference | 3 | `9b48c6a` |
| [lint_report.md](lint_report.md) | memory-lint 最近一次执行报告 | lint | 0 | 自动生成 |

## 归档（`_archive/`，仅供历史溯源）

- `_archive/architecture-snapshot-2026-06-27.md` — 旧版 ainews-project-architecture（已规范化拆分到 project_overview / progress / decisions）
- `_archive/obsidian-cli-facts-snapshot-2026-06-27.md` — 旧版 obsidian-vault-cli-facts（已并入 [[reference#R1]] + [[reference#R2]]）
- `_archive/ainews-source-matrix-snapshot-2026-06-27.md` — 信息源 v1 实测调研快照（结论已落地 `sources.md` / `blacklist.md`）
