# 过滤 / 聚类 / 写盘判断标准

> 给 news-filter、news-cluster、news-writer subagent 的判断标准。
> 默认偏严：宁可少留高质量，也不放噪音过线。

最后更新：2026-06-27

---

## 1. 去重规则（news-filter）

按以下顺序判断，命中任一即视为重复（保留**信息最完整**的那条，其余丢弃并记原因）：

1. **URL 完全相同**（含查询参数）→ 直接合并
2. **URL host + path 相同**（忽略 utm/ref 等查询参数）→ 视为同一条
3. **标题 ≥ 0.85 语义相似**（subagent 自行判断；可参考"同事件、同主体、同动作"三要素）→ 视为同事件不同源报道，**保留 tier 更低（更一手）的那条**
4. **正文摘要前 100 字 ≥ 0.9 重叠**（罕见但要兜底）→ 同 2

**不去重**：
- 同事件的中英双语报道（两条都留，cluster 阶段合到同 topic）
- 同事件的"发布"+"深度分析"两类报道（角度不同）

---

## 2. 信噪过滤规则（news-filter）

**默认丢弃**（写入丢弃理由）：

| 类别 | 关键词 / 模式 | 例外 |
|---|---|---|
| 融资 PR | "completes Series X", "raises $XM", "valuation reaches" | 投资方是顶级 VC + 金额 > $100M + 公司是 AI 头部 → 保留 |
| 招聘 / 团队公告 | "we're hiring", "join our team" | 关键人物动向（如核心研究员跳槽）→ 保留 |
| 活动 / 大会通知 | "register now", "RSVP", "conference announcement" | 顶会 NeurIPS/ICML 论文榜单 → 保留 |
| 产品营销软文 | 通篇赞美、无技术细节、无可验证数据 | — |
| 二手编译 | "据 XX 报道"、"the X reported" + 无新增信息 | 编译方加了独家分析 → 保留 |
| 广告 / 赞助 | "sponsored by"、"promoted post" | — |

**保留优先**：
- 一手发布（论文、官方博客、官方公告）
- 含可验证基准数据（benchmark, eval scores）
- 含开源 release（github / huggingface 链接）
- 政策 / 监管动向（EU AI Act, FCC, NIST 等）
- 安全 / 对齐 / 失败案例（无论来源）

**模糊地带**：subagent 拿不准时**倾向保留**，标 `low_confidence: true`，让 cluster 阶段二次判断。

---

## 3. 主题聚类规则（news-cluster）

### 推荐主题桶（slug 用 kebab-case，对应 `20-Topics/<slug>.md`）

| slug | 包含 |
|---|---|
| `model-releases` | 新模型/版本发布、参数公布、基准刷新 |
| `safety-alignment` | RLHF、red-teaming、AI 安全研究、对齐失败案例 |
| `opensource-tools` | 新开源框架/库/工具/数据集 |
| `research-papers` | arXiv / HF Daily Papers 学术为主（不涉发布事件） |
| `policy-regulation` | 政策、监管、立法、政府动向 |
| `industry-moves` | 公司层动作（合作、收购、关停、战略转向） |
| `funding-investment` | 通过 §2 过滤后仍保留的融资事件 |
| `infra-hardware` | GPU、芯片、数据中心、训练成本 |
| `applications` | AI 在垂直行业的应用案例 |

**粒度**：
- 一个桶 ≥ 2 条才独立成 topic；< 2 条归 `applications` 或 `industry-moves` 杂项
- 桶 > 8 条要考虑切分（如 `model-releases-llm` vs `model-releases-multimodal`）
- 新主题：如果一天里某新领域涌出 ≥ 3 条且现有桶都不合适 → 创建新 topic 并在 Daily 注释「新增主题」

### 不要做的事
- ❌ 不要按"来源"聚类（来源是 frontmatter 字段，不是主题）
- ❌ 不要按"公司"聚类（应按"事件类型"——例如同一天 OpenAI 既发模型又签合作，分别归 model-releases 与 industry-moves）

---

## 4. Zettel 入选标准（news-writer）

不是每条 entry 都升级为 Zettel。**仅以下情况升级**：

1. **概念/方法首次出现**：vault 内全文搜索后该概念无 Zettel → 创建
2. **重大事件锚点**：有历史价值的发布/收购/政策（半年后回看仍重要）
3. **可复用洞察**：含一句"可被引用"的关键判断（如"context window 不再是瓶颈"）

**不升级**为 Zettel 的情况：
- 仅是事件通知（产品发布的"附带条目"），只在 Daily 列出 + wikilink 一笔带过
- 同概念已有 Zettel：在 Daily 直接 wikilink 旧 Zettel，不重建

**升级数控制**：
- 一次跑 Zettel 总数建议 3–10 张；超过 10 张说明 filter 不够严，回头检查
- 全部条目都不达标也 OK（罕见的"低产日"），Daily 写一句"今日无原子卡级洞察"
