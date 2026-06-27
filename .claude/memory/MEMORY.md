# Memory Index
> _Last synced: 2026-06-27 | Base commit: `8756e50`_

本目录是 AInews 的**项目记忆**，随仓库 git 管理。Obsidian 默认不索引 `.claude/` 隐藏目录，故不混入笔记图谱。新会话先读本目录了解项目上下文。

**原则**：记忆只留"跨会话需要知道的有效信息"——架构决策、当前状态、CLI 能力。一次性调研结果落地到 skill 后归档到 `_archive/`。

| 文件 | 描述 | 类型 | 引用 | Commit |
|------|------|------|------|--------|
| [ainews-project-architecture.md](ainews-project-architecture.md) | 已落地架构、文件分布、14 源摘要、脆弱点、基础设施增强、演进路径 | project | 1 | `8756e50` |
| [obsidian-vault-cli-facts.md](obsidian-vault-cli-facts.md) | Obsidian 官方 CLI 能力边界 + AInews vault 标识 | reference | 1 | `8756e50` |

## 归档（_archive/，仅备查）

- `_archive/ainews-source-matrix-snapshot-2026-06-27.md` — 信息源 v1 实测调研快照。结论已 100% 落地到 `.claude/skills/ai-news/references/sources.md` 与 `blacklist.md`，本文件仅供"为何 a16z RSS 在黑名单 / 为何 Meta 更新慢"等历史溯源
