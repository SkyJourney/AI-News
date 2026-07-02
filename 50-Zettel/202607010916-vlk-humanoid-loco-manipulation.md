---
created: 2026-07-01 09:16:00
updated: 2026-07-01 09:16:00
status: draft
title: 'VLK 框架实现人形机器人无标注 sim-to-real 迁移'
source: arxiv-api
source_url: http://arxiv.org/abs/2606.30645v1
topic: research-papers
tags: [paper, rl, cv, training]
---

## 概念 / 事件

VLK（Vision-Language-Kinematics）框架：用 3D 高斯溅射重建真实室内场景、合成 48,000 条视觉-语言-运动学配对轨迹，无需人工标注地训练人形机器人感知操作策略，在 Unitree G1 上完成 sim-to-real 迁移。

## 关键洞察

- "合成数据 + 重建场景"绕过人形机器人数据收集瓶颈——48,000 条轨迹在无人工干预下自动生成，规模化路径明确
- 视觉-语言-运动学三模态联合预测是关键设计：单独预测任一模态都会降低全身协调质量
- Sim-to-real 在人形机器人上的验证说明 3DGS 场景重建已足够忠实，成为 embodied AI 新基础设施

## 来源

- [原文](http://arxiv.org/abs/2606.30645v1) — `arxiv-api`

## 关联

- [[research-papers]]
- [[agents]]
