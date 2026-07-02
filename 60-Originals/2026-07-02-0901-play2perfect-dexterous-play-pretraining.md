---
id: 2026-07-02-0901-play2perfect-dexterous-play-pretraining
type: source-original
title: 'Play2Perfect：灵巧操作中预训练游戏阶段对精密装配的影响因素研究'
original_title: 'Play2Perfect: What Matters in Dexterous Play Pretraining for Precise Assembly?'
source_name: huggingface-daily-papers
source_url: https://huggingface.co/papers/2606.26428
author: ["Tyler Ga Wei Lum", "Kushal Kedia", "C. Karen Liu", "Jeannette Bohg"]
published_at: 2026-06-23
fetched_at: 2026-07-02T09:13:18+08:00
language: en
translated: true
translation_engine: haiku
word_count: 1247
images_attempted: 21
images_saved: 21
fallback_notice: null
related_daily: 2026-07-02
related_zettels: []
related_topics: []
tags: [source-original, language-en]
---

# Play2Perfect：灵巧操作中预训练游戏阶段对精密装配的影响因素研究

> 原文：[Play2Perfect: What Matters in Dexterous Play Pretraining for Precise Assembly?](https://huggingface.co/papers/2606.26428) · huggingface-daily-papers · 2026-06-23
> 抓取：2026-07-02T09:13:18+08:00 · 翻译：haiku · 1247 字

## 研究概览

Play2Perfect 是一个强化学习框架，通过在多样化对象上进行无任务约束的预训练游戏阶段，实现样本高效的机器人精密装配任务。该方法首先让机器人学习通用的操作技能，然后通过微调适应精密装配任务。

### 核心问题与挑战

多指机器人承诺具有人手的速度和灵巧性，但精密装配这样的挑战性问题仍未被有效解决。这类任务具有以下特征：

1. **接触丰富（Contact-Rich）**：需要精确的接触交互，使得模仿学习的数据收集变得困难
2. **稀疏奖励（Sparse-Reward）**：由于奖励信号稀缺，直接的强化学习探索变得棘手
3. **环境复杂性**：以往工作通常通过特殊的夹具、工具附件和环境固定装置来简化问题

### Play2Perfect 框架核心思想

该论文提出的核心论点是：**在机器人能够完成精密装配之前，它必须首先学会"玩耍"**。

框架包含两个关键阶段：

**第一阶段：游戏预训练（Play Phase）**
- 目标：通过与多样化对象和目标的交互获得可复用的操作先验
- 学习内容：抓取、手内重定向、位姿到达等基础操作技能
- 特点：任务无关的自由探索

**第二阶段：精密装配微调（Perfect Phase）**
- 目标：将通用的操作先验适应到精密装配任务
- 焦点：最后的接触丰富、高精度交互
- 方法：有针对性的探索和精细调优

### 关键研究问题

论文系统性地研究了游戏预训练过程中的多个关键设计选择：

1. **对象多样性**：预训练中使用的对象种类的影响
2. **训练目标**：不同的学习目标函数如何影响最终性能
3. **轨迹多样性**：探索多样性对学习质量的影响
4. **目标精度**：游戏阶段中目标精度对装配精度的影响

### 关键研究成果

**样本效率改进**
- 相比从零开始的强化学习训练，即使在提供密集的多阶段奖励的情况下，Play2Perfect 方法的样本效率提高了 **33 倍**

**现实世界适用性**
- 实现了零样本 sim-to-real 转移（模拟到真实环境的直接转移）
- 在接触间隙仅为 0.5 毫米的紧插任务中实现了 **60% 的成功率**
- 在长地平线多部分装配和螺钉拧紧任务上达到了 **50% 以上的成功率**

### 技术意义

这项研究表明，通过将强化学习问题分解为两个阶段（通用预训练和特定微调），可以显著提高机器人操作的效率和性能。这种"先玩后专业化"的策略体现了一个重要的学习范式：获得广泛的基础技能对于后续的专业化应用至关重要。

### 社区反应

该论文在学术社区获得了广泛关注，HuggingFace Daily Papers 上的讨论中，研究者指出这一工作有望推进灵巧机器人操作领域的发展，特别是在实际应用中常见的精密装配场景。

## 相关资源

- **项目主页**：https://play2perfect.github.io/
- **GitHub 仓库**：https://github.com/kushal2000/play2perfect（13 stars）
- **论文链接**：https://arxiv.org/abs/2606.26428
- **PDF 版本**：https://arxiv.org/pdf/2606.26428

## 研究机构

本研究来自**斯坦福大学**（Stanford University），由多位顶级机器人研究者合作完成，属于当前机器人学习领域的前沿工作。
