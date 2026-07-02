---
id: 2026-07-02-0901-dockerless-environment-free-program-verifier
type: source-original
title: 'Dockerless：面向编码代理的无环境程序验证器'
original_title: 'Dockerless: Environment-Free Program Verifier for Coding Agents'
source_name: huggingface-daily-papers
source_url: 'https://huggingface.co/papers/2606.28436'
author:
  - Wenhao Zeng
  - Yuling Shi
  - Xiaodong Gu
  - Chao Hu
  - Chaofan Wang
  - Yuhao Cui
  - Hongting Zhou
  - Mengnan Qi
  - Jianqiao Wangni
  - Zhaojian Yu
  - Shuzheng Gao
  - Kai Cai
  - Shilin He
published_at: 2026-06-26
fetched_at: '2026-07-02T09:12:26+08:00'
language: en
translated: true
translation_engine: haiku
word_count: 1181
images_attempted: 25
images_saved: 25
fallback_notice: null
related_daily: 2026-07-02
related_zettels: []
related_topics: []
tags:
  - source-original
  - language-en
---

# Dockerless：面向编码代理的无环境程序验证器

> 原文：[Dockerless: Environment-Free Program Verifier for Coding Agents](https://huggingface.co/papers/2606.28436) · huggingface-daily-papers · 2026-06-26
> 抓取：2026-07-02T09:12:26+08:00 · 翻译：haiku · 1181 字

## 摘要

程序验证器在训练编码代理中发挥核心作用，包括为监督微调（SFT）选择轨迹和为强化学习（RL）提供奖励。标准的基于执行的验证需要在按仓库配置的环境（如 Docker 镜像）内运行单元测试，这产生了大量的环境设置成本。我们提出 Dockerless，一种无环境的代理化补丁验证器，它可以评估生成的代码补丁而无需执行它们。与简单地将候选补丁与参考补丁进行匹配相反，Dockerless 使用通过代理化仓库探索收集的证据来判断补丁的正确性。在验证器评估基准上，Dockerless 比最强的开源验证器高出 14.3 个 AUC 点。将 Dockerless 同时用作 SFT 轨迹过滤器和 RL 奖励函数可实现完全无环境的后训练流程。生成的模型在 SWE-bench Verified、Multilingual 和 Pro 上分别达到 62.0%、50.0% 和 35.2% 的解决率。它比 Qwen3.5-9B 基线分别高出 2.4、8.7 和 2.9 个百分点，与基于环境的后训练相匹配。

## 概述

本论文介绍了 Dockerless，一个新颖的验证系统，可以评估代码补丁是否正确解决编程任务，而无需依赖容器化环境。该研究解决了 AI 辅助软件工程中的一个关键挑战：现有验证方法依赖于 Docker 容器和隔离执行环境。这些方法在大规模评估编码代理输出时会引入显著的计算开销、延迟问题和基础设施复杂性。

## 核心创新

Dockerless 的方法消除了环境依赖，同时保持了验证的准确性。这代表了从基于容器的程序验证到与环境无关的验证的范式转变，使得能够更高效地评估 AI 生成的代码解决方案。

### 技术方法

该验证系统采用"代理化仓库探索"的方法来判断补丁正确性。系统通过两个阶段运作：

**第一阶段：问题生成与证据收集**

验证器从问题描述和参考补丁中推导诊断问题，然后派遣并行的子代理来使用 `find` 和 `grep` 等只读工具探索仓库。

**第二阶段：判断**

收集的证据用于支持最终的正确性评估，产生一个 0 到 1 之间的连续分数。

### 训练方法

训练方法对 3.7K 个执行标记的问题进行拒绝采样。系统通过仅保留预测判决与地面真值测试结果相匹配的轨迹来学习，确保一致的推理链而不是幸运匹配。

## 性能成果

在验证器基准上，Dockerless 在 SWE-bench Verified 上达到了 81.0 AUC，比最强的开源替代方案高出 14.3 个点。对于端到端的模型训练，完全无环境的流程在 SWE-bench Verified 上达到了 62.0% 的解决率，与基于环境的方法相匹配，同时无需任何仓库特定的设置。

## 实际影响

这项工作使得能够在没有 Docker 依赖解决的情况下进行编码代理的可扩展后训练，使得对"缺乏可复现测试环境的真实世界仓库的广阔长尾"进行训练成为可行。

## 相关工作背景

该研究为软件工程与机器学习领域的发展做出贡献，特别是支持编码代理训练和 SWE-bench 等基准框架的最新进展。该工作使得验证系统的实际部署对于大规模代码生成评估成为可能。

## 关键数据

- 在验证器评估基准上的 AUC 提升：14.3 点
- SWE-bench Verified 解决率：62.0%
- SWE-bench Multilingual 解决率：50.0%
- SWE-bench Pro 解决率：35.2%
- 相对于 Qwen3.5-9B 基线的改进：
  - Verified：+2.4 点
  - Multilingual：+8.7 点
  - Pro：+2.9 点
- 训练数据：3.7K 个执行标记的问题

## 论文贡献

本论文的主要贡献包括：

1. 提出 Dockerless 框架，一种无环境的代理化补丁验证方法
2. 展示代理化仓库探索在补丁评估中的有效性
3. 演示完全无环境的后训练流程的可行性
4. 在 SWE-bench 基准上实现与基于环境的方法竞争的性能

## 结论

Dockerless 通过消除对 Docker 和仓库特定环境配置的依赖，为编码代理的训练和评估提供了一个更实用和可扩展的方法。通过使用代理化推理来评估补丁正确性，该系统在保持性能的同时大幅降低了基础设施复杂性，使得对大规模、多样化代码库的训练成为可行。

![图 1](_assets/2026-07-02/2026-07-02-0901-dockerless-environment-free-program-verifier-001.webp)

![图 2](_assets/2026-07-02/2026-07-02-0901-dockerless-environment-free-program-verifier-002.webp)

![图 3](_assets/2026-07-02/2026-07-02-0901-dockerless-environment-free-program-verifier-003.webp)

![图 4](_assets/2026-07-02/2026-07-02-0901-dockerless-environment-free-program-verifier-004.webp)

![图 5](_assets/2026-07-02/2026-07-02-0901-dockerless-environment-free-program-verifier-005.webp)

![图 6](_assets/2026-07-02/2026-07-02-0901-dockerless-environment-free-program-verifier-006.webp)

![图 7](_assets/2026-07-02/2026-07-02-0901-dockerless-environment-free-program-verifier-007.webp)

![图 8](_assets/2026-07-02/2026-07-02-0901-dockerless-environment-free-program-verifier-008.webp)

![图 9](_assets/2026-07-02/2026-07-02-0901-dockerless-environment-free-program-verifier-009.webp)

![图 10](_assets/2026-07-02/2026-07-02-0901-dockerless-environment-free-program-verifier-010.webp)

![图 11](_assets/2026-07-02/2026-07-02-0901-dockerless-environment-free-program-verifier-011.webp)

![图 12](_assets/2026-07-02/2026-07-02-0901-dockerless-environment-free-program-verifier-012.webp)

![图 13](_assets/2026-07-02/2026-07-02-0901-dockerless-environment-free-program-verifier-013.webp)

![图 14](_assets/2026-07-02/2026-07-02-0901-dockerless-environment-free-program-verifier-014.webp)

![图 15](_assets/2026-07-02/2026-07-02-0901-dockerless-environment-free-program-verifier-015.webp)

![图 16](_assets/2026-07-02/2026-07-02-0901-dockerless-environment-free-program-verifier-016.webp)

![图 17](_assets/2026-07-02/2026-07-02-0901-dockerless-environment-free-program-verifier-017.webp)

![图 18](_assets/2026-07-02/2026-07-02-0901-dockerless-environment-free-program-verifier-018.webp)

![图 19](_assets/2026-07-02/2026-07-02-0901-dockerless-environment-free-program-verifier-019.webp)

![图 20](_assets/2026-07-02/2026-07-02-0901-dockerless-environment-free-program-verifier-020.webp)

![图 21](_assets/2026-07-02/2026-07-02-0901-dockerless-environment-free-program-verifier-021.webp)

![图 22](_assets/2026-07-02/2026-07-02-0901-dockerless-environment-free-program-verifier-022.webp)

![图 23](_assets/2026-07-02/2026-07-02-0901-dockerless-environment-free-program-verifier-023.webp)

![图 24](_assets/2026-07-02/2026-07-02-0901-dockerless-environment-free-program-verifier-024.webp)

![图 25](_assets/2026-07-02/2026-07-02-0901-dockerless-environment-free-program-verifier-025.webp)

---

**论文来源**：arXiv:2606.28436 | **组织**：ByteDance | **发布日期**：2026年6月26日

