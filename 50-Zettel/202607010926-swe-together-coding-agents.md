---
created: 2026-07-01 09:26:00
updated: 2026-07-01 09:26:00
status: draft
source: huggingface-daily-papers
source_url: https://huggingface.co/papers/2606.29957
topic: agents
tags: [paper, agent, eval, coding]
---

## 概念 / 事件

SWE-Together（11 赞）：基于真实编码会话的多轮基准，使用响应式用户模拟器评估 Agent 协作能力——与 SWE-Interact 互补，同样揭示 Agent 在真实交互场景下的能力缺口。

## 关键洞察

- "真实编码会话"数据来源是差异点：SWE-Together 的用户模拟器行为基于对人类开发者真实交互模式的研究，而非人工设计场景
- 响应式（reactive）模拟器与渐进披露模拟器的差异：前者测试 Agent 处理随机反馈的鲁棒性，后者测试需求发现能力
- 两个独立团队同期发布多轮编码基准，说明学界已形成共识：单轮 SWE-bench 不足以衡量真实开发者场景下的 Agent 价值

## 来源

- [原文](https://huggingface.co/papers/2606.29957) — `huggingface-daily-papers`

## 关联

- [[agents]]
- [[202607010925-swe-interact-coding-benchmark]]
