# AInews Vault SCHEMA

> 任何 AI agent 在本 vault 内**写文件之前必读本文件**。这是 vault 的根公约。
> 与本文件配套但角色不同：`.claude/skills/ai-news/references/vault-schema.md` 是 `/ai-news` 采集管道内部 subagent 的镜像参考；本文件是给"路过 vault 的所有 AI"看的根约定。两者内容一致，更新时需同步。

最后更新：2026-06-27

---

## 1. 目录约定

| 目录 | 用途 | 谁写 |
|---|---|---|
| `00-Inbox/` | 原始抓取、未消化条目；进入流水线前的缓冲 | `/ai-news` fetcher、人手收集 |
| `10-Daily/` | 每日简报（汇总层），一天一文件 | `/ai-news` writer |
| `20-Topics/` | 主题汇聚笔记（如"模型发布""安全对齐"）；同一主题文件持续 append | `/ai-news` cluster + 人手维护 |
| `40-Deep-Dives/` | 专题深度研究（人手发起 + `deep-research` skill 协助） | 人手为主 |
| `50-Zettel/` | 原子概念卡（Zettelkasten，一题一卡，强双链） | `/ai-news` writer + 人手 |
| `90-Archive/` | 归档过期/低价值内容 | 人手为主 |
| `99-Log/` | 运行日志（采集时间、错误、统计、源死链报告） | `/ai-news` + 任何自动化流程 |

⚠️ **信息源登记不在 vault 内**——12 个源的 tier/perspective/fetch_method/url/reliability/last_verified 全部归 `.claude/skills/ai-news/references/sources.md` 单一权威。vault 不再设 `30-Sources/` 目录。

---

## 2. 文件命名

| 类型 | 模式 | 示例 |
|---|---|---|
| Daily 简报 | `10-Daily/YYYY-MM-DD.md` | `10-Daily/2026-06-27.md` |
| Zettel 原子卡 | `50-Zettel/YYYYMMDDHHmm-<slug>.md` | `50-Zettel/202606271430-gpt5-multimodal.md` |
| Topic 主题笔记 | `20-Topics/<slug>.md`（小写连字符） | `20-Topics/model-releases.md` |
| Deep Dive | `40-Deep-Dives/YYYY-MM-<slug>.md` | `40-Deep-Dives/2026-06-rlhf-survey.md` |
| 运行日志 | `99-Log/YYYY-MM-DD-<run-type>.md` | `99-Log/2026-06-27-run.md`、`99-Log/2026-06-27-source-deadcheck.md` |

**Zettel 的时间戳 ID（`YYYYMMDDHHmm-`）是强约定**：用于跨目录 wikilink 时防重名失链。

---

## 3. Frontmatter 通用字段

所有由 AI 自动写入的文件必须含 YAML frontmatter。基础字段（缺一不可）：

```yaml
---
created: 2026-06-27T14:30:00+08:00   # ISO 8601 with local tz
updated: 2026-06-27T14:30:00+08:00
status: draft | published | archived
source: openai-rss                    # 引用 .claude/skills/ai-news/references/sources.md 的 name
topic: model-releases                 # 引用或创建 20-Topics/<slug>.md
tags: [llm, multimodal]               # 自由标签，便于 Obsidian 检索
---
```

扩展字段按文件类型补充（Zettel 加 `links_in/links_out` 统计；Daily 加 `entry_count`；Log 加 `run_duration_seconds`）。

---

## 4. Wikilink 规范

- **跨目录引用 Zettel** → 一律用时间戳 ID：`[[202606271430-gpt5-multimodal]]`，不要用文件名/标题
- **引用 Topic** → 用 slug：`[[model-releases]]`
- **引用 Daily** → 用日期：`[[2026-06-27]]`
- **不在 vault 内的资源**（信息源登记、采集脚本）→ 用相对路径 Markdown 链接，不用 wikilink：`[sources.md](.claude/skills/ai-news/references/sources.md)`

---

## 5. AI 落盘前自检清单

写文件前 AI 应自检：
1. 目录正确？（按 §1 表）
2. 文件名符合 §2 模式？
3. frontmatter 字段齐全？（§3）
4. wikilink 用了时间戳 ID 而非标题？（§4）
5. `source` 字段引用的 source 在 `.claude/skills/ai-news/references/sources.md` 内（不在则先登记或选 fallback）

任何一项不满足，停下不写。
