# 过滤 / 聚类 / 写盘判断标准

> 给 news-cluster、news-writer subagent + Phase 2 filter 脚本的判断标准。
> 默认偏严：宁可少留高质量，也不放噪音过线。

**v2.3 起 §1.1 / §1.5 / §2 / §2.5 由 `scripts/filter-inline.py` 主会话内联规则化执行**（不再走 news-filter agent）。本节规则是脚本实现 + 人工 review 的双重权威——脚本规则与本节冲突时以本节为准，需同步修脚本。

最后更新：2026-06-29

---

## 1. 去重规则（news-filter）

### 1.1 同跑内去重

按以下顺序判断，命中任一即视为重复（保留**信息最完整**的那条，其余丢弃并记原因）：

1. **URL 完全相同**（含查询参数）→ 直接合并
2. **URL host + path 相同**（忽略 utm/ref 等查询参数）→ 视为同一条
3. **标题 ≥ 0.85 语义相似**（subagent 自行判断；可参考"同事件、同主体、同动作"三要素）→ 视为同事件不同源报道，**保留 tier 更低（更一手）的那条**
4. **正文摘要前 100 字 ≥ 0.9 重叠**（罕见但要兜底）→ 同 2

**不去重**：
- 同事件的中英双语报道（两条都留，cluster 阶段合到同 topic）
- 同事件的"发布"+"深度分析"两类报道（角度不同）

### 1.5 跨日去重（v2.2 新增）

filter 在 §1.1 同跑内去重完成后，对剩下 kept 候选**再过一道跨日 _seen-urls.json 索引**：

**URL normalize 规则**（用于跨日命中匹配，**不**改写 entry.url 本身的值）：

```
normalize(url) =
  url.lower()
     .replaceAll(/^https?:\/\//, '')      // 去 scheme
     .replaceAll(/^www\./, '')             // 去 www 前缀
     .replaceAll(/[?#].*$/, '')           // 去查询参数和 anchor
     .replaceAll(/\/+$/, '')               // 去尾斜杠
```

例如：
- `https://www.anthropic.com/news/fable-mythos-access` → `anthropic.com/news/fable-mythos-access`
- `https://anthropic.com/news/fable-mythos-access?utm=x` → `anthropic.com/news/fable-mythos-access`
- 上面两条 normalize 后**相同** → 跨日去重视为同一文章

匹配时构建临时 map `{normalized_url: original_seen_node}`，候选 URL normalize 后做 key lookup。命中后回看 seen_node 拿 first_seen_date 等字段做决策。

**步骤**：
1. Read `00-Inbox/_seen-urls.json`（不存在 → 跳过本段，按新 schema 建空文件）
2. 清理过期节点：删除 `first_seen_date` 距 target_date > 30 天的 URL 节点（防文件膨胀），把清理动作记到自己的 stats.seen_urls_pruned
3. 对每条 kept 候选 URL，按下表决策：

| 候选 URL 命中 _seen-urls | first_seen_date 距 target_date | 决策 |
|---|---|---|
| ✗ 未命中 | — | 正常进 kept，待 filter 末尾追加进 _seen-urls |
| ✓ 命中 | ≤ 7 天 | **默认 discarded**，reason: `seen-on-<first_seen_date>` |
| ✓ 命中 | ≤ 7 天 + 词汇重叠 ≤ 0.6 | **保留**，标 `re_coverage: true` + `previously_kept_in_daily: <date>`（方案 Y 豁免） |
| ✓ 命中 | > 7 天 | 视为已淡出，正常进 kept |

4. **词汇重叠豁免计算**（方案 Y）：
   - 对当前 entry.raw_summary 与 _seen-urls 内对应 URL 的 raw_summary_excerpt 做词集 Jaccard：
     - 中文：按字切分（去停用词"的、了、和、是、在、对"等）
     - 英文：按空格切分（去停用词 `the/a/an/of/to/in/and/is/for/on/with`，转小写）
   - `overlap = |A ∩ B| / |A ∪ B|`
   - `overlap > 0.6` → 视为同视角复述，**仍 discarded**（不豁免）
   - `overlap ≤ 0.6` → 视为新角度/深度分析，**保留**并标 `re_coverage: true`
   - raw_summary 或 raw_summary_excerpt 任一为空时，词集为 ∅ → overlap 视为 0 → 默认丢（不豁免空摘要）

5. **写回 _seen-urls.json**——把本跑次最终 kept（含 re_coverage 项）的 URL 写回：
   - 全新 URL → 创建节点，填 `first_seen_date / first_seen_run / title / source_name / kept_in_daily / raw_summary_excerpt`（zettel_id 留空，writer Phase 4 回填）
   - 既有 URL 但因 re_coverage 保留 → **不更新** first_seen_date（保留首次），但在 `kept_in_daily` 追加当日日期（变数组）
   - 全文写盘前先 sort `urls` 节点的 keys 让 diff 稳定

**re_coverage 条目下游处理**：
- cluster 视为正常 entry，可分到对应 topic
- writer 写 Daily 时该条 entry 前缀一个 🔄 标识（如 `🔄 [复盘] <title>`），并在 frontmatter `re_coverage_count` +1
- digester 同样输出，但章节内排在该 topic 末尾
- writer 不重建 Zettel——若 _seen-urls 内已有 zettel_id，直接复用 wikilink；若无则按常规判断 zettel_worthy

---

## 2. 信噪过滤规则（filter-inline.py §2）

**默认丢弃**（写入丢弃理由）：

| 类别 | 关键词 / 模式 | 例外 |
|---|---|---|
| 融资 PR | `raises $XM`, `closes/completes Series X`, `valuation reaches`, `融资 N 亿`, `估值 N 亿`, `完成 X 轮` | 顶级 VC + $100M+ + AI 头部 → 降为 `low_confidence: true` 保留（让 cluster 二判） |
| 招聘 / 团队公告 | `we're hiring`, `join our team`, `open roles`, `招聘`, `急聘`, `内推` | 关键人物动向（如核心研究员跳槽）→ 不在 §2 规则化丢，靠 cluster 二判 |
| 活动 / 大会通知 | `register now`, `RSVP`, `conference announcement`, `save the date`, `报名通知`, `嘉宾邀请` | 顶会 NeurIPS/ICML 论文榜单 → 靠 §2 keep signal `paper`/`benchmark` 覆盖 |
| 广告 / 赞助 | `sponsored by`, `promoted post`, `#sponsored`, `赞助内容`, `推广文章`, `商务合作` | — |
| **VC 软文 / IR 公告（v2.3 新增）** | 标题开头 `Investing in X`、`Investor Relations`、`Late Stage Venture`、`投资了` | — |
| 产品营销软文 | 通篇赞美、无技术细节、无可验证数据 | 无规则化模式（脆弱），靠 cluster 二判 |
| 二手编译 | 「据 XX 报道」、"the X reported" + 无新增信息 | 编译方加了独家分析 → 不在 §2 规则化丢，靠 cluster 二判 |

**保留优先信号（hit 任一 → keep，覆盖一切 discard 规则）**：
- arxiv.org / github.com / huggingface.co 链接
- `benchmark`、`eval/evaluation score/result`、`SOTA`、`state-of-the-art`
- `open-source`、`开源`、`论文`、`预印本`、`基准`、`评测`
- 政策关键词：`EU AI Act`、`NIST`、`FCC`、`executive order`
- 安全 / 对齐 / 可解释性：`red-team`、`alignment`、`safety`、`interpretability`、`对齐`、`可解释性`、`安全研究`

**模糊地带**：脚本判不准时**倾向保留**，标 `low_confidence: true`，让 cluster 阶段二次判断。具体规则：
- tier 3 + 摘要 < 50 字 + 无 keep signal → low_confidence keep
- published 解析失败 → low_confidence keep

## 2.5 时效过滤规则（filter-inline.py §2.5，v2.3 新增 / v2.4 单源化）

> **v2.4 起 fetcher 不再做任何时窗过滤**（之前 fetcher subagent prompt 内有"过滤超过 7 天的旧条目"是 v1 残留，与本节 14d 阈值不一致，导致 7-14d 内有效内容被 fetcher 提前剔）。时效判定**单一权威在本节**——fetcher 把抓到的最多 N 条全保留交给主会话，由 filter-inline.py §2.5 按 14d 阈值统一裁决。

**规则**：`entry.published` 距 `target_date` **> 14 天** → discard，reason `stale:Nd_old`。**所有 source 一律 14 天阈值，不分 tier**。

**设计原因**：
- 用户期望"今天的 AI 新闻"，14d 前的内容是 throwback
- RSS feed 经常给陈年项（feed reader 提供"最近 N 条"而非"按时间窗口"），若不过滤 anthropic/the-batch 这种偶有低活跃期的源会污染当日 Daily
- 与 §1.5 跨日去重协同：14d 内 + 命中 _seen-urls → cross_day_discarded；14d 内 + 未命中 → kept；14d 外 → stale_discarded
- 副作用：tier 1 一手发布源（anthropic 等）若 RSS 推送陈年项会被丢，且 meta-ai-blog 等低活源若全部陈年会"看起来失效"——这是预期行为，需在 Phase 6 Log 醒目标出按 source 拆分的 stale 数，用于发现源活性退化

**执行顺序**（filter-inline.py）：§1.1 同跑去重 → **§2.5 时效（先于 §2）** → §2 信噪 → §1.5 跨日去重 → Write。§2.5 优先于 §1.5 意味着"14d 外 + 已 seen"会归类为 stale 而非 cross_day_discarded，最终结果相同。

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

---

## 5. Tags 打标策略（news-writer 必读）

writer 给 Daily / Zettel / Topic 的 frontmatter `tags` 数组打标。Tag 让 Obsidian tag pane + Bases 视图按维度切片。

### 分类轴（每条 entry 应有 ≥ 2 个、≤ 5 个 tag）

| 轴 | tag 形式 | 例子 | 取自哪里 |
|---|---|---|---|
| **技术领域** | 单词小写 | `llm` `multimodal` `agent` `rlhf` `safety` `cv` `nlp` `rl` `interpretability` `inference` `training` `eval` | 内容判断 |
| **产品/公司** | 公司名小写 | `openai` `anthropic` `google` `meta` `nvidia` `deepmind` `zai` `cursor` | title/summary 提到 |
| **事件类型** | 行为词 | `release` `paper` `funding` `policy` `partnership` `personnel` `opensource` | 与 topic slug 同步 |
| **来源 tier 标签**（仅在 source 是 fallback / degraded / VC 时打） | `tier3` `degraded` `vc-bias` | sources.md 字段 | frontmatter |

### 命名规则
- 全小写、kebab-case（多词用连字符）
- 不用中文（Obsidian tag pane 对中文支持但不利搜索）
- 公司名用常用简称（`openai` 不是 `open-ai`、`zai` 不是 `z-ai`）
- 不要把 topic slug 重复成 tag（topic 已经是 wikilink，tag 用更细粒度的技术词）

### 示例

GPT-5.6 Sol 发布的 Zettel：
```yaml
tags: [llm, release, openai, safety, coding]
```

arXiv 67 模型 co-failure ceiling 论文的 Zettel：
```yaml
tags: [llm, paper, eval, agent, opensource]
```

a16z VC 评论的 Zettel（如果有）：
```yaml
tags: [policy, vc-bias, tier3]
```

Daily 简报 frontmatter（聚合）：
```yaml
tags: [daily-digest, <当日主要技术领域 tag 各 1>]   # 如 [daily-digest, llm, safety, agent]
```

### 禁忌

- ❌ 不要 invent 新 tag（除非 ≥ 3 条 entries 都该共享某个新轴，否则用现有轴）
- ❌ 不要给低质量条目（low_confidence + 未升级 Zettel）打超过 2 个 tag——避免污染 tag pane
- ❌ 不要打 `#ai` `#ml` 这种过宽的 tag——全 vault 都该有，无信息量
