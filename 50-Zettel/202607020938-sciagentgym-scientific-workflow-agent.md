---
created: 2026-07-02 09:38:00
status: draft
source: jiqizhixin
source_url: http://weixin.sogou.com/weixin?type=2&query=%E6%9C%BA%E5%99%A8%E4%B9%8B%E5%BF%83+%E4%BB%8E%E7%AD%94%E9%A2%98%E5%88%B0%E5%81%9A%E5%AE%9E%E9%AA%8C%EF%BC%9ASciAgentGym%E8%AE%A9%E5%A4%A7%E6%A8%A1%E5%9E%8B%E8%BF%9B%E5%85%A5%E7%A7%91%E5%AD%A6%E5%B7%A5%E4%BD%9C%E6%B5%81
topic: agents
tags: [agent, eval, paper]
---

## 概念 / 事件
复旦大学 NLP 实验室提出 SciAgentGym，一个面向多步科学工具使用的智能体环境，配套 259 个任务的评测集 SciAgentBench，覆盖物理、化学、材料科学、生命科学四大领域，把大模型从"科学问答"推进到"科学实验工作流"。

## 关键洞察
- 评测集 SciAgentBench 强调类型安全、可复现性和可扩展性——针对科学场景中工具调用链路长、副作用不可逆（如实验操作）的特点专门设计
- 定位是"从答题到做实验"：区别于传统科学 QA 基准，SciAgentGym 要求 Agent 在多步骤、有状态的科学工作流环境中完成任务，更贴近真实科研辅助场景
- 抓取受限（微信生态搜索跳转页无法自动化解析），本条洞察基于摘要信息，具体实验数据与基线对比待后续人工核实原文

## 来源
- [[2026-07-02-0901-从答题到做实验-sciagentgym科学工作流]]
- [原文外链](http://weixin.sogou.com/weixin?type=2&query=%E6%9C%BA%E5%99%A8%E4%B9%8B%E5%BF%83+%E4%BB%8E%E7%AD%94%E9%A2%98%E5%88%B0%E5%81%9A%E5%AE%9E%E9%AA%8C%EF%BC%9ASciAgentGym%E8%AE%A9%E5%A4%A7%E6%A8%A1%E5%9E%8B%E8%BF%9B%E5%85%A5%E7%A7%91%E5%AD%A6%E5%B7%A5%E4%BD%9C%E6%B5%81) — `jiqizhixin`

## 关联
- [[agents]]
