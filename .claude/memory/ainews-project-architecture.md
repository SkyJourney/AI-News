---
name: ainews-project-architecture
description: AInews 项目当前架构与状态——已落地的核心决策，跨会话必读
metadata:
  type: project
---

AInews = `/Volumes/Projects/AInews` 作为 AI 资讯的 Obsidian vault + 本地 git。

## 已落地架构（8 commit，2026-06-27）

- **分层**：采集 = Claude Code skill + subagent；vault = 纯落盘知识库。管道与仓库解耦。
- **采集**：内置 WebFetch / Bash + arXiv/HF 官方 API + curl 健康检查。**不依赖第三方 MCP**（用户明确否决）。
- **产出**：双层——`10-Daily/YYYY-MM-DD.md` 简报 + `50-Zettel/YYYYMMDDHHmm-<slug>.md` 原子卡。
- **触发**：手动 `/ai-news`（`disable-model-invocation: true`，仅用户触发）；v2 推荐 Desktop scheduled tasks。
- **目录**：vault 7 层 `00-Inbox / 10-Daily / 20-Topics / 40-Deep-Dives / 50-Zettel / 90-Archive / 99-Log`。**没有** `30-Sources/`——信息源全部归 `.claude/skills/ai-news/references/sources.md` 单一权威。

## 文件分布（实施所在）

```
.claude/
├── skills/ai-news/
│   ├── SKILL.md             # 5-phase 编排 + retry + V2 调度占位
│   ├── references/          # sources / blacklist / vault-schema / filter-criteria
│   └── scripts/             # source-health.sh / arxiv-fetch.py
├── agents/                  # 6 个原生 subagent：fetcher-{rss,api,webfetch} + filter + cluster + writer
└── memory/                  # 本文件 + obsidian-vault-cli-facts + _archive/
```

## 信息源（当前 14 个，详见 sources.md）

- Tier 1 主力 4（OpenAI / DeepMind / arXiv / HF Daily Papers）
- Tier 2 聚合分析 4（Import AI / Interconnects / 量子位 / Air Street Press）
- Tier 3 webfetch 兜底 6（Anthropic / Meta AI / The Batch / 机器之心 / a16z / State of AI）
  - meta-ai-blog 标 `reliability: degraded`（80+ 天无新内容实测）
  - state-of-ai 是"事件锁集"型源（平日 0 条）

## 已演化但仍需关注的脆弱点

- **fetcher 主观拒绝**：fetcher-rss 与 fetcher-webfetch 都加了"不要因外部因素主观拒绝"约束（commit ddda56a 与 adc4e48）。若新加 fetcher 类型需复用同模式约束。
- **retry 机制**：SKILL.md Phase 1 有 first-fail 自动 retry 1 次；雪崩保护 > 3 个失败不 retry。
- **Zettel 时间戳冲突**：writer 用本地时区分钟级 ID；同分钟多卡顺延 1 分钟。多次跑同日时要注意不撞 ID。

## 演进路径（计划中）

1. 跑稳几天后启用 Desktop scheduled tasks（每日 9:03 local）
2. Obsidian Bases 数据库视图给 vault 加结构化导航
3. 跨多日 Log 趋势统计脚本（>= 7 天数据后）

## 相关记忆

- [[obsidian-vault-cli-facts]] — Obsidian CLI 边界
- `_archive/ainews-source-matrix-snapshot-2026-06-27.md` — 原始信息源实测调研（内容已落地到 sources.md / blacklist.md，归档保留）
