---
name: ainews-source-matrix
description: AInews 信息源 v1 选型与有效性矩阵（实测 2026-06-27，含主力/降级/死源黑名单）——正式接入前必须复验时效
metadata:
  type: project
---

AI 资讯信息源**有效性实测结论（2026-06-27，由 3 个核查 subagent 联网逐源验证）**。⚠️ RSS/API 会变动，正式接入前需复验最新一条时效。frontmatter 建议给每源标注 `tier / perspective(research|product|investor) / fetch_method / url / reliability`。

**一手来源 + 学术**
- ✅ OpenAI 官方 RSS `https://openai.com/news/rss.xml`
- ✅ Google DeepMind 官方 RSS `https://deepmind.google/blog/rss.xml`
- ✅ arXiv 官方 API `http://export.arxiv.org/api/query`（按 `cat:cs.AI`/`cat:cs.LG` + `sortBy=submittedDate` 检索，需 ~3 秒/次限流，返回 Atom XML）
- ✅ HuggingFace Daily Papers `https://huggingface.co/api/daily_papers`（JSON，带 upvotes 社区策展，信噪比最高，自带 arxiv id 可回链；支持 `?date=YYYY-MM-DD`）
- ⚠️ Anthropic：无官方 RSS → WebFetch `https://www.anthropic.com/news`
- ⚠️ Meta AI：无 RSS 且更新慢 → 低频 WebFetch `https://ai.meta.com/blog/`，靠 arXiv 兜底
- ❌ Papers with Code：**2025-07 已被 Meta 关停**，整站 302 重定向到 HF，弃用（角色由 HF Daily Papers/Trending 替代）

**聚合分析层**
- ✅ Import AI（Jack Clark）RSS `https://importai.substack.com/feed`（周更，政策/治理/前沿深度）
- ✅ Interconnects（Nathan Lambert）RSS `https://www.interconnects.ai/feed`（RLHF/训练/开源硬核，部分付费墙仅摘要）
- ✅ 量子位 RSS `https://www.qbitai.com/feed`（中文高频近日更，需关键词过滤融资/PR 软文）
- ⚠️ The Batch（质量最高，吴恩达周评，几乎无软文）：无官方 RSS → WebFetch `https://www.deeplearning.ai/the-batch/`，建议保留为"加固主力"
- ⚠️ 机器之心：无官方 RSS → 微信镜像 `http://plink.anyfeeder.com/weixin/almosthuman2014` 或 RSSHub，需双兜底
- ❌ Ben's Bites：已转型为低频创投/builder 评论，旧"每日产品"刊停更，降级/弃用

**投资 / 市场视角层**（用户"听推荐"，结论：以 Air Street 为主力）
- ✅ **Air Street Press** RSS `https://press.airstreet.com/feed` —— **投资层里唯一开箱即用、干净、免费、时效到当天**的结构化源
- ✅ State of AI Report `https://www.stateof.ai`（年度 PDF/Slides 锚点，每年约 10 月，最权威独立 AI 年报）
- ⚠️ Stratechery（Ben Thompson，**非 VC 立场**）：免费周更长文 + 免费 Passport 个性化 RSS，但 ToS 禁共享，单账号自用
- ⚠️ a16z：⚠️**用户原本想加，但经典 RSS `a16z.com/feed/` 已死约 2 年**，只能 WebFetch `https://a16z.com/news-content/`，且强 VC 叙事偏向 → 可选、需打 `perspective: investor` + `bias: VC` 标签
- ❌ CB Insights（颗粒数据全在付费墙后）、Sequoia（无 RSS、更新稀疏）：v1 降权

**Twitter/X 实时信号**：Nitter ❌公共实例全灭、RSS-Bridge ⚠️需自带付费 token 且高运维易碎。要做只剩两条——X 官方 pay-per-use（合规，精选号小量读取很便宜，~$0.001–0.005/条）或 TwitterAPI.io（最省心但属 X ToS 灰区，Apify 作兜底）。→ **v1 暂不做，列为 v2 可选**。

**反直觉尽调发现（教训）**：用户最初的几个直觉源在实测后被证伪——RSS 统一管道、a16z、Papers with Code、Nitter 都已死或不可靠。→ 沉淀为偏好：**先实测信息源有效性，再写采集架构**，否则 v1 上线即一堆死链。

相关：[[ainews-project-architecture]]。
