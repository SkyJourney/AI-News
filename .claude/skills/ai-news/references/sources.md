# AInews 信息源登记（v1，实测 2026-06-27）

> 本文件是 `/ai-news` skill 的**唯一权威源清单**。vault 内不存源元数据。
> 每次正式接入前需复验 URL 时效（RSS/API 会变动）。
> 死源/黑名单见 [blacklist.md](blacklist.md)。
> 数据格式：纯 YAML 列表，便于 `scripts/source-health.sh` 用 grep 解析（每条 source 一个 `url:` 行）。

---

## sources

```yaml
# === Tier 1 主力（✅ 一手 + 学术）===

- name: openai-rss
  tier: 1
  perspective: research
  fetch_method: rss
  url: https://openai.com/news/rss.xml
  reliability: alive
  last_verified: 2026-06-27
  notes: 官方一手

- name: deepmind-rss
  tier: 1
  perspective: research
  fetch_method: rss
  url: https://deepmind.google/blog/rss.xml
  reliability: alive
  last_verified: 2026-06-27
  notes: Google DeepMind 官方

- name: arxiv-api
  tier: 1
  perspective: research
  fetch_method: api
  url: http://export.arxiv.org/api/query
  reliability: alive
  last_verified: 2026-06-27
  notes: 按 cat:cs.AI/cs.LG + sortBy=submittedDate 检索；返回 Atom XML；严格 3 秒/次限流（arXiv 礼仪）；由 scripts/arxiv-fetch.py 封装

- name: huggingface-daily-papers
  tier: 1
  perspective: research
  fetch_method: api
  url: https://huggingface.co/api/daily_papers
  reliability: alive
  last_verified: 2026-06-27
  notes: JSON，带 upvotes 社区策展，信噪比最高，自带 arxiv id 可回链；支持 ?date=YYYY-MM-DD

# === Tier 2 聚合分析层（✅ 周更/日更）===

- name: import-ai
  tier: 2
  perspective: research
  fetch_method: rss
  url: https://importai.substack.com/feed
  reliability: alive
  last_verified: 2026-06-27
  notes: Jack Clark 周更，政策/治理/前沿深度

- name: interconnects
  tier: 2
  perspective: research
  fetch_method: rss
  url: https://www.interconnects.ai/feed
  reliability: alive
  last_verified: 2026-06-27
  notes: Nathan Lambert，RLHF/训练/开源硬核；部分付费墙仅摘要

- name: qbitai
  tier: 2
  perspective: product
  fetch_method: rss
  url: https://www.qbitai.com/feed
  reliability: alive
  last_verified: 2026-06-27
  notes: 中文高频近日更；需 filter 过滤融资/PR 软文

- name: air-street-press
  tier: 2
  perspective: investor
  fetch_method: rss
  url: https://press.airstreet.com/feed
  reliability: alive
  last_verified: 2026-06-27
  notes: 投资层里唯一开箱即用、干净、免费、时效到当天的结构化源

# === Tier 3 降级源（⚠️ 无官方 RSS，靠 WebFetch 兜底）===

- name: anthropic-news
  tier: 3
  perspective: research
  fetch_method: webfetch
  url: https://www.anthropic.com/news
  reliability: alive
  fallback: true
  last_verified: 2026-06-27
  notes: 无官方 RSS

- name: meta-ai-blog
  tier: 3
  perspective: research
  fetch_method: webfetch
  url: https://ai.meta.com/blog/
  reliability: degraded
  fallback: true
  last_verified: 2026-06-27
  notes: 无 RSS 且更新极慢（2026-06-27 实测最新内容仍是 2026-04-08，80+ 天无新文）；filter 会按 stale 全弃；保留入清单仅为偶发更新；arXiv 兜底

- name: the-batch
  tier: 3
  perspective: research
  fetch_method: webfetch
  url: https://www.deeplearning.ai/the-batch/
  reliability: alive
  fallback: true
  last_verified: 2026-06-27
  notes: 吴恩达周评，质量最高几乎无软文；无官方 RSS

- name: jiqizhixin
  tier: 3
  perspective: product
  fetch_method: webfetch
  url: http://plink.anyfeeder.com/weixin/almosthuman2014
  reliability: alive
  fallback: true
  last_verified: 2026-06-27
  notes: 机器之心微信镜像；需双兜底；可考虑 RSSHub 备份

# === Tier 3 投资 / 市场视角（⚠️ 偏 VC / 仅事件锁集）===

- name: a16z-news-content
  tier: 3
  perspective: investor
  bias: VC
  fetch_method: webfetch
  url: https://a16z.com/news-content/
  reliability: alive
  fallback: true
  last_verified: 2026-06-27
  notes: 经典 a16z RSS feed/ 已死约 2 年（见 blacklist.md）；此 URL 是替代 webfetch 路径；强 VC 叙事偏向，filter 阶段需对"AI 必将颠覆一切"类口号格外严格

- name: state-of-ai
  tier: 3
  perspective: investor
  fetch_method: webfetch
  url: https://www.stateof.ai
  reliability: alive
  fallback: true
  last_verified: 2026-06-27
  notes: 年度 State of AI Report 锚点（每年约 10 月发布 PDF/Slides）。本体系仅检测引页面是否更新（fetcher 看 "Read the report" / 最新年份链接），不解析 PDF。平日 entry_count 通常 0；发布日才有 1 条"YYYY State of AI Report" 条目
```

---

## 字段含义

| 字段 | 取值 | 说明 |
|---|---|---|
| `name` | kebab-case 唯一 | fetcher subagent 接收此参数；vault frontmatter `source:` 字段引用此值 |
| `tier` | 1 / 2 / 3 | 1=一手+学术、2=聚合分析、3=降级 webfetch |
| `perspective` | research / product / investor | 视角偏向，用于 filter / cluster |
| `fetch_method` | rss / api / webfetch | 路由到 news-fetcher-{rss,api,webfetch} subagent |
| `url` | 完整 URL | scripts/source-health.sh 用 grep `^\s+url:` 抽取 |
| `reliability` | alive / degraded / dead | dead 不抓；degraded 仍抓但 filter 阶段加权降低 |
| `fallback` | true（可省） | 仅 tier 3 标，提示 fetcher 用更宽容的解析策略 |
| `last_verified` | YYYY-MM-DD | skill Phase 0 比对今天，> 30 天打 stale 警告 |
| `notes` | 自由文本 | 抓取注意事项 |

---

## 变更约定

- **新增源**：先用 WebFetch 试抓 → 若返回结构化内容，append 到对应 tier 段
- **降级源**：把 `reliability` 从 `alive` 改 `degraded`；连续 2 次跑全失败再考虑 `dead` 或移入 [blacklist.md](blacklist.md)
- **拉黑**：从本文件删 + 写入 blacklist.md（含失效日期与原因），防止未来"想当然"加回
