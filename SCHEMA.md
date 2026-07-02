# AInews Vault SCHEMA

> 任何 AI agent 在本 vault 内**写文件之前必读本文件**。这是 vault 的根公约。
> 与本文件配套但角色不同：`.claude/skills/ai-news/references/vault-schema.md` 是 `/ai-news` 采集管道内部 subagent 的镜像参考；本文件是给"路过 vault 的所有 AI"看的根约定。两者内容一致，更新时需同步。

最后更新：2026-07-01

---

## 1. 目录约定

| 目录 | 用途 | 谁写 |
|---|---|---|
| `00-Inbox/` | **Phase 间 IPC 中间产物**：fetch.json / filtered.json / cluster.json，一跑一组（共用同一 HHMM）。subagent 输出大 JSON 直接 Write 到这里，主会话只传文件路径，规避 32k token 输出上限。也供 `--from-cache=<filename>` 跨跑调试/断点恢复 | `/ai-news` Phase 1 主会话 + Phase 2 filter + Phase 3 cluster |
| `10-Daily/` | 每日简报（汇总层），一天一文件，**含 wikilink / Zettel ID / Bases 字段**，是 vault 内部档案 | `/ai-news` writer |
| `20-Topics/` | 主题汇聚笔记（如"模型发布""安全对齐"）；同一主题文件持续 append | `/ai-news` cluster + 人手维护 |
| `30-Digests/` | **可分享/可打印的纯文本汇总版**——基于同日 cluster 输出生成，去 wikilink、URL 完整展开、章节自包含；读者无 Obsidian 也能完整阅读 | `/ai-news` digester |
| `40-Deep-Dives/` | 预留 v2 weekly/monthly digester（待积累 ≥7 天 30-Digests/ 历史后启用，识别跨日延续主题、热门 topic 趋势线）；当前阶段也接受人手发起 + `deep-research` skill 协助的专题长文 | 暂留空（v2 自动 + 人手） |
| `50-Zettel/` | 原子概念卡（Zettelkasten，一题一卡，强双链） | `/ai-news` writer + 人手 |
| `60-Originals/` | 原文全文离线归档（含翻译版 + 图片资产），每天从 10-Daily + 30-Digests 上条目抓取；vault **自包含**的基石层 | `/ai-news` originalizer |
| `90-Archive/` | 归档过期/低价值内容 | 人手为主 |
| `99-Log/` | 运行日志（采集时间、错误、统计、源死链报告） | `/ai-news` + 任何自动化流程 |

⚠️ **信息源登记不在 vault 内**——14 个源的 tier/perspective/fetch_method/url/reliability/last_verified 全部归 `.claude/skills/ai-news/references/sources.md` 单一权威。vault 不再设 `30-Sources/` 目录。

⚠️ **`10-Daily/` 与 `30-Digests/` 是同一份 cluster 输出的两个渲染视图**——前者面向 vault 内部 PKM 工作流（双链、概念回溯），后者面向外部分享/打印（自包含、可印）。两者不互相派生，digester 直接消费 cluster 的 `topics` JSON。

⚠️ **`60-Originals/` 是其他层的双链目标**——vault 自 F1 起以本层为原文单一权威，10-Daily / 20-Topics / 30-Digests / 50-Zettel 引用条目时统一双链到 60-Originals，不再直接嵌外部 URL；外链失效不影响 vault 完整性。

---

## 2. 文件命名

| 类型 | 模式 | 示例 |
|---|---|---|
| Phase 1 Fetch 缓存 | `00-Inbox/YYYY-MM-DD-HHMM-fetch.json` | `00-Inbox/2026-06-29-0816-fetch.json` |
| Phase 2 Filter 中间产物 | `00-Inbox/YYYY-MM-DD-HHMM-filtered.json` | `00-Inbox/2026-06-29-0816-filtered.json` |
| Phase 3 Cluster 中间产物 | `00-Inbox/YYYY-MM-DD-HHMM-cluster.json` | `00-Inbox/2026-06-29-0816-cluster.json` |
| Daily 简报 | `10-Daily/YYYY-MM-DD.md` | `10-Daily/2026-06-29.md` |
| Zettel 原子卡 | `50-Zettel/YYYYMMDDHHmm-<slug>.md` | `50-Zettel/202606291430-gpt5-multimodal.md` |
| 60-Originals 原文 | `60-Originals/YYYY-MM-DD-HHMM-<slug>.md`（与 Zettel ID 同源，同 HHMM） | `60-Originals/2026-07-01-0816-openai-gpt5-preview.md` |
| 60-Originals 图片资产 | `60-Originals/_assets/YYYY-MM-DD/<id>-<n>.<ext>`（`<id>` 同主文件、`<n>` 3 位补零 `001` 起） | `60-Originals/_assets/2026-07-01/2026-07-01-0816-openai-gpt5-preview-001.png` |
| Topic 主题笔记 | `20-Topics/<slug>.md`（小写连字符） | `20-Topics/model-releases.md` |
| Digest 分享版 | `30-Digests/YYYY-MM-DD-digest.md`（一天一文件） | `30-Digests/2026-06-29-digest.md` |
| Deep Dive / Weekly | `40-Deep-Dives/YYYY-MM-<slug>.md` 或 `40-Deep-Dives/YYYY-Www-weekly.md` | `40-Deep-Dives/2026-W26-weekly.md` |
| 运行日志 | `99-Log/YYYY-MM-DD-<run-type>.md` | `99-Log/2026-06-29-run.md`、`99-Log/2026-06-29-source-deadcheck.md` |

**Zettel 的时间戳 ID（`YYYYMMDDHHmm-`）是强约定**：用于跨目录 wikilink 时防重名失链。

**60-Originals 与 Zettel 同 HHMM**：同一条原文对应的 60-Originals 主文件与 50-Zettel（若产出）共用同一 HHMM，便于精确配对与反查；同 HHMM 内多条时同源顺延 1 分钟（沿用 Zettel 规则）。

**IPC 文件 HHMM 同跑绑定**：同一跑次产生的 `fetch.json / filtered.json / cluster.json` 三个 IPC 文件**必须共用同一 HHMM**——这是 Phase 链跨阶段定位中间产物的唯一锚。主会话 Phase 1 落 fetch.json 时锁定 HHMM，传给后续所有 phase。`--from-cache=<filename>` 接受三种文件中的任意一种，从对应 phase 起跑。

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

扩展字段按文件类型补充（Zettel 加 `title`/`title_original`；Daily 加 `entry_count`；Log 加 `run_duration_seconds`）。

### 50-Zettel 原子卡

```yaml
---
created: 2026-06-27 18:00:00
status: draft
title: <中文主标题>          # 8-24 字新闻体，从"概念/事件"段落归纳；必填
title_original: <原文标题>   # 原文标题原样保留（不论中英文），作副标题；查不到/无必要时可省略
source: openai-rss
source_url: https://openai.com/news/xxx
topic: model-releases
tags: [llm, multimodal]
---
```

### 60-Originals 原文全文（F1 起启用）

```yaml
---
id: 2026-07-01-0816-openai-gpt5-preview   # 同文件名 stem
type: source-original
title: <中文标题>
original_title: <原文标题>
source_name: openai-rss                    # 引用 sources.md 的 name
source_url: <原文 URL>
author: []                                 # 作者列表，可为空数组
published_at: 2026-07-01                   # 原文发布日期
fetched_at: 2026-07-01T08:16:00+08:00      # 抓取时间戳
language: en                               # 原文语种 en|zh|ja|...
translated: true                           # 是否有翻译版
translation_engine: haiku                  # 翻译模型（默认 haiku；language=zh 时可为 null）
word_count: 2340                           # 中文正文字数
images_attempted: 3                        # 尝试下载的图片数
images_saved: 2                            # 成功保存到 _assets 的数
fallback_notice: null                      # 抓失败时填人可读原因；否则 null
related_daily: 2026-07-01                  # originalizer 首写时填
related_zettels: []                        # F1.4 writer 回填 [[YYYYMMDDHHmm-slug]]
related_topics: []                         # F1.4 writer/cluster 回填 [[topic-slug]]
tags: [source-original, language-en]
---
```

**字段语义约束**：
- `id` 必须与文件名 stem（去 `.md` 后缀）完全一致，充当 wikilink 目标
- `fallback_notice` 是三态：`null` = 抓取正常、字符串 = 抓失败/降级原因、字段缺失 = 未启用 originalizer
- `related_*` 三字段模板中永远存在（默认 `[]` / `""`），便于 Bases 视图无 undefined 分支

### 日期聚合排序约定（跨文件类型通用）

任何文件内出现**多条按日期分组/罗列**的结构（Topic 现有的 `## YYYY-MM-DD` 区块，未来 Zettel"更新历史"、Deep-Dives 周报/月报"大事记"等），一律**倒序排列（最新在前）**——正序等于把最新内容埋在最下面。新增此类结构时写入逻辑要一开始就按倒序设计，不要等页面渲染出问题才回头补。

---

## 4. Wikilink 规范

- **跨目录引用 Zettel** → 一律用时间戳 ID：`[[202606271430-gpt5-multimodal]]`，不要用文件名/标题
- **引用 Topic** → 用 slug：`[[model-releases]]`
- **引用 Daily** → 用日期：`[[2026-06-27]]`
- **引用 60-Originals** → 用 id（同文件名 stem，不带目录前缀）：`[[2026-07-01-0816-openai-gpt5-preview]]`
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
6. 若写 60-Originals：`images_attempted` / `images_saved` 已如实统计？抓失败已在 `fallback_notice` 填人可读原因（不留空 null）？

任何一项不满足，停下不写。
