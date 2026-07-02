---
id: 2026-07-02-0901-evolution-fine-tuning-learning-to-discover
type: source-original
title: '演化微调：跨 371 个优化任务学习发现'
original_title: 'Evolution Fine-Tuning: Learning to Discover Across 371 Optimization Tasks'
source_name: huggingface-daily-papers
source_url: https://huggingface.co/papers/2606.29082
author: []
published_at: 2026-07-01
fetched_at: 2026-07-02T09:11:59+08:00
language: en
translated: true
translation_engine: haiku
word_count: 603
images_attempted: 25
images_saved: 25
fallback_notice: null
related_daily: 2026-07-02
related_zettels: []
related_topics: []
tags: [source-original, language-en]
---

# 演化微调：跨 371 个优化任务学习发现

> 原文：[Evolution Fine-Tuning: Learning to Discover Across 371 Optimization Tasks](https://huggingface.co/papers/2606.29082) · huggingface-daily-papers · 2026-07-01
> 抓取：2026-07-02T09:11:59+08:00 · 翻译：haiku · 603 字

## 概述

这项研究介绍了演化微调（EFT），一种训练方法，使较小的语言模型能够通过学习进化搜索轨迹来内化发现能力。与其依赖每个新问题的外部支架不同，这些模型获得可重用的优化策略。

## 主要贡献

**数据集创建**：研究人员构建了芬奇收藏（Finch Collection），包含约 156,000 条进化轨迹，跨越 10 个域和 371 个优化任务。他们使用 OpenEvolve 支架和 Qwen3.5-397B 作为教师模型收集这些轨迹。

**模型开发**：该团队在改进轨迹上微调开源模型（2B 到 9B 参数），创建了芬奇模型系列。这种方法通过将能力从昂贵的专有模型转移到更小的开源替代品，实现了发现民主化。

**跨任务泛化**：芬奇相比基础模型在保留任务上表现出"平均 10.22% 的改进"，更大的模型显示出更大的收益。当与测试时强化学习相结合时，这些模型在圆形堆积问题上达到了最先进的性能。

## 技术方法

该方法将优化搜索运行视为监督信号。与先前的方法每次都从头开始解决问题不同，EFT 将要修改的解决方案部分和何时回溯的决策直接编码到模型参数中。轨迹过滤过程通过删除系统错误、不可恢复的情况和过长序列，保留了 172,997 条原始轨迹中的 156,731 条。

## 实际影响

这项研究表明"扩展训练任务的数量可改善跨任务发现转移"，当从 15 个扩展到 355 个训练任务时，性能提升 14.1%。模型表现出涌现行为，结合来自多个域的策略来解决陌生问题。
