---
created: 2026-06-27 14:37:00
updated: 2026-07-01 09:31:00
entry_total: 10
---

# 基础设施 & 硬件 (infra-hardware)

追踪 GPU、专用 AI 芯片、数据中心、推理优化、训练成本等基础设施动态。

## 2026-06-27

- **OpenAI × Broadcom Jalapeño LLM inference chip** ([[202606271437-jalapeno-inference-chip]])
  OpenAI 与 Broadcom 联合推出 Jalapeño 专用推理芯片，首次公开自研硬件路线，摆脱 NVIDIA 依赖。
  源：`openai-rss`

- **DeepSeek V4 DSpark speculative decoding** ([[202606271438-dspark-speculative-decoding]])
  DSpark 投机解码实现 60–85% 推理提速，配套 DeepSpec 框架开源供社区复现。
  源：`jiqizhixin`

## 2026-06-28

- **OpenAI × Broadcom Jalapeño 推理芯片** ([[202606271437-jalapeno-inference-chip]])
  28 日批次延续，Jalapeño 自研芯片路线作为重大历史节点持续关注。
  源：`openai-rss`

- **DeepSeek V4 DSpark 投机解码** ([[202606271438-dspark-speculative-decoding]])
  Flash 提速 60–85% / Pro 提速 57–78% 的实测数据在 28 日批次再次出现。
  源：`jiqizhixin`

- **陈天奇《Modern GPU Programming For MLSys》书稿公开**（未升级 Zettel，低置信度）
  CMU 陈天奇免费在线书，主线 Blackwell 架构，案例含矩阵乘法 + FlashAttention。
  源：`jiqizhixin`

- **The Batch Issue 359: Apple 端侧模型配方 + GLM-5.2**（未升级 Zettel，低置信度）
  Andrew Ng 点评 Apple 端侧模型效率方案与 GLM-5.2 开放 agent 意义。
  源：`the-batch`

## 2026-07-01

- **异步 Pipeline 并行 LLM 预训练：一步梯度延迟不是瓶颈** ([[202607010919-async-pipeline-parallel-llm]])
  关键在优化器选择——Muon 对梯度延迟鲁棒，10B 参数验证与同步训练性能对齐，异步并行消除 GPU bubble 路径清晰。
  源：`arxiv-api`（同时：`huggingface-daily-papers` 19 赞）
- **中国信通院发布 AI Infra 运维首个评测基准** ([[202607010920-china-ai-infra-ops-benchmark]])
  覆盖五大国内芯片平台，AI 基础设施运维从"能跑"到"可量化"成熟度标志。
  源：`qbitai`
- **ElevenLabs：70 倍 GPU 效率提升——算力稀缺是工程问题** ([[202607010921-elevenlabs-gpu-efficiency-70x]])
  batching + FP8 + speculative decoding + KV-cache 压缩组合达到 140 用户/GPU，推理优化标准套件实测验证。
  源：`air-street-press`
