<!-- Last updated: 2026-06-27 | Commit: 8756e50 -->

# AInews

aliases: AInews, ai-news, AI 新闻, AI资讯, AI新闻

AI 资讯 Obsidian vault + 采集管道。所有采集逻辑在 `.claude/skills/ai-news/` + `.claude/agents/`。

## 新会话入口

- 项目当前状态 → `.claude/memory/ainews-project-architecture.md`
- vault 落盘约定 → `SCHEMA.md`
- 采集管道编排 → `.claude/skills/ai-news/SKILL.md`
- 信息源（14 个）→ `.claude/skills/ai-news/references/sources.md`
- vault 总览导航 → `MOC.md`

## 关键约定

- 信息源元数据**不在 vault 内**，归 skill `references/sources.md` 单一权威
- vault 内文件由 `news-writer` subagent 写，frontmatter 必须按 `references/vault-schema.md`
- 触发采集：`/ai-news`（手动，`disable-model-invocation: true`）
- 调试单源：`bash .claude/skills/ai-news/scripts/test-fetcher.sh <source_name>`

## 记忆体系（会话启动必读）

> **强制规则**：每次新会话启动时，必须先读取本项目的记忆体系索引，再按需加载关键记忆文件，然后才能开始处理用户请求。长会话中若上下文被压缩，同样需要重新加载。

### 读取流程

1. **读取索引**：`cat .claude/memory/MEMORY.md` — 获取记忆文件清单与最近更新状态（含 Base commit 锚点）
2. **必读文件**（每次会话必须加载）：
   - `ainews-project-architecture.md` — 已落地架构、14 源摘要、脆弱点、基础设施增强、演进路径
3. **按需加载**（与当前任务相关时加载）：
   - `obsidian-vault-cli-facts.md` — Obsidian 官方 CLI 边界 + AInews vault 标识（涉及 vault CLI / 注册流程时）
   - `_archive/ainews-source-matrix-snapshot-2026-06-27.md` — 信息源 v1 实测调研快照（涉及"为何 X 源在黑名单"等历史溯源时）
4. **健康检查报告**（按需查看）：
   - `lint_report.md` — 最新一次 memory-lint 结果与待处理项

### 记忆目录

```
.claude/memory/
├── MEMORY.md                           # 索引（入口）
├── ainews-project-architecture.md      # 项目架构（必读，type=project）
├── obsidian-vault-cli-facts.md         # CLI 与 vault 标识（按需，type=reference）
├── lint_report.md                      # 健康检查报告（type=lint，自动生成）
└── _archive/                           # 调研快照归档（仅历史溯源）
    └── ainews-source-matrix-snapshot-2026-06-27.md
```

> 记忆文件是跨会话持久化的知识，优先级高于 Agent 的默认推断。若记忆内容与当前代码状态冲突，以代码为准并更新记忆。
