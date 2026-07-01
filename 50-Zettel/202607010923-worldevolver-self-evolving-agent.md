---
created: 2026-07-01 09:23:00
updated: 2026-07-01 09:23:00
status: draft
source: arxiv-api
source_url: http://arxiv.org/abs/2606.30639v1
topic: agents
tags: [paper, agent, rl, llm]
---

## 概念 / 事件

WorldEvolver：自演化世界模型框架，在不修改 Agent 参数和下游任务的前提下，通过情节记忆（检索模拟真实转换）、语义记忆（从预测误差中提炼启发规则）和选择性预见（过滤低置信预测）三模块持续修订部署时上下文。

## 关键洞察

- "只改上下文、不改参数"是关键约束：WorldEvolver 在测试时学习，绕开了 fine-tuning 成本，让世界模型像记忆一样演化
- 预测-观察不匹配触发语义记忆更新，形成"错了才学"的机制，比预设规则更具适应性
- 在 ALFWorld 和 ScienceWorld 上同时提升世界模型预测精度和下游 Agent 成功率，验证了"好的世界模型 = 更好的规划"的直觉

## 来源

- [原文](http://arxiv.org/abs/2606.30639v1) — `arxiv-api`

## 关联

- [[agents]]
- [[202607010927-agentic-abstention-convolve]]
