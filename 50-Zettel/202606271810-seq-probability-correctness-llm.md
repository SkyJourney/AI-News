---
created: 2026-06-27T18:10:00+08:00
status: draft
source: arxiv-api
source_url: http://arxiv.org/abs/2606.27359v1
topic: research-papers-llm
tags: [decoding, llm, correctness, probability]
---

## 概念 / 事件

研究量化了 LLM 解码中序列概率与答案正确性的关系，跨多种解码方法验证：高概率序列不等于正确答案。

## 关键洞察

- "高置信度 ≠ 高准确率" 被跨解码方法量化，根本上质疑了"用概率过滤输出"的主流做法
- 该发现对自洽性（Self-Consistency）、Best-of-N 等依赖序列概率的方法有直接否定含义
- 研究跨解码方法（beam search、greedy、sampling 等）验证，结论稳健性高

## 来源

- [论文](http://arxiv.org/abs/2606.27359v1) — `arxiv-api`

## 关联

- [[research-papers-llm]]
