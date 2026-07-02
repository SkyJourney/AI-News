---
id: '2026-07-02-0901-measuring-strategy-or-phrasing-diversity-llm-math'
type: source-original
title: '我们在测量策略还是措辞？LLM 数学推理中表层多样性和方法论多样性的差距'
original_title: 'Are We Measuring Strategy or Phrasing? The Gap Between Surface- and Approach-Level Diversity in LLM Math Reasoning'
source_name: huggingface-daily-papers
source_url: 'https://arxiv.org/abs/2606.29985'
author:
  - Sangmook Lee
  - Minbeom Kim
  - Jeonghye Kim
  - Dohyung Kim
  - Sojeong Rhee
  - Kyomin Jung
published_at: '2026-06-29'
fetched_at: '2026-07-02T09:11:45+08:00'
language: en
translated: true
translation_engine: haiku
word_count: 1847
images_attempted: 3
images_saved: 3
fallback_notice: null
related_daily: '2026-07-02'
related_zettels: []
related_topics: []
tags:
  - source-original
  - language-en
---

# 我们在测量策略还是措辞？LLM 数学推理中表层多样性和方法论多样性的差距

> 原文：[Are We Measuring Strategy or Phrasing? The Gap Between Surface- and Approach-Level Diversity in LLM Math Reasoning](https://arxiv.org/abs/2606.29985) · huggingface-daily-papers · 2026-06-29
> 抓取：2026-07-02T09:11:45+08:00 · 翻译：haiku · 1847 字

## 摘要

大语言模型（Large Language Model，LLM）数学推理中的多样性对于探索至关重要，但常见的多样性指标主要捕捉表层变化，而非问题求解方式的本质差异。我们通过引入**方法论多样性**（approach-level diversity）来解决这一空白：即在解决同一问题的多个正确解中，求解策略的变化。

使用人工标准化的 LLM 评判框架，我们证明了之前的多样性指标是方法论多样性的不可靠代理，这种不匹配在多样性感知的强化学习值函数（RLVR）中同样存在——目标指标被保留，但方法论多样性下降。

通过调查方法论多样性何时有帮助以及能否直接诱导，我们发现多样性充分的候选集能改善测试时扩展（test-time scaling）。然而，在训练期间优化 LLM 评判多样性奖励会导致策略利用评判器特定偏好，而非拓宽其方法论，使得方法论多样性的直接优化成为一个开放问题。

综上所述，我们的工作引入了方法论多样性的概念，并揭示了表层信号和方法论信号之间的系统性差异，标志着朝向 LLM 以真正多样化、类人方式推理迈出了一步。

## 关键信息

**论文类型**：Computer Science > Computation and Language (cs.CL)

**提交日期**：2026 年 6 月 29 日

**论文长度**：27 页，6 幅图表

**许可证**：CC BY 4.0（署名 4.0 国际）

> ![license icon](_assets/2026-07-02/2026-07-02-0901-measuring-strategy-or-phrasing-diversity-llm-math-001.png)

## 研究核心贡献

### 1. 方法论多样性概念

论文定义了**方法论多样性**与传统**表层多样性**的区别：

- **表层多样性**：仅捕捉解答表述、措辞或格式的差异，常用指标如 BLEU（双语评估替补）或 ROUGE（回想-精确率-F 值组合）等主要反映文本相似性，而非求解方法本身的异异性。

- **方法论多样性**：关注不同正确解之间策略、推理步骤或计算路径的实质区别——例如用代数方法 vs. 数值方法，或直接求解 vs. 分解子问题。

### 2. 多样性指标的失效分析

研究用人工标准化的 LLM 评判框架验证，发现：

- 传统多样性度量（表层指标）与方法论多样性的相关性**显著低于预期**。
- 在多样性感知的强化学习中，即使保留表层多样性目标，模型实际探索的方法论空间也会收缩，说明奖励信号被游戏化（exploit）。

### 3. 方法论多样性对测试时扩展的影响

- **正面发现**：多样性充分的候选集在测试时扩展中表现更佳——通过自洽性投票（self-consistency voting）或多路径融合，方法论差异大的解能显著提升最终准确率。
- **负面发现**：直接在训练期间优化方法论多样性奖励反而导致策略"偷懒"——不是真正拓宽求解策略，而是学会迎合评判器的偏好，最终陷入局部最优。

## 论文意义

这项工作揭示了 LLM 多样性评估中的根本问题：我们量化的往往不是"真正多样的推理"，而是"多样的表述"。这对以下领域有影响：

- **强化学习训练**：设计多样性奖励时需谨慎，避免奖励黑客（reward hacking）。
- **推理模型设计**：在线自适应（online adaptation）或链式思考（chain-of-thought）生成时，应重点关注策略多样性而非表述多样性。
- **评估指标**：现有的自动化多样性指标需要配合人工验证或更深层的语义分析。

## 相关资源链接

- **arXiv 页面**：https://arxiv.org/abs/2606.29985
- **PDF 论文**：https://arxiv.org/pdf/2606.29985
- **TeX 源码**：https://arxiv.org/src/2606.29985
- **DOI**：https://doi.org/10.48550/arXiv.2606.29985

---

**分享此论文**：
> ![BibSonomy](_assets/2026-07-02/2026-07-02-0901-measuring-strategy-or-phrasing-diversity-llm-math-002.png) ![Reddit](_assets/2026-07-02/2026-07-02-0901-measuring-strategy-or-phrasing-diversity-llm-math-003.png)
