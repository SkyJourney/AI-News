# Vault 落盘协议（skill 内部参考）

> 本文件是 `/ai-news` 内 fetcher/cluster/writer subagent 的**自包含落盘约定**——因为 subagent 启动时不读 vault 根的 `SCHEMA.md`，所以这里完整镜像一份。
> 与 vault 根 `/Volumes/Projects/AInews/SCHEMA.md` 同步维护：改一处必须改另一处。

最后同步：2026-06-27

---

## 1. vault 目录用途

| 目录 | `/ai-news` 谁写 | 写什么 |
|---|---|---|
| `00-Inbox/` | (暂不写) | 流水线缓冲，v1 直接跳过，writer 直接写 10-Daily/50-Zettel |
| `10-Daily/` | news-writer | 当日简报，一天一文件 |
| `20-Topics/` | news-cluster + news-writer | 主题文件（append 模式） |
| `40-Deep-Dives/` | (不写) | 人工领域，skill 不动 |
| `50-Zettel/` | news-writer | 原子卡，一题一卡 |
| `90-Archive/` | (不写) | 人工归档 |
| `99-Log/` | 主会话（Phase 5） + Phase 0 死链报告 | 运行日志 |

---

## 2. 文件命名（强约定）

| 类型 | 模式 | 示例 |
|---|---|---|
| Daily 简报 | `10-Daily/YYYY-MM-DD.md` | `10-Daily/2026-06-27.md` |
| Zettel 原子卡 | `50-Zettel/YYYYMMDDHHmm-<slug>.md` | `50-Zettel/202606271430-gpt5-multimodal.md` |
| Topic 主题 | `20-Topics/<slug>.md` | `20-Topics/model-releases.md` |
| 运行日志 | `99-Log/YYYY-MM-DD-run.md` | `99-Log/2026-06-27-run.md` |
| 死链报告 | `99-Log/YYYY-MM-DD-source-deadcheck.md` | `99-Log/2026-06-27-source-deadcheck.md` |

**Zettel 时间戳 ID 规则**：`YYYYMMDDHHmm`（12 位，分钟级），用本地时区（Asia/Shanghai）。多张卡同分钟时往后顺延 1 分钟。

**slug 规则**：小写连字符、ASCII、不超过 50 字符；从条目标题取关键词，去掉停用词。

---

## 3. Frontmatter 必填字段

### Daily 简报
```yaml
---
created: 2026-06-27 18:00:00
status: published
entry_count: 12          # 当日纳入条目数
sources_alive: 10        # 成功抓的源数
sources_dead: 2          # 死掉的源数
topics: [model-releases, safety, opensource]
tags: [daily-digest, llm, safety]    # daily-digest + 当日主要技术领域 tag（详见 filter-criteria §5）
previous_daily: 2026-06-26           # 若昨日 Daily 存在则填，便于反向跳转
---
```

### Zettel 原子卡
```yaml
---
created: 2026-06-27 18:00:00
status: draft
source: openai-rss       # 必须是 sources.md 内的 name
source_url: https://openai.com/news/xxx
topic: model-releases    # 引用或创建 20-Topics/<slug>.md
tags: [llm, multimodal]
---
```

### Topic 主题（append 模式，首次创建写 frontmatter，后续 append 不动 frontmatter）
```yaml
---
created: 2026-06-27 18:00:00
updated: 2026-06-27 18:00:00
entry_total: 1           # 累计纳入条目数（每次 append 后 writer 更新）
---
```

### 运行日志
```yaml
---
created: 2026-06-27 18:00:00
run_duration_seconds: 87
sources_attempted: 12
sources_alive: 10
sources_dead: 2
entries_fetched: 47
entries_after_dedup: 38
entries_after_filter: 25
zettel_written: 8
---
```

---

## 4. Wikilink 规范

| 引用 | 写法 | 示例 |
|---|---|---|
| 跨目录引 Zettel | 时间戳 ID（**不用标题**） | `[[202606271430-gpt5-multimodal]]` |
| 引 Topic | slug | `[[model-releases]]` |
| 引 Daily | 日期 | `[[2026-06-27]]` |
| 引 vault 外资源（sources.md 等） | Markdown 链接，不用 wikilink | `[sources.md](.claude/skills/ai-news/references/sources.md)` |

**Daily 简报中典型一段写法**：
```markdown
## 🤖 模型发布

- **GPT-5 多模态版本** ([[202606271430-gpt5-multimodal]])
  来自 [[openai-rss]]，强调 vision-audio 端到端。
  → 详见 [[model-releases]]
```

---

## 5. 落盘前自检清单（每个 writer subagent 必跑）

写文件前自检：
1. 目录正确？（§1）
2. 文件名符合 §2 模式？（特别是 Zettel 时间戳 ID 是 12 位本地时区分钟）
3. frontmatter 字段齐全？（§3 按文件类型）
4. wikilink 用了时间戳 ID 而非标题？（§4）
5. `source:` 字段引用的 name 在 [sources.md](sources.md) 内？
6. Topic 文件首次创建用 Write、后续 append 用 Edit（**绝不重写 Topic 文件**，会丢历史）

任何一项不满足，停下不写，把问题写入 99-Log。
