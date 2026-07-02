---
created: 2026-07-01 09:17:00
updated: 2026-07-01 09:17:00
status: draft
title: 'LeVo 2 歌曲生成逼近商用系统水准'
source: arxiv-api
source_url: http://arxiv.org/abs/2606.30642v1
topic: research-papers
tags: [paper, multimodal, training, release]
---

## 概念 / 事件

LeVo 2：混合 LLM-Diffusion 框架，通过层级建模（语义规划 → 音轨细化）+ 美学引导训练计划，实现稳定且富有音乐性的完整歌曲生成，在 6 个主观维度超越开源基线、逼近商用系统。

## 关键洞察

- "混合 token → LLM 语义规划 + 并行音轨预测 + Diffusion 波形重建"是三段拆解训练冲突的核心设计，解决了此前单一架构下音乐协调与声学细节的不可兼得
- 美学引导预训练 + 渐进式后训练（SFT → 离线 DPO → 半在线 DPO）说明音乐生成已进入"RLHF 化"阶段
- 歌曲生成进入商用对等区间，将加速 AI 音乐工具商业化

## 来源

- [原文](http://arxiv.org/abs/2606.30642v1) — `arxiv-api`

## 关联

- [[research-papers]]
- [[model-releases]]
