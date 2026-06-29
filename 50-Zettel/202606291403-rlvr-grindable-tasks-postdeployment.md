---
created: 2026-06-29 14:03:00
updated: 2026-06-29 14:03:00
status: draft
source: jiqizhixin
source_url: http://weixin.sogou.com/weixin?type=2&query=%E6%9C%BA%E5%99%A8%E4%B9%8B%E5%BF%83+Dwarkesh+Patel
topic: research-papers
tags: [llm, rl, training, agent]
---

## 概念 / 事件

Dwarkesh Patel 提出下一代 AI 训练范式转向：RLVR 需从"可验证任务"进化到"可磨性任务"，并倡导"发布后学习写回权重"——模型通过真实部署积累经验并持续更新。

## 关键洞察

- 首次出现概念"可磨性任务"（Grindable Tasks）：与"可验证任务"的区别在于不需要明确正确答案，而是通过持续打磨（反复迭代）来改进，扩展了 RLVR 可应用场景的边界
- 另一首次出现概念"发布后学习写回权重"：模型在部署中持续从用户交互中学习，将经验写回模型权重（区别于 RAG 或 fine-tune 的被动事后处理）
- 范式转向的核心诉求：从"发布前一次性训练"到"发布即训练起点"，将模型生命周期从阶段式变为连续式
- 对数据飞轮的影响：若该范式成立，部署规模越大的公司在训练数据积累上的优势将被进一步放大

## 来源

- [Dwarkesh Patel：下一代AI，可能是干活干出来的](http://weixin.sogou.com/weixin?type=2&query=%E6%9C%BA%E5%99%A8%E4%B9%8B%E5%BF%83+Dwarkesh+Patel) — `jiqizhixin`

## 关联

- [[research-papers]]
- [[202606291401-llm-sycophancy-rlhf]]（RLHF 奖励机制缺陷 → RLVR"可磨性"范式作为替代路径）
