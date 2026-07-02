---
created: 2026-07-02 09:35:00
status: draft
source: huggingface-daily-papers
source_url: https://huggingface.co/papers/2606.30534
topic: research-papers
tags: [llm, paper, multimodal, opensource]
---

## 概念 / 事件
北京人工智能研究院提出 Orca，一个通用世界基础模型的初步实现：核心是用"下一状态预测"取代割裂的下一令牌/下一帧/下一动作预测，统一建模世界的状态转移。

## 关键洞察
- 双范式学习：无意识学习（从连续视频中学习自然密集的状态转移，无需标注）+ 有意识学习（语言条件下学习稀疏但有意义的状态转移），消融实验显示二者组合优于单独使用
- 预训练数据规模 125K 小时视频 + 1.6 亿条事件注释；下游用文本生成、图像预测、具身动作生成三类任务验证潜在空间有效性，骨干冻结、只训练轻量读出头
- 核心论点"更强的世界潜在空间 → 更强的下游读出"在三类任务上均随预训练规模一致提升，为"世界模型"提供了一条独立于单纯堆参数规模的扩展路线

## 来源
- [[2026-07-02-0901-orca-the-world-is-in-your-mind]]
- [原文外链](https://huggingface.co/papers/2606.30534) — `huggingface-daily-papers`

## 关联
- [[research-papers]]
- [[202607010923-worldevolver-self-evolving-agent]]
- [[202606300955-physisforcing-physics-world-model]]
