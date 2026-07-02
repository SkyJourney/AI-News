---
created: 2026-07-01 09:18:00
updated: 2026-07-01 09:18:00
status: draft
title: 'Beyond IID 基准戳破表格基础模型泛化神话'
source: huggingface-daily-papers
source_url: https://huggingface.co/papers/2606.30410
topic: research-papers
tags: [paper, eval, llm]
---

## 概念 / 事件

Beyond IID 基准（36 赞）：全面评测表格基础模型，发现其在小规模 IID 数据上表现卓越，但在复杂真实数据集上泛化能力严重不足——挑战"表格 FM 可通用"的市场叙事。

## 关键洞察

- "小 IID 优秀、复杂分布失败"的分裂性能揭示：当前表格基础模型本质上仍是高效的 in-distribution 学习器，而非真正通用的推理器
- 此评测 timing 精准：正值各公司开始将表格 FM 推向企业数据分析场景，打击"开箱即用"期待
- 与 GeneBench-Pro 同步出现，说明 AI 各垂直领域都在从"demo 竞争"向"严格基准竞争"转型

## 来源

- [原文](https://huggingface.co/papers/2606.30410) — `huggingface-daily-papers`

## 关联

- [[research-papers]]
- [[202607010915-genebench-pro-genomics-benchmark]]
