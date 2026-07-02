---
id: 2026-07-02-0901-brain2qwerty-brain-ai-human-communication
type: source-original
title: '从脑电波到文字：Brain2Qwerty 提供无需手术的新型沟通方式'
original_title: 'From Brain Waves to Words: Brain2Qwerty Offers a New Path to Communication Without Surgery'
source_name: meta-ai-blog
source_url: https://ai.meta.com/blog/brain2qwerty-brain-ai-human-communication/
author: []
published_at: 2026-06-29
fetched_at: 2026-07-02T01:11:57+08:00
language: en
translated: true
translation_engine: haiku
word_count: 670
images_attempted: 0
images_saved: 0
fallback_notice: '脚本失败：Python 版本不兼容；WebFetch 兜底'
related_daily: 2026-07-02
related_zettels: []
related_topics: []
tags: [source-original, language-en]
---

# 从脑电波到文字：Brain2Qwerty 提供无需手术的新型沟通方式

> 原文：[From Brain Waves to Words: Brain2Qwerty Offers a New Path to Communication Without Surgery](https://ai.meta.com/blog/brain2qwerty-brain-ai-human-communication/) · meta-ai-blog · 2026-06-29
> 抓取：2026-07-02T01:11:57+08:00 · 翻译：haiku · 670 字

**发布时间**：2026 年 6 月 29 日 | **阅读时长**：3 分钟

## 概述

Meta 推出了 Brain2Qwerty v2，这是非侵入式脑计算机接口技术的一项重大进展。该系统能够将脑活动解码为文字，无需手术植入设备，代表了在为神经系统疾病患者恢复沟通能力方面的重大进展。

## 关键技术细节

该研究基于来自九名参与者约 22,000 个句子进行训练，每名参与者在打字时佩戴脑磁图（MEG）设备 10 小时。该团队没有采用传统信号检测方法，而是采用端到端深度学习直接解读原始神经信号。

该系统达到了 **61% 的单词准确率**，大幅超越"其他非侵入式方法的 8% 单词准确率"。对于表现最好的参与者，准确率达到了 78%，超过一半的解码句子错误率为一个单词以下。

## 技术方法

- 直接从原始脑信号解码的端到端深度学习管道
- 利用语义上下文的微调大型语言模型，以弥合嘈杂记录和连贯语言之间的差距
- 部署的 AI 代理优化解码配置

## 临床意义

该方法可能使数百万因脑损伤而无法交流的患者受益。与侵入式手术技术（立体脑电图、脑皮层脑电图）不同，这种非侵入式方法更具可扩展性，同时接近手术精度水平。

## 开放科学承诺

Meta 发布：

- v1 和 v2 的完整训练代码
- 来自巴斯克认知、脑和语言中心（BCBL）的数据集
- 与更广泛的基础模型的集成：Tribe v2、NeuralSet 和 NeuralBench

## 相关资源

- [Brain2Qwerty v2 论文](https://ai.meta.com/research/publications/accurate-decoding-of-natural-sentences-from-non-invasive-brain-recordings/)
- [代码库](https://github.com/facebookresearch/brain2qwerty)
- [数据集访问](https://huggingface.co/datasets/bcbl190626/SpanishBCBL)
