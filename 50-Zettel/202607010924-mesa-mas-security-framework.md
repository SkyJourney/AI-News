---
created: 2026-07-01 09:24:00
updated: 2026-07-01 09:24:00
status: draft
title: 'MESA 框架：无需攻击样本评估多智能体安全风险'
source: arxiv-api
source_url: http://arxiv.org/abs/2606.30602v1
topic: agents
tags: [paper, agent, safety]
---

## 概念 / 事件

MESA 框架：无需攻击样本，用 6 个图论指标 + 2 个动态探针对多智能体系统（MAS）通信边进行安全风险排序，与实际攻击成功率的 Spearman 相关系数达 0.60（峰值 0.73）——监控排名前 10% 的边可拦截 3 倍于随机分配的攻击。

## 关键洞察

- MAS 攻击影响高度不均匀：单条边最高承担 75% 总攻击成功率——集中防御而非均匀防御是正确策略
- "无需攻击痕迹的主动风险排序"使 MESA 可在部署前运行，而非事后检测——将 MAS 安全从响应式转为主动式
- 在 9 个 LLM（7B-120B）上跨模型验证，6/9 分组 AUC=1.0，说明风险结构是 MAS 拓扑决定的，与底层 LLM 关系较弱

## 来源

- [原文](http://arxiv.org/abs/2606.30602v1) — `arxiv-api`

## 关联

- [[agents]]
- [[safety-alignment]]
