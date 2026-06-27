---
name: ainews-project-architecture
description: AInews 项目定位与已敲定的核心架构决策（采集/仓库分层、采集手段、产出形态、触发、目录结构、分阶段实施）
metadata:
  type: project
---

AInews = 把 `/Volumes/Projects/AInews` 做成「AI 资讯」的 Obsidian vault + 本地 git 管理。已与用户对齐并敲定的架构决策（2026-06-27）：

- **分层（核心）**：采集+整理 = Claude Code 的 **skill + subagent**（智能抓取 / 去重 / 信噪过滤 / 总结 / 按主题归并）；**vault = 纯落盘知识库**（只负责存储 / 组织 / 检索，不承担订阅拉取）。管道与仓库解耦。
- **采集手段**：走**轻量内置**——Claude Code 内置 WebSearch/WebFetch + arXiv/HF **官方 API**；**不依赖第三方 MCP**（用户明确顾虑其非官方、稳定性与按需输出存疑；实测也证明该路风险高）。是否引入官方 MCP 留到 v2 再单独验证。
- **明确否决**：① 不把 RSS 当"统一拉取基础设施"（RSS 只是数据格式之一，不挂 vault 内 RSS 插件做管道）；② 不依赖第三方 MCP server。
- **产出形态**：**双层**——`10-Daily/` 每日简报（汇总层）+ `50-Zettel/` 原子概念卡（可双链复用）。
- **触发方式**：**定时自动**（scheduled agent / cron）；但先做手动 skill `/ai-news`，调稳后再包一层定时。
- **目录结构（v2，已落盘）**：vault 内 7 个目录 `00-Inbox / 10-Daily / 20-Topics / 40-Deep-Dives / 50-Zettel / 90-Archive / 99-Log`。⚠️ 砍掉了 v1 的 vault 内 `30-Sources/`——信息源完整登记（tier/perspective/fetch_method/url/reliability/last_verified）+ 死源黑名单单一权威归 `.claude/skills/ai-news/references/{sources,blacklist}.md`，**vault 不再持有信息源元数据**。
- **可复用基建**：编排可复用环境内已有的 `deep-research` skill 与 `Workflow` 多 agent 工具（AI 资讯聚合 ≈ 周期性的轻量 deep-research + 落盘）。

**实施分两阶段**：
- ✅ **阶段一已完成（2026-06-27，commit `8b063c0`）** = vault 极简骨架：7 目录 + 各放 `.gitkeep` + `SCHEMA.md`（vault 根 AI 协议）+ `README.md` + `.gitignore`（.obsidian 共享配置入库、忽略 workspace*.json/缓存/.trash）+ 首次 git 提交。**信息源登记不在 vault 内**，挪到阶段二 skill `references/`。
- 阶段二（待执行） = 采集管道：`.claude/skills/ai-news/{SKILL.md, references/, scripts/}` + `.claude/agents/` 6 个原生 subagent（news-fetcher-rss/api/webfetch + news-filter + news-cluster + news-writer）。基于 Claude 官方 [skills](https://code.claude.com/docs/en/skills) 与 [sub-agents](https://code.claude.com/docs/en/sub-agents) 文档；编排不用 Workflow 工具，SKILL.md 文字指引主会话 spawn subagent。调度暂缓（V2 首选 Desktop scheduled tasks，PASS Cloud Routines 因无法访问本地 vault）。完整 plan：`~/.claude/plans/misty-splashing-hopcroft.md`。

相关：[[ainews-source-matrix]]、[[obsidian-vault-cli-facts]]。
