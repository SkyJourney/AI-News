---
id: 2026-07-02-0901-multi-block-diffusion-language-models
type: source-original
title: 多块扩散语言模型
original_title: Multi-Block Diffusion Language Models
source_name: huggingface-daily-papers
source_url: https://huggingface.co/papers/2606.29215
author: [Yijie Jin, Jiajun Xu, Yuxuan Liu, Chenkai Xu, Yi Tu, Jiajun Li, Dandan Tu, Xiaohui Yan, Kai Yu, Pengfei Liu, Zhijie Deng]
published_at: 2026-06-30
fetched_at: 2026-07-02T09:01:00+08:00
language: en
translated: true
translation_engine: haiku
word_count: 1360
images_attempted: 0
images_saved: 0
fallback_notice: '脚本输出 HTML 质量低（前端组件）；WebFetch 兜底成功'
related_daily: 2026-07-02
related_zettels: []
related_topics: []
tags: [source-original, language-en]
---

# 多块扩散语言模型

> 原文：[Multi-Block Diffusion Language Models](https://huggingface.co/papers/2606.29215) · huggingface-daily-papers · 2026-06-30
> 抓取：2026-07-02T09:01:00+08:00 · 翻译：haiku · 1360 字

## 摘要

块扩散语言模型（Block Diffusion Language Models）通过 KV 缓存和灵活长度生成增强文本生成。本工作将单块扩散扩展到多块扩散，实现连续块集的并发解码，以实现块间并行性。然而，现有模型在教师强制（teacher forcing）下训练，仅观察单个噪声块，这与实际多块操作产生训练推理不匹配。

作者提出 **多块教师强制（MultiTF）**，一种后训练方法，通过有界噪声组和随机噪声调度器将模型与多块推理状态对齐。他们引入了优化的块缓冲推理机制，保留前缀缓存重用和静态输入形状以用于 CUDA Graph 执行。

## 关键结果

**性能提升：**

- MBD-LLaDA2-Mini 将每次前向传递的令牌数（Tokens Per Forward pass）从 3.47 增加到 6.19（+78.4%）
- 平均准确度从 79.95% 提升至 81.03%
- 与 DMax 增强相结合时：9.34 TPF，仅精度下降 1.02%
- 实现吞吐量：951.41 TPS vs 基线 781.50 TPS

## 方法论

### 多块扩散（MultiBD）

MultiBD 通过维持"并发解码的连续块的运行集"而非顺序解码，推广了块级自回归生成。这在保留 KV 缓存优势的同时暴露块间并行性。

### 多块教师强制（MultiTF）

核心创新解决训练推理错配。MultiTF 构造：

1. **噪声组布局**：系统性移位布局涵盖所有有界运行集，加上随机布局实现分布多样性
2. **链均匀调度器**：随机每组噪声分配，创建更大的位槽噪声差距，匹配推理条件
3. **组感知双流掩码**：启用组内可见性同时防止信息泄漏

### 块缓冲机制

固定大小缓冲保留静态张量形状以实现 CUDA Graph 捕获，同时：

- 保持逻辑运行集语义
- 支持解码存储重叠
- 保留前缀缓存重用
- 启用四态槽转换：虚拟→活跃→待缓存→在缓存中

## 理论贡献

附录 A 提供覆盖分析，展示系统移位保证表示所有连续运行集直至最大大小的表示，目标不匹配由运行集和噪声比分布散度界定。

## 实验验证

在数学（GSM8K、MATH500）和代码（MBPP+、HumanEval+）基准上评估了 LLaDA2 和 SDAR 模型族。消融研究确认布局来源和链均匀调度对于在改善并行性的同时保持准确度都是必要的。
