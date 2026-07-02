---
id: 2026-07-02-0901-blockpilot-instance-adaptive-policy-learning
type: source-original
title: 'BlockPilot：用于扩散式推理的实例自适应策略学习'
original_title: 'BlockPilot: Instance-Adaptive Policy Learning for Diffusion-based Speculative Decoding'
source_name: huggingface-daily-papers
source_url: https://huggingface.co/papers/2606.31315
author: []
published_at: 2026-06-29
fetched_at: 2026-07-02T01:11:55+00:00
language: en
translated: true
translation_engine: haiku
word_count: 1277
images_attempted: 0
images_saved: 0
fallback_notice: '脚本失败: Python 版本不兼容；WebFetch 兜底'
related_daily: 2026-07-02
related_zettels: []
related_topics: []
tags: [source-original, language-en]
---

# BlockPilot：用于扩散式推理的实例自适应策略学习

> 原文：[BlockPilot: Instance-Adaptive Policy Learning for Diffusion-based Speculative Decoding](https://huggingface.co/papers/2606.31315) · huggingface-daily-papers · 2026-06-29
> 抓取：2026-07-02T01:11:55+00:00 · 翻译：haiku · 1277 字

## 摘要

BlockPilot 是一种新颖方法，通过使块大小选择具有自适应性而非固定值来优化大语言模型推理效率。该研究发现"最优块大小在不同样本间有所不同"，并提出了一个轻量级预测器来确定针对扩散式推理的实例特定块大小。

## 主要发现

**可变最优块大小**：论文证明了不同输入样本从不同推理块大小中受益，与使用相同配置处理所有输入的现有固定块方法相反。

**局部结构性**："最优块大小在样本间表现出强局部性，最优解集中在训练块大小周围的狭窄区域内"，这使得可以进行高效预测而非耗费成本的搜索。

**分类表述**：问题不采用连续优化，而是简化为离散分类任务，从小候选集（如 {B-2, B-1, B, B+1, B+2}）中选择。

## 方法论

BlockPilot 使用"预填充阶段后最后一个令牌的预测概率分布"作为轻量级多层感知机的输入，该感知机预测最优块大小。此预测在预填充后每个样本发生一次，增加的开销最少。

## 结果

在 Qwen3-4B 上，BlockPilot 在温度 T=1 时实现了"5.92 的接受长度和 4.20 倍的加速"，超越了 DFlash 等固定块基准方法，同时只引入毫秒级延迟。
