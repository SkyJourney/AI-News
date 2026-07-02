---
id: 2026-07-02-0901-dataevolver-self-evolving-multi-agent-data
type: source-original
title: 'DataEvolver：用于文本丰富图像生成的自演进多智能体数据构造'
original_title: 'DataEvolver: Self-Evolving Multi-Agent Data Construction for Text-Rich Image Generation'
source_name: huggingface-daily-papers
source_url: 'https://huggingface.co/papers/2606.31537'
author: ["Siyu Yan", "Yizhen Gao", "Yilin Wang", "Dongxing Mao", "Alex Jinpeng Wang"]
published_at: 2026-06-30
fetched_at: 2026-07-02T09:14:21+08:00
language: en
translated: true
translation_engine: haiku
word_count: 399
images_attempted: 0
images_saved: 0
fallback_notice: 'fetch_channel: direct; 脚本成功抓取但 HTML 质量差，已用 WebFetch 兜底获得干净 Markdown'
related_daily: 2026-07-02
related_zettels: []
related_topics: []
tags: [source-original, language-en]
---

# DataEvolver：用于文本丰富图像生成的自演进多智能体数据构造

> 原文：[DataEvolver: Self-Evolving Multi-Agent Data Construction for Text-Rich Image Generation](https://huggingface.co/papers/2606.31537) · huggingface-daily-papers · 2026-06-30
> 抓取：2026-07-02T09:14:21+08:00 · 翻译：haiku · 399 字

## 概述

DataEvolver 解决了文本丰富图像生成中的一个根本挑战：现有数据管道采用静态的"爬取-过滤-冻结"方法，虽然被拒绝的样本包含诊断价值，但仍会被丢弃。本研究提出将数据构造视为一个迭代的反馈驱动的过程。

## 核心创新

框架不是将被拒绝的样本视为废料，而是将拒绝模式转化为可操作的指导。正如论文所述："被拒绝的样本可以为改进文本丰富图像数据构造提供可操作的反馈。"

## 四智能体架构

**检索器（Retriever）**：使用自适应的、由策略条件化的查询策略而非固定关键词来发现候选样本。

**验证器（Verifier）**：在图像质量、文本识别和语义一致性三个维度评估候选样本，同时对失败模式进行分类。

**评论员（Critic）**：将轮级拒绝统计综合为自然语言反馈，以修订检索查询和生成提示。

**生成器（Generator）**：通过有针对性的合成来覆盖未充分覆盖的语义区域，解决仅通过检索无法覆盖的长尾场景。

## 关键结果

在 0.75M 规模的 PixArt-α 模型上：
- TextScenesHQ：OCR-F1 相比最强基线提升 85.3%
- LongTextBench：提升 35.3%
- 效果可转移到 Show-o2，表明泛化性超越单个架构

## 区别特性

与之前优化模型输出的反馈驱动方法不同，DataEvolver 将反馈循环应用于数据构造过程本身。该框架完全在自然语言策略空间中运行，无需基于梯度的优化，使其具有模块化和可解释性。
