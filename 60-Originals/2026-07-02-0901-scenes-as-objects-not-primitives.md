---
id: 2026-07-02-0901-scenes-as-objects-not-primitives
type: source-original
title: '场景作为对象，而非原始元素：从未定位视图的实例结构化 3D 标记化'
original_title: 'Scenes as Objects, Not Primitives: Instance-Structured 3D Tokenization from Unposed Views'
source_name: huggingface-daily-papers
source_url: 'https://huggingface.co/papers/2606.29513'
author: ["Mijin Yoo", "In Cho", "Subin Jeon", "Jiwoo Lee", "Eunbyung Park", "Seon Joo Kim"]
published_at: 2026-06-28
fetched_at: 2026-07-02T09:15:00+08:00
language: en
translated: true
translation_engine: haiku
word_count: 1248
images_attempted: 0
images_saved: 0
fallback_notice: '脚本失败：无有效 HTML 提取；WebFetch 兜底成功'
related_daily: 2026-07-02
related_zettels: []
related_topics: []
tags: [source-original, language-en]
---

# 场景作为对象，而非原始元素：从未定位视图的实例结构化 3D 标记化

> 原文：[Scenes as Objects, Not Primitives: Instance-Structured 3D Tokenization from Unposed Views](https://huggingface.co/papers/2606.29513) · huggingface-daily-papers · 2026-06-28
> 抓取：2026-07-02T09:15:00+08:00 · 翻译：haiku · 1248 字

## 核心贡献

本文提出了一个前馈框架，将 3D 场景表示为"实例结构化标记组"，而非无组织的点云或高斯球体。关键创新在于将对象实例视为本地表示单元，而不是从原始元素后处理派生。

## 技术架构

该系统采用两级分解（two-level factorization）：

- **实例标记** 捕捉实体级别的身份和边界
- **锚标记** 编码局部几何与外观，解码为 3D 高斯球体

冻结的几何基础模型（VGGT）从多视图特征中提取，通过两个 transformer 阶段处理：一个图像-锚解码器和一个锚分组解码器，后者通过 softmax 竞争将锚分配给实例。

## 训练方法

该框架使用联合监督：RGB 图像通过锚标记监督重构质量，而实例掩码通过组标记监督分组。至关重要的是，不需要 3D 注解——仅使用基于 2D 渲染的监督。

## 关键结果

在 ScanNet 基准上，该模型在实例分割（AP：0.235）上的性能超过了逐场景优化方法。特征提升通过分解的组和锚级嵌入，大幅度将语义存储从 8.4M 标量减少至 59.4K。

## 下游应用

标记组直接支持以下能力：

- 实例级场景编辑（删除、插入、变换）
- 在实例尺度而非原始元素尺度上的高效开放词汇检索
- 无需后处理的连贯 3D 实例操作
