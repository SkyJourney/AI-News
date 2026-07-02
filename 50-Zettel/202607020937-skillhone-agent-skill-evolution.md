---
created: 2026-07-02 09:37:00
status: draft
title: 'SkillHone：基于决策历史的 Agent 技能持续演进框架'
title_original: 'SkillHone：通过持久决策历史实现持续智能体技能演进的框架'
source: huggingface-daily-papers
source_url: https://huggingface.co/papers/2606.08671
topic: agents
tags: [agent, paper, opensource]
---

## 概念 / 事件
SkillHone 提出用"持久决策历史"取代"仅保留最终工件"的智能体技能演进范式：记录每次技能修订背后的诊断、候选方案、评估证据与结果，让后续 Agent 无需重新推导即可继续优化技能。

## 关键洞察
- 角色分离架构：优化子智能体只能写技能库、看不到未编辑的探针/验证器；评估子智能体只能跑候选技能、返回"编辑后的"证据报告——防止评估目标被直接记忆
- 深度研究基准 GAIA/WebWalkerQA-EN 上分别以 15.8/3.2 个百分点超越商业深度研究 Agent（且不依赖预集成搜索栈）；消融显示"决策历史"贡献（-13.4/-10.9pp）远大于"角色分离"贡献（-6.4/-5.3pp）
- 技能包可无额外优化直接迁移到不同执行主干（Claude Sonnet 4.6 上 GAIA 达 72.4%），说明增益来自技能程序本身而非对单一模型的过拟合，为 Agent 技能资产的可迁移性提供实证

## 来源
- [[2026-07-02-0901-skillhone-continual-agent-skill-evolution]]
- [原文外链](https://huggingface.co/papers/2606.08671) — `huggingface-daily-papers`

## 关联
- [[agents]]
