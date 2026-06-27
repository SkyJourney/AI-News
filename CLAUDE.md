# AInews

aliases: AInews, ai-news, AI 新闻, AI资讯, AI新闻

AI 资讯 Obsidian vault + 采集管道。所有采集逻辑在 `.claude/skills/ai-news/` + `.claude/agents/`。

## 新会话入口
- 项目当前状态 → `.claude/memory/ainews-project-architecture.md`
- vault 落盘约定 → `SCHEMA.md`
- 采集管道编排 → `.claude/skills/ai-news/SKILL.md`
- 信息源（14 个） → `.claude/skills/ai-news/references/sources.md`

## 关键约定
- 信息源元数据**不在 vault 内**，归 skill `references/sources.md` 单一权威
- vault 内文件由 `news-writer` subagent 写，frontmatter 必须按 `references/vault-schema.md`
- 触发采集：`/ai-news`（手动，`disable-model-invocation: true`）
