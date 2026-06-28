# AInews Vault SCHEMA

> 任何 AI agent 在本 vault 内**写文件之前必读本文件**。这是 vault 的根公约。
> 与本文件配套但角色不同：`.claude/skills/ai-news/references/vault-schema.md` 是 `/ai-news` 采集管道内部 subagent 的镜像参考；本文件是给"路过 vault 的所有 AI"看的根约定。两者内容一致，更新时需同步。

最后更新：2026-06-27

---

## 1. 目录约定

| 目录 | 用途 | 谁写 |
|---|---|---|
| `00-Inbox/` | **Phase 1 fetcher 输出的原始 JSON 缓存**——每跑落盘一份，供 `--from-cache` 调试 / 同日重跑跳过 fetch / 断点恢复 | `/ai-news` Phase 1（主会话写） |
| `10-Daily/` | 每日简报（汇总层），一天一文件，**含 wikilink / Zettel ID / Bases 字段**，是 vault 内部档案 | `/ai-news` writer |
| `20-Topics/` | 主题汇聚笔记（如"模型发布""安全对齐"）；同一主题文件持续 append | `/ai-news` cluster + 人手维护 |
| `30-Digests/` | **可分享/可打印的纯文本汇总版**——基于同日 cluster 输出生成，去 wikilink、URL 完整展开、章节自包含；读者无 Obsidian 也能完整阅读 | `/ai-news` digester |
| `40-Deep-Dives/` | 预留 v2 weekly/monthly digester（待积累 ≥7 天 30-Digests/ 历史后启用，识别跨日延续主题、热门 topic 趋势线）；当前阶段也接受人手发起 + `deep-research` skill 协助的专题长文 | 暂留空（v2 自动 + 人手） |
| `50-Zettel/` | 原子概念卡（Zettelkasten，一题一卡，强双链） | `/ai-news` writer + 人手 |
| `90-Archive/` | 归档过期/低价值内容 | 人手为主 |
| `99-Log/` | 运行日志（采集时间、错误、统计、源死链报告） | `/ai-news` + 任何自动化流程 |

⚠️ **信息源登记不在 vault 内**——14 个源的 tier/perspective/fetch_method/url/reliability/last_verified 全部归 `.claude/skills/ai-news/references/sources.md` 单一权威。vault 不再设 `30-Sources/` 目录。

⚠️ **`10-Daily/` 与 `30-Digests/` 是同一份 cluster 输出的两个渲染视图**——前者面向 vault 内部 PKM 工作流（双链、概念回溯），后者面向外部分享/打印（自包含、可印）。两者不互相派生，digester 直接消费 cluster 的 `topics` JSON。

---

## 2. 文件命名

| 类型 | 模式 | 示例 |
|---|---|---|
| Fetch 缓存 | `00-Inbox/YYYY-MM-DD-HHMM-fetch.json`（一跑一文件） | `00-Inbox/2026-06-27-0900-fetch.json` |
| Daily 简报 | `10-Daily/YYYY-MM-DD.md` | `10-Daily/2026-06-27.md` |
| Zettel 原子卡 | `50-Zettel/YYYYMMDDHHmm-<slug>.md` | `50-Zettel/202606271430-gpt5-multimodal.md` |
| Topic 主题笔记 | `20-Topics/<slug>.md`（小写连字符） | `20-Topics/model-releases.md` |
| Digest 分享版 | `30-Digests/YYYY-MM-DD-digest.md`（一天一文件） | `30-Digests/2026-06-27-digest.md` |
| Deep Dive / Weekly | `40-Deep-Dives/YYYY-MM-<slug>.md` 或 `40-Deep-Dives/YYYY-Www-weekly.md` | `40-Deep-Dives/2026-W26-weekly.md` |
| 运行日志 | `99-Log/YYYY-MM-DD-<run-type>.md` | `99-Log/2026-06-27-run.md`、`99-Log/2026-06-27-source-deadcheck.md` |

**Zettel 的时间戳 ID（`YYYYMMDDHHmm-`）是强约定**：用于跨目录 wikilink 时防重名失链。

---

## 3. Frontmatter 通用字段

所有由 AI 自动写入的文件必须含 YAML frontmatter。基础字段（缺一不可）：

```yaml
---
created: 2026-06-27 14:30:00   # ISO 8601 with local tz
updated: 2026-06-27 14:30:00
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
- **引用 MOC** → `[[MOC]]`（vault 总览入口）
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
