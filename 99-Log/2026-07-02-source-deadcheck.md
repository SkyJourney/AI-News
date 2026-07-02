---
created: 2026-07-02 09:01:17
---

# 死链报告 @ 2026-07-02

## dead 源

| source | url | status | 建议 |
|---|---|---|---|
| arxiv-api | http://export.arxiv.org/api/query | 301000（异常/超时） | 本次跑排除；下次跑前人工复验 export.arxiv.org 可达性，若连续失败考虑 reliability 改 degraded |

## stale 源（last_verified > 30 天）

无（所有源 last_verified 在 2026-06-27 ~ 2026-06-29 之间，距今 3-5 天）

## alive 源池（13 个，进入 Phase 1）

openai-rss, deepmind-rss, huggingface-daily-papers, import-ai, interconnects, qbitai, air-street-press, anthropic-news, meta-ai-blog, the-batch, jiqizhixin, a16z-news-content, state-of-ai
