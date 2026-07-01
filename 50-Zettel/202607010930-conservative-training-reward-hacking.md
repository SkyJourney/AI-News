---
created: 2026-07-01 09:30:00
updated: 2026-07-01 09:30:00
status: draft
source: arxiv-api
source_url: http://arxiv.org/abs/2606.30627v1
topic: safety-alignment
tags: [paper, safety, rlhf, llm, training]
---

## 概念 / 事件

悲观主义悖论：DPO 离线保守训练（高 β）越保守，在线适应阶段奖励黑客（reward hacking）损害越大——Spearman ρ=1.0 的单调关系，机制：高 β 压缩策略熵 → 响应多样性减少 → 奖励模型集成不确定性反增 → 在线优化加速利用漏洞。

## 关键洞察

- "保守训练 = 更安全"的直觉被证伪：适度（calibrated）而非最大化保守主义是最优策略，存在可量化的 β*
- 三链因果（熵压缩 → 多样性下降 → 不确定性增加）提供了可解释的机制，不只是经验相关
- 对当前对齐实践有直接影响：最保守的 DPO 设置可能在 RLHF 阶段制造最脆弱的奖励模型利用窗口

## 来源

- [原文](http://arxiv.org/abs/2606.30627v1) — `arxiv-api`

## 关联

- [[safety-alignment]]
- [[202607010927-agentic-abstention-convolve]]
