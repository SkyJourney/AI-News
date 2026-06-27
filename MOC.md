---
created: 2026-06-27T20:30:00+08:00
updated: 2026-06-27T20:30:00+08:00
status: published
tags: [moc, navigation]
---

# AInews — Map of Content

> AI 资讯知识库导航。新会话/打开 vault 从这里开始。
>
> **本文件人工维护**：新增 topic 或视图后顺手更新这里。日期类信息（最新 Daily / 本周热点）用下面的 Bases 视图动态看，不写死。

---

## 📰 最新动态

- **Daily 时间线 + 健康度监控** → [[_base-latest-daily]]（Bases 视图）
- **本周新增 Zettel** → 见 [[_base-by-topic]] 视图"按主题分组"，按 created 倒序
- 触发新一轮 `/ai-news` 抓取最新

## 🗂️ 主题入口（`20-Topics/`）

按事件类型组织。同主题文件 append 模式累积。

- 🤖 **模型/产品发布** → [[model-releases]]
- 🛡️ **安全 / 对齐 / 治理** → [[safety-alignment]]
- 📑 **学术（LLM 方法论）** → [[research-papers-llm]]
- 🧪 **学术（应用 / 科学 ML）** → [[research-papers-applied]]
- 🏢 **公司动态 / 人才流动** → [[industry-moves]]
- 💰 **融资 / 投资** → [[funding-investment]]
- 🖥️ **基础设施 / 硬件** → [[infra-hardware]]
- 🧬 **健康 / 科学应用** → [[applications-health-science]]
- 🛠️ **其他应用 / 工具** → [[applications]]

（出现 ≥ 2 条才独立成桶；新主题由 cluster 自动创建并加 `new_topic: true` 标记。）

## 🔍 数据库视图（Obsidian Bases）

| 视图 | 用途 |
|---|---|
| [[_base-by-topic]] | 按主题分组看所有 Zettel；高优 draft 单视图；卡片视图 |
| [[_base-by-source]] | 按来源切片（一手 / 学术 / 投资视角） |
| [[_base-latest-daily]] | Daily 时间线 + 卡片视图 + 健康度异常检测 |

需要新视图？添加 `_base-<name>.base` 到 vault 根。

## 🔗 信息源（14 个，1 个 degraded）

- 完整登记 → [`.claude/skills/ai-news/references/sources.md`](.claude/skills/ai-news/references/sources.md)
- 死源黑名单 → [`.claude/skills/ai-news/references/blacklist.md`](.claude/skills/ai-news/references/blacklist.md)
- 过滤 / 聚类 / 打标准则 → [`.claude/skills/ai-news/references/filter-criteria.md`](.claude/skills/ai-news/references/filter-criteria.md)

## ⚙️ 工作流

| 操作 | 命令 |
|---|---|
| 跑全流程 | `/ai-news` |
| 指定日期 | `/ai-news --date=YYYY-MM-DD` |
| 仅健康检查 | `/ai-news --dry-run` |
| 调试单源 | `bash .claude/skills/ai-news/scripts/test-fetcher.sh <name>` |
| 全源活性 | `bash .claude/skills/ai-news/scripts/source-health.sh` |

## 📚 文档

- vault 落盘协议 → [[SCHEMA]]
- 项目说明 → [[README]]
- 采集编排 → [`.claude/skills/ai-news/SKILL.md`](.claude/skills/ai-news/SKILL.md)
- subagent 6 个 → `.claude/agents/news-*.md`

## 🗃️ 归档

- 人工归档资讯 → `90-Archive/`
- 项目记忆调研快照 → `.claude/memory/_archive/`
