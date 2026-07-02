---
created: 2026-07-02 09:39:00
status: draft
source: huggingface-daily-papers
source_url: https://huggingface.co/papers/2606.26968
topic: safety-alignment
tags: [safety, paper, eval]
---

## 概念 / 事件
RedVox 是首个覆盖英/法/意/西/德五语种、3414 条音频的语音模型安全与公平性基准，揭示当前语音模型的多语言安全评估近乎空白（38 个模型仅 8% 报告过任何多语言分析）。

## 关键洞察
- 漏洞随语言与模态双重放大：非英语请求不安全响应率是英语的两倍（10.0% vs 5.1%），语音输入本身比纯文本提示的不安全响应率高出最多 20 个百分点，开源权重模型（如 Voxtral）不安全响应率达约 25%（专有模型 ≤3.1%）
- 用 GPT-5.5 做自动评估器，相对人工标注的宏观 F1 达 0.94，为语音安全评测的自动化提供了可信基准
- 首次系统记录"基于语音的红队测试"对参与者的心理影响：61.5% 参与者在发布含有害内容的语音时感到不适，56.4% 认为"说出来"比"写出来"承担更大个人责任——语音红队存在文本红队没有的伦理新维度

## 来源
- [[2026-07-02-0901-redvox-safety-fairness-gaps-speech-models]]
- [原文外链](https://huggingface.co/papers/2606.26968) — `huggingface-daily-papers`

## 关联
- [[safety-alignment]]
- [[202606291413-singguard-multimodal-guardrail]]
