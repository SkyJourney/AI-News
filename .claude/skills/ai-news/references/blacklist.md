# AInews 信息源黑名单（防"想当然"加回）

> 这些源在实测中已死、转型、付费墙或不可靠。**未来任何 AI 或人想"加上经典 RSS"前必读本文件**。
> 移除某源时同步从 [sources.md](sources.md) 删除，把记录搬到这里。

最后更新：2026-06-27

---

## ❌ 已死 / 已停 / 已转型

### papers-with-code
- **失效日期**：2025-07
- **状态**：被 Meta 关停，整站 302 重定向到 HuggingFace
- **原本用途**：跟踪带代码的论文榜单 / SOTA
- **替代**：已在 sources.md 的 `huggingface-daily-papers` 内由 HF 接管角色
- **复活前提**：不会复活，永久关停

### bens-bites
- **失效日期**：2025（具体月份未确认）
- **状态**：转型为低频创投/builder 评论，旧"每日产品刊"停更
- **原本用途**：每日 AI 产品速览
- **替代**：无直接替代；Air Street Press 在投资视角部分覆盖
- **复活前提**：除非他们重启"每日产品"刊，否则不要加

### a16z-rss
- **URL**：`https://a16z.com/feed/`
- **失效日期**：约 2023 起，**用户原本想加这条**
- **状态**：经典 RSS 死链约 2 年
- **替代**：低优先级 WebFetch `https://a16z.com/news-content/`，且强 VC 叙事偏向
- **复活前提**：a16z 重启官方 RSS（不太可能）；若加 WebFetch 必须打 `perspective: investor` + `bias: VC` 标签

### nitter-public-instances
- **失效日期**：2024
- **状态**：所有 Nitter 公共实例已被 X 反爬全灭
- **原本用途**：免费抓 X/Twitter
- **替代**：v1 暂不做 X；v2 候选 = X 官方 pay-per-use 或 TwitterAPI.io（ToS 灰区）
- **复活前提**：Nitter 找到稳定突破方案（基本无望）

---

## ❌ 付费墙 / 无 RSS / 更新稀疏（不值得 v1 接入）

### cb-insights
- **状态**：颗粒数据全在付费墙后
- **原本用途**：创投市场数据
- **决策**：v1 降权弃用，需要数据时人工查阅

### sequoia
- **状态**：无 RSS、更新稀疏
- **决策**：v1 降权弃用

---

## ⚠️ ToS 限制（合法但不纳入采集）

### stratechery
- **状态**：免费周更长文 + 免费 Passport 个性化 RSS
- **限制**：ToS 禁共享，单账号自用
- **决策**：不纳入 `/ai-news` 自动采集；用户可自行订阅阅读

---

## 不在 v1 范围（边界，等 v2 评估）

| 资源 | 状态 | v2 候选方案 |
|---|---|---|
| Twitter/X 实时信号 | Nitter 全灭、X API 计费 | X 官方 pay-per-use（~$0.001–0.005/条）或 TwitterAPI.io（灰区） |
| State of AI Report PDF | 年度发布（约 10 月） | 单独的"年报事件"触发，不在日常 daily |
| Sequoia AI 长文 | 偶发优质 | 人工转发到 `40-Deep-Dives/` |

---

## 教训沉淀

用户最初的几个直觉源在实测后被证伪——RSS 统一管道、a16z 经典 RSS、Papers with Code、Nitter 都已死或不可靠。

→ 偏好：**先实测信息源有效性，再写采集架构**，否则 v1 上线即一堆死链。
