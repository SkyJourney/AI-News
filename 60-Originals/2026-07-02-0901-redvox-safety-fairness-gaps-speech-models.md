---
id: 2026-07-02-0901-redvox-safety-fairness-gaps-speech-models
type: source-original
title: RedVox：跨语言语音模型的安全与公平性差距
original_title: 'RedVox: Safety and Fairness Gaps in Speech Models Across Languages'
source_name: huggingface-daily-papers
source_url: https://huggingface.co/papers/2606.26968
author: ["Beatrice Savoldi", "Sara Papi", "Wafa Aissa", "Matteo Negri", "Luisa Bentivogli"]
published_at: 2026-07-01
fetched_at: 2026-07-02T09:12:38+08:00
language: en
translated: true
translation_engine: haiku
word_count: 1442
images_attempted: 25
images_saved: 25
fallback_notice: null
related_daily: 2026-07-02
related_zettels: []
related_topics: []
tags: [source-original, language-en]
---

# RedVox：跨语言语音模型的安全与公平性差距

> 原文：[RedVox: Safety and Fairness Gaps in Speech Models Across Languages](https://huggingface.co/papers/2606.26968) · huggingface-daily-papers · 2026-07-01
> 抓取：2026-07-02T09:12:38+08:00 · 翻译：haiku · 1442 字

## 完整文章总结

### 标题与作者

**RedVox：跨语言语音模型的安全与公平性差距**

作者：Beatrice Savoldi、Sara Papi、Wafa Aissa、Matteo Negri、Luisa Bentivogli
Fondazione Bruno Kessler（意大利）

### 摘要

该研究检查了跨多种语言的语音模型中的安全漏洞。研究人员调查了 38 个语音模型，发现仅 8% 的模型报告了任何多语言分析。他们推出了 RedVox，一个涵盖五种语言（英语、法语、意大利语、西班牙语和德语）的多语言安全与公平性基准，包含 3,414 个音频条目，用于评估模型对不安全和刻板要求的响应。关键发现表明，漏洞在非英语语言中恶化，并且当请求来自语音输入时会被放大。

### 核心研究发现

**1. 安全文档差距**

对语音模型发布的审查发现，大多数模型缺乏多语言安全评估。在检查的 38 个模型中，仅 11 个记录了任何安全评估，且绝大多数关注英语。

**2. 关键漏洞识别**

- 专有模型显示不安全响应率 ≤3.1%
- 开源权重模型（如 Voxtral）在约 25% 的情况下产生有害响应
- 非英语请求的不安全响应率是英语的两倍（5.1% 对比 10.0%）

**3. 多模态漏洞**

语音输入被证明是最有问题的，有害响应率达到 10-44%。即使是非语音音频与有害文本配对也会增加不安全输出，相比仅文本提示增加高达 20%。

**4. 刻板印象处理**

刻板要求比明显不安全的内容以更高的速率触发争议响应，表明模型在处理微妙的偏见强化方面存在困难。

### 研究方法

**RedVox 数据集构建**

- 来自 7 个欧洲机构的 52 名研究人员提供数据
- 两种请求类型：语音（有害内容有声）和音频（有害文本加非语音音频）
- 建立在现有基准之上（SHADES 用于公平性，M-ALERT 用于安全性）
- 仅 50% 的参与者同意公开数据发布

**评估框架**

响应被分类为：

- 安全：模型明确劝阻有害活动
- 偶然安全：误解导致无害响应
- 有争议：取决于背景的有害性
- 不安全：模型认可或遵从有害请求

GPT-5.5 作为自动评估器，针对手动标注进行了验证，显示相关性上的宏观 F1 分数为 0.94。

### 参与者福祉发现

该研究记录了基于语音的红队测试中的独特挑战。调查结果显示：

- 61.5% 的参与者报告在发布包含有害内容的语音录音时感到不适
- 56.4% 的参与者在说出有害请求时相比写出有害请求时感到个人责任
- 43.6% 的参与者担心语音识别和去语境化
- 48.7% 的参与者请求语音匿名化技术

这些发现表明，语音研究提出了文本模态中不存在的独特个人和隐私问题。

### 评估的模型

**开源权重模型：**

- Qwen2-Audio、Qwen3-Omni
- Phi-4-Multimodal、Voxtral
- Gemma 4

**专有模型：**

- Gemini 3.1 Flash-Lite 和 Pro-Preview
- GPT-realtime-2

> 📷 **图 1**：论文相关图表
> 原图链接：https://cdn-uploads.huggingface.co/production/uploads/66309b3833ccd9e68c5d5171/IT5ZKeh3e_bQT_klgitnj.png

### 承认的局限

该研究专注于五种高资源的印欧语言，可能限制了对类型上不同或服务不足的语言的通用性。该研究检查了自然有害请求，而不是可能导致更高伤害率的蓄意越狱策略。此外，该工作未包括完全通过语音传递整个请求的条件。

### 伦理考虑

- 参与是自愿且无补偿的
- 为数据参与和公开发布获得了单独同意
- 限制每个参与者的数据分配，以最小化接触令人沮丧内容的情况
- 数据与直接参与者标识符脱钩
- 采用定制许可条款的门禁访问发布模式

### 意义

这项工作解决了语音模型多语言安全评估中的关键空白。该研究表明，漏洞甚至在自然条件下仍然存在，并在非英语语言中系统性地恶化——引发了关于跨语言社区公平 AI 开发和部署的重要问题。
