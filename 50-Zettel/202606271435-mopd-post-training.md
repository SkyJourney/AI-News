---
created: 2026-06-27 14:35:00
status: draft
title: '多教师在线蒸馏 MOPD：后训练新范式'
source: interconnects
source_url: https://www.interconnects.ai/p/frontier-post-training-recipe-review
topic: research-papers
tags: [llm, training, paper, rlhf]
---

## 概念 / 事件

多教师在线蒸馏（Multi-teacher On-Policy Distillation，MOPD）——前沿模型 post-training 的新范式，解决单一教师蒸馏的分布漂移问题。

## 关键洞察

- MOPD 将多个教师模型的信号在 on-policy 条件下联合蒸馏，避免了 off-policy 蒸馏导致的分布偏移积累
- Interconnects 综述将 MOPD 纳入"前沿 post-training 菜谱"，说明该方法已被头部实验室实际采用
- 与传统 RLHF 相比，MOPD 降低了对单一奖励模型质量的依赖，提升 post-training 鲁棒性

## 来源

- [原文](https://www.interconnects.ai/p/frontier-post-training-recipe-review) — `interconnects`

## 关联

- [[research-papers]]
- [[202606271434-import-ai-461-alignment-not-on-track]]
