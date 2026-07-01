---
created: 2026-07-01 09:25:00
updated: 2026-07-01 09:25:00
status: draft
source: arxiv-api
source_url: http://arxiv.org/abs/2606.30573v1
topic: agents
tags: [paper, agent, eval, coding]
---

## 概念 / 事件

SWE-Interact：将 SWE 基准重构为用户驱动的长时程编码会话——用户模拟器从模糊指令出发、渐进披露需求、检查工作区并提供反馈。最强模型（Opus 4.8、GPT 5.5）在单轮任务约 50% 成功率但在 SWE-Interact 上仅 25%——揭示交互能力与自主能力的正交性。

## 关键洞察

- 单轮性能不预测多轮：最强模型的性能折半，说明"发现用户意图 + 适应变化需求"是独立能力轴，当前 SOTA 未覆盖
- 最强模型的主要失败模式是"过度 agentic 编码"（忘记需求、技术失误），而非无法生成代码——"行动节制"比"行动能力"更缺乏
- 与 SWE-Together（[[202607010926-swe-together-coding-agents]]）同期出现，多轮交互式编码基准成为 2026 年 agent 评测新前沿

## 来源

- [原文](http://arxiv.org/abs/2606.30573v1) — `arxiv-api`

## 关联

- [[agents]]
- [[202607010926-swe-together-coding-agents]]
- [[202607010927-agentic-abstention-convolve]]
