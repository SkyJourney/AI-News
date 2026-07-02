---
id: 2026-07-02-0901-improving-health-intelligence-in-chatgpt
type: source-original
title: ChatGPT 中健康智能的提升
original_title: Improving health intelligence in ChatGPT
source_name: openai-rss
source_url: https://openai.com/index/improving-health-intelligence-in-chatgpt
author: []
published_at: 2026-06-18
fetched_at: 2026-07-02T09:11:20+08:00
language: en
translated: true
translation_engine: haiku
word_count: 2006
images_attempted: 0
images_saved: 0
fallback_notice: 'direct http_403; jina ok'
related_daily: 2026-07-02
related_zettels: []
related_topics: []
tags: [source-original, language-en]
---

# ChatGPT 中健康智能的提升

> 原文：[Improving health intelligence in ChatGPT](https://openai.com/index/improving-health-intelligence-in-chatgpt) · openai-rss · 2026-06-18
> 抓取：2026-07-02T09:11:20+08:00 · 翻译：haiku · 2006 字

健康是人们使用 ChatGPT 最有意义的方式之一。每周有超过 2.3 亿人转向 ChatGPT 寻求健康和健康问题的帮助：理解健康信息、解读化验结果、准备医疗预约、了解保险、建立更健康的习惯，以及确定接下来该提什么问题。

通过 GPT-5.5 Instant（第五代 5.5 即时版本），我们在健康应用上取得了实质性进展，改进包括识别何时可能需要紧急护理、询问相关背景、解释不确定性以及使复杂信息更容易理解。在我们最具挑战性的健康评估中，GPT-5.5 Instant 现在的表现可与我们的前沿 Thinking 模型相媲美。由于它对所有 ChatGPT 免费用户可用，更多人能够从这些改进中受益。

这一进展既反映了模型能力的进步，也反映了我们背后医生主导的健康评估工作。在我们的各项工作中，来自全球的医生网络通过审视模型示例回应、描述理想行为以及识别失败模式来帮助定义在真实健康情境中"好"是什么样子。与医生合作让我们有办法衡量健康方面的进展，并随时间改进 ChatGPT 的回应方式。

## 衡量健康方面的进展

在健康领域，进展意味着提供准确、易于理解且基于良好判断的回应：认识到何时需要更多背景信息、在不过度自信的情况下解释不确定性，以及帮助人们了解何时应该寻求医疗。

为了衡量这一进展，我们使用了健康特定的评估，包括 [HealthBench](https://openai.com/index/healthbench/) 和 [HealthBench Professional](https://arxiv.org/pdf/2604.27470v1)。这些评估使用真实的健康对话和医生编写的评分标准来评估准确性、安全性、沟通、背景意识、完整性和适当的升级等特性。

_GPT-5.5 Instant 在健康评估汇总（包括 HealthBench Professional）上达到了与我们最新前沿模型相似的健康表现，从 GPT-5.3 Instant 有实质性改进。5.5 Instant（2026 年 5 月发布）和 5.3 Instant（2026 年 3 月发布）对所有 ChatGPT 免费用户可用（受限制），我们使用 API 定价来计算 5.4 Thinking 和 5.5 Thinking 的成本。_

作为另一个比较，我们让医生为代表性的健康对话写出回应，拥有无限时间和互联网访问（但没有 AI）。一个独立的医生团队随后在一段时间内比较了这些医生写的回应与模型回应，审视了在真实交互中重要的特性，包括准确性、沟通、完整性、指令遵循和健康决策有用性，审视了 3,500 条被审视的回应。

_GPT-5.5 Instant 的回应在这次评估中的各项标准上都被评为高于医生写的回应和较旧模型的回应。_

医生评估 GPT-5.5 Instant 的回应比旧模型和医生的回应有更少的失败模式。例如，GPT-5.5 Instant 在以下方面的失败实例比旧模型和医生都少：未根据当地医疗保健背景调整、遗漏危险信号或转诊到护理、或在需要时未能从用户那里寻求额外背景信息。

鉴于我们的模型在健康方面使用的规模，理解最近模型改进的另一种方式是测量生产流量。我们在生产流量上使用隐私保护监控来追踪健康回应中可能的事实性问题。基于最近生产流量中的健康对比——每周数十亿条消息——在过去两个月内，至少带有一个被标记为事实性问题的回应的比率下降了 71%。

## 更好的回应是什么样子

随时间推移比较模型在真实健康问题上的回应表明 ChatGPT 如何在对健康重要的方式上改进了：认识到某个情况可能需要紧急关注、以更好的判断处理不确定性，以及为人们提供关于接下来该做什么的更清晰、更有用的指导。

## 进展背后的医学专业知识

这一进展是由帮助我们定义、衡量和改进 ChatGPT 中健康回应的医生们塑造的。

OpenAI 与来自 60 个国家、49 种语言和 26 个医学专科的全球超过 260 名医生合作。他们的反馈指导 ChatGPT 如何在从日常健康问题到更复杂的临床情况的广泛场景中回应健康问题。

医生审视示例模型回应，并评估它们是否准确、清晰、完整、适当谨慎和有用。他们帮助识别回应可能遗漏重要背景的地方，它可能听起来太自信的地方，它应该对下一步更清楚的地方，或更直接地鼓励某人寻求医疗护理的地方。

迄今为止，医生已审视了超过 700,000 个示例模型回应，这些回应反映了患者和临床医生在现实世界中如何使用 ChatGPT。每几分钟就有一名医生审视一条新的回应。他们的反馈变成了评分标准和评估标准，帮助研究人员衡量回应在真实健康情境中是否准确、安全、清晰、完整、适当谨慎和有用。这给了我们一个更清晰的方式来看模型在哪些方面改进了以及它们在哪些方面仍需要工作。

## 将健康改进带给更多人

这项工作也支持 OpenAI 更广泛的健康工作，包括为医疗保健构建的工具，如 [ChatGPT for Clinicians](https://openai.com/index/making-chatgpt-better-for-clinicians/) 和 [OpenAI for Healthcare](https://openai.com/index/openai-for-healthcare/)，这些工具通过文档、研究和护理交付等任务支持医疗专业人士。

改善人类健康将是 AGI（通用人工智能）最个人化、最具体的影响之一。随着我们的模型继续改进，我们的目标是使 ChatGPT 在那些时刻更准确、更有用和更有影响力——并继续将这一进展带给更多人。
