---
created: 2026-06-27 14:35:00
updated: 2026-07-02 09:41:00
entry_total: 46
---

# 研究论文 (research-papers)

追踪 arXiv / HuggingFace Daily Papers / 顶会的学术论文，涵盖 LLM 训练方法、多模态、评测基准等。

## 2026-07-02

- **Orca: The World is in Your Mind** ([[202607020935-orca-world-foundation-model]])
  北京人工智能研究院提出统一世界基础模型，以 Next-State-Prediction 取代割裂的 next-token/frame/action 预测。
  源：`huggingface-daily-papers`（176 赞）
- **DOPD: Dual On-policy Distillation**（未升级 Zettel）
  双向在线蒸馏方法，解决"特权错觉"导致的能力差距误判问题。
  源：`huggingface-daily-papers`（75 赞）
- **BlockPilot: Instance-Adaptive Policy Learning for Diffusion-based Speculative Decoding**（未升级 Zettel）
  自适应 block 尺寸策略提升扩散式推测解码效率，替代固定推理 block 假设。
  源：`huggingface-daily-papers`（67 赞）
- **Scenes as Objects, Not Primitives**（未升级 Zettel）
  实例级 3D token 分组框架，从无姿态多视角图像直接输出对象中心结构化表示。
  源：`huggingface-daily-papers`（34 赞）
- **GEAR: Guided End-to-End AutoRegression for Image Synthesis**（未升级 Zettel）
  联合训练 VQ tokenizer 与自回归生成器，用表示对齐引导解决两阶段解耦缺陷。
  源：`huggingface-daily-papers`（28 赞）
- **Evolution Fine-Tuning**（未升级 Zettel）
  371 个优化任务上验证 LLM 进化式搜索经验的跨任务迁移能力。
  源：`huggingface-daily-papers`（23 赞）
- **Multi-Block Diffusion Language Models**（未升级 Zettel）
  从 Single-Block 扩展到 Multi-Block 扩散语言模型，解决 teacher forcing 下的块间并行问题。
  源：`huggingface-daily-papers`（22 赞）
- **MemLearner: Learning to Query Context Memory for Video World Models**（原文抓取超时，未升级 Zettel）
  视频世界模型记忆检索方法，应对场景遮挡与动态物体下的规则式记忆检索失效问题。
  源：[原文](https://huggingface.co/papers/2606.31734) — `huggingface-daily-papers`（18 赞）
- **PhotoQuilt: Training-Free Arbitrary-Resolution Photomosaics**（未升级 Zettel）
  无训练框架实现任意分辨率照片马赛克生成，解决扩散模型难以同时满足全局与局部细节的问题。
  源：`huggingface-daily-papers`（12 赞）
- **Little Brains, Big Feats: Exploring Compact Language Models**（未升级 Zettel）
  紧凑语言模型在 RAG 生成阶段的性能评估研究。
  源：`huggingface-daily-papers`（10 赞）
- **Are We Measuring Strategy or Phrasing?**（未升级 Zettel）
  提出"策略级多样性"概念，揭示现有 LLM 数学推理多样性指标多为表面变化而非真实策略差异。
  源：`huggingface-daily-papers`（10 赞）
- **Play2Perfect: Dexterous Play Pretraining for Precise Assembly**（未升级 Zettel）
  灵巧操作预训练研究，探索精确装配任务在接触密集、稀疏奖励场景下的可行路径。
  源：`huggingface-daily-papers`（10 赞）
- **Loop世界模型论文登顶Hugging Face** ([[202607020936-loop-world-model-paper]])
  中国初创脸谱心智提出 LoopWM，用迭代潜空间深度作新 scaling axis，登顶 HF Papers 当日 Top1。
  源：`qbitai`
- **Testing Mythos and Fable, Moving Beyond SWE-bench**（未升级 Zettel，复盘）
  The Batch 综述美国政府与 Anthropic 对前沿模型访问权的控制行动持续传播。
  源：`the-batch` · 首记于 [[2026-06-29]]
- **State of AI Report 2025** ([[202606291405-state-of-ai-report-2025]])（复盘）
  🔄 [复盘] 第八届年度 AI 状态报告持续被引用，覆盖研究/产业/政策/安全/使用趋势综合分析。
  源：`state-of-ai` · 首记于 [[2026-06-29]]
- **State of AI Report 2025 - Full Slide Deck**（未升级 Zettel，复盘）
  报告完整幻灯片版持续传播，作为主报告的配套引用材料。
  源：`state-of-ai` · 首记于 [[2026-06-29]]
- **2025 Report Launch Blog Post**（未升级 Zettel，复盘）
  报告发布博文延伸解读，聚焦 OpenAI 竞争地位、推理模型进展、科研加速等主题。
  源：`state-of-ai` · 首记于 [[2026-06-29]]
## 2026-07-01

- **GeneBench-Pro：AI 基因组学 & 生物学评测基准** ([[202607010915-genebench-pro-genomics-benchmark]])
  OpenAI 发布基于复杂真实世界数据集的生命科学评测基准，AI 科学能力竞争进入标准化评测阶段。
  源：`openai-rss`
- **VLK：合成场景学习人形机器人感知操作** ([[202607010916-vlk-humanoid-loco-manipulation]])
  3DGS 重建 + 合成 48k 轨迹无需人工标注，视觉-语言-运动学三模态在 Unitree G1 上完成 sim-to-real。
  源：`arxiv-api`
- **LeVo 2：层级 LLM-Diffusion 歌曲生成** ([[202607010917-levo2-song-generation]])
  语义规划 + 音轨细化 + 美学引导后训练，完整歌曲生成逼近商用系统水平。
  源：`arxiv-api`
- **Beyond IID：表格基础模型泛化能力基准** ([[202607010918-tabular-foundation-models-benchmark]])
  36 赞高关注论文揭示表格 FM 在复杂数据集上泛化严重不足，挑战"通用"叙事。
  源：`huggingface-daily-papers`
- **State of AI Report 2025** ([[202606291405-state-of-ai-report-2025]])（复盘）
  🔄 [复盘] 年度 AI 状态报告持续受关注，今日再次浮现。
  源：`state-of-ai` · 首记于 [[2026-06-29]]

## 2026-06-30

- **Introducing LifeSciBench** ([[202606300953-lifescibench-life-science-eval]])
  专家撰写的生命科学真实任务 AI 评测基准，从知识问答转向 task completion 评测范式。
  源：`openai-rss`
- **Predicting model behavior before release by simulating deployment** ([[202606300954-deployment-simulation-model-behavior]])
  OpenAI Deployment Simulation 利用真实对话数据在发布前预测模型行为分布。
  源：`openai-rss`
- **Adaptive Financial Transformer with Regime-Gated Attention for Stock Return Prediction**（未升级 Zettel）
  金融预测 Transformer 模型，arXiv 2606.29347。
  源：`arxiv-api`
- **Reliability, Faithfulness, and the Limits of Post-hoc Explanations of Opaque Scientific Models**（未升级 Zettel）
  科学模型事后解释可靠性研究，arXiv 2606.29346。
  源：`arxiv-api`
- **PHF: Privileged Hidden Flow for On-Policy Self-Distillation**（未升级 Zettel）
  在线策略自蒸馏新方法，arXiv 2606.29340。
  源：`arxiv-api`
- **Nonlinear mixture model motivated subspace clustering**（未升级 Zettel）
  非线性混合模型驱动的子空间聚类，arXiv 2606.29261。
  源：`arxiv-api`
- **PhysisForcing: Physics Reinforced World Simulator for Robotic Manipulation** ([[202606300955-physisforcing-physics-world-model]])
  训练阶段注入物理约束力，从根本上解决视频生成世界模型的物理不合理问题，HF 40 upvotes 本批次最高。
  源：`huggingface-daily-papers`
- **Translation as a Bridging Action: Transferring Manipulation Skills from Humans to Robots**（未升级 Zettel）
  通过人类动作数据向双臂机器人迁移新操作技能，HF 33 upvotes。
  源：`huggingface-daily-papers`

## 2026-06-29

- **梁文锋署名的DSpark** ([[202606291410-dspark-architecture-deepseek]])
  DeepSeek 系统工程论文，梁文锋亲署，精髓在于极强的工程优化而非算法创新。
  源：`qbitai`
- **PhysisForcing: Physics-Constrained World Models**（未升级 Zettel）
  物理约束世界模型，HF 3 upvotes。
  源：`huggingface-daily-papers`
- **Ko-WideSearch: Korean Web Agent Benchmark**（未升级 Zettel）
  韩语 Web Agent 基准数据集，HF 2 upvotes。
  源：`huggingface-daily-papers`
- **Qwen-Image-2.0-RL: Reinforcement Learning for Image Generation**（未升级 Zettel）
  Qwen 图像生成 RL 训练论文，HF 1 upvote。
  源：`huggingface-daily-papers`
- **Formalizing Latent Thoughts in LLMs**（未升级 Zettel）
  LLM 内部思维公理化表示，HF 1 upvote。
  源：`huggingface-daily-papers`
- **NormGuard: Norm-Constrained Flow Matching RL**（未升级 Zettel）
  范数约束 Flow Matching RL，HF 0 upvotes。
  源：`huggingface-daily-papers`
- **Google Paper Assistant: AI Tool for Scientific Paper Review**（未升级 Zettel）
  Google AI 辅助科学同行评审工具论文，HF 0 upvotes。
  源：`huggingface-daily-papers`
- **SimFoundry: Robot Policy Simulation Generation**（未升级 Zettel）
  机器人策略仿真生成框架，HF 0 upvotes。
  源：`huggingface-daily-papers`

## 2026-06-28

- **MME-CoF-Pro（延续）** ([[202606271436-mme-cof-pro-video-reasoning]])
  28 日批次再次抓到，视频推理能力与生成质量解耦的结论持续传播。
  源：`jiqizhixin`

- **微软年度 AI 职场报告 2026**（未升级 Zettel，低置信度）
  28 页报告指出员工已准备好使用 AI 但企业流程尚未适配；具体数据待核实。
  源：`qbitai`

- **The Batch Issue 358: Testing Mythos and Fable**（未升级 Zettel，低置信度）
  The Batch 评测 Mythos / Fable，并讨论超越 SWE-bench 的下一代 coding 基准方向。
  源：`the-batch`

## 2026-06-27

- **Multi-teacher On-Policy Distillation (MOPD)** ([[202606271435-mopd-post-training]])
  前沿 post-training 菜谱综述：MOPD 以多教师在线蒸馏解决单一教师的分布漂移问题。
  源：`interconnects`

- **MME-CoF-Pro: 303 sample video reasoning benchmark (ECCV 2026)** ([[202606271436-mme-cof-pro-video-reasoning]])
  专注视频链式推理的新基准被 ECCV 2026 采纳；Veo 56 / Sora 50，视频推理仍有大空间。
  源：`jiqizhixin`

