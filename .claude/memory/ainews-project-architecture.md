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
- **目录结构**：AI 资讯定制版 `00-Inbox / 10-Daily / 20-Topics / 30-Sources / 40-Deep-Dives / 50-Zettel / 90-Archive / 99-Log`。
- **可复用基建**：编排可复用环境内已有的 `deep-research` skill 与 `Workflow` 多 agent 工具（AI 资讯聚合 ≈ 周期性的轻量 deep-research + 落盘）。

**实施分两阶段（均尚未执行）**：
- 阶段一 = vault 骨架落盘：建目录 + `SCHEMA.md` + `30-Sources/` 信息源登记 + `.gitignore`（.obsidian 共享配置入库、忽略 workspace*.json/缓存/.trash）+ `README.md` + 首次 git 提交。计划已经用户批准，但用户选择**新开会话执行**。
- 阶段二 = 采集管道（skill + subagent），待阶段一落地后单独规划。

相关：[[ainews-source-matrix]]、[[obsidian-vault-cli-facts]]。
