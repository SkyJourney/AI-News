---
name: ainews-project-architecture
description: AInews 项目当前架构与状态——已落地核心决策、文件分布、14 源摘要、脆弱点、基础设施
type: project
last_updated: 2026-06-27
commit: 8756e50
---

AInews = `/Volumes/Projects/AInews` 作为 AI 资讯的 Obsidian vault + 本地 git。

## 已落地架构（11 commit，2026-06-27）

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

## 基础设施增强（Tier 2-3，commit fb0e170 + 8756e50）

- **3 个 Obsidian Bases 视图**（vault 根 `_base-*.base`）：按主题 / 按 source / Daily 时间线+健康度监控。frontmatter 即数据，无需 Dataview。
- **scripts/test-fetcher.sh**：单源调试入口 `bash test-fetcher.sh <source_name>`——显示元数据 + 活性 + 内容采样 + spawn 命令模板。已修 bash 3.2 中文符号紧跟变量名 unbound variable 坑（用 `${var}` brace + 中文换 ASCII）。
- **fetcher 三类全加 `low_confidence` 字段**：fetcher-rss/api/webfetch 每条 entry 都要带；触发条件含模糊 URL/严重缺摘要/非直链等。下游 filter/cluster/writer 用该字段决策严格度。
- **filter-criteria.md §5 Tags 规范**：writer 给 Daily/Zettel/Topic 打 4 类 tag（技术领域/公司/事件类型/来源 tier）；小写 kebab-case、不用中文、2-5 个/条。
- **vault 根 MOC.md**：Map of Content 总览入口；动静分离设计（静态结构人维护、动态内容交给 Bases）。
- **writer Daily 加"📍 昨日回顾"段**：写 Daily 前 Glob 昨日文件 + Read TL;DR，列延续/反差/完成三类跨日链；frontmatter 加 `previous_daily` 字段。

## 演进路径（计划中）

1. 跑稳几天后启用 Desktop scheduled tasks（每日 9:03 local）
2. 跨多日 Log 趋势统计脚本（>= 7 天数据后）
3. 视情况按多日使用感受调整 Zettel 原子化粒度

## 相关记忆

- [[obsidian-vault-cli-facts]] — Obsidian CLI 边界
- `_archive/ainews-source-matrix-snapshot-2026-06-27.md` — 原始信息源实测调研（内容已落地到 sources.md / blacklist.md，归档保留）
