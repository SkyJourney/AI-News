---
created: 2026-07-02 09:36:00
status: draft
title: 'Loop 世界模型论文登顶 HF，周鸿祎陆奇投资'
title_original: 'Loop世界模型论文登顶Hugging Face，来自中国一家初创，周鸿祎陆奇都投了'
source: qbitai
source_url: https://www.qbitai.com/2026/07/441225.html
topic: research-papers
tags: [paper, llm, reasoning]
---

## 概念 / 事件
中国初创"脸谱心智"（FaceMind）提出 Looped World Models（LoopWM），登顶 Hugging Face Papers 当日 Top1：用共享参数 Transformer 模块对同一潜在状态反复迭代细化，把"计算深度"变成可随任务复杂度动态调节的新扩展维度（iterative latent depth），而非只靠堆参数规模。

## 关键洞察
- 提出独立于模型规模和训练数据之外的第三条 scaling axis——迭代潜空间深度：简单场景少迭代、复杂场景多迭代，参数效率最高提升 100×，单步推理 FLOPs 最高减少约 25×，长时程 rollout 计算节省达两个数量级
- 在 ScienceWorld 基准上，LoopWM 用远小的参数量打平了参数量高出两个数量级的更大模型——证明"更会反复想"可以替代"更大"
- 与硅谷正热的 Loop Engineering（用循环系统替代手动 prompt）呼应但站位更深：Loop Engineering 解决"AI 怎么持续干活"，LoopWM 回答"AI 能否在持续干活时保持对世界的稳定理解"——是 Agent 认知层从执行系统向世界建模系统迈进的信号

## 来源
- [[2026-07-02-0901-loop世界模型论文登顶huggingface]]
- [原文外链](https://www.qbitai.com/2026/07/441225.html) — `qbitai`

## 关联
- [[research-papers]]
- [[202607020935-orca-world-foundation-model]]
- [[202607010923-worldevolver-self-evolving-agent]]
