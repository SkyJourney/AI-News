---
created: 2026-06-29 14:02:00
updated: 2026-06-29 14:02:00
status: draft
source: jiqizhixin
source_url: http://weixin.sogou.com/weixin?type=2&query=%E6%9C%BA%E5%99%A8%E4%B9%8B%E5%BF%83+ICML+2026+Oral
topic: research-papers
tags: [llm, paper, training, eval, interpretability]
---

## 概念 / 事件

ICML 2026 Oral 论文：北京大学 & 智源提出"机理数据归因"（Mechanistic Data Attribution）框架，追踪内部机制（如归纳头）的形成源头，发现驱动关键能力的并非高质量文本，而是 XML、LaTeX 等"垃圾数据"中的重复结构。

## 关键洞察

- 反直觉核心发现：关键能力（如归纳头）由结构重复的"低质量"数据驱动，而非人工筛选的高质量语料
- 新框架"机理数据归因"将数据集影响分析从黑盒输出层延伸至内部机制层，是 interpretability 与数据策略的交叉创新
- 实践含义：数据清洗策略若过度过滤 XML/LaTeX 类结构化数据，可能意外损伤模型的归纳推理能力
- ICML Oral 级别意味着该发现经过同行严格评审，可信度较高

## 来源

- [ICML 2026 Oral｜大模型的能力从哪些训练数据来？北大&智源提出「机理数据归因」](http://weixin.sogou.com/weixin?type=2&query=%E6%9C%BA%E5%99%A8%E4%B9%8B%E5%BF%83+ICML+2026+Oral) — `jiqizhixin`

## 关联

- [[research-papers]]
