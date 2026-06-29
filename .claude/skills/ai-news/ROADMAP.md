# /ai-news skill 演化 Roadmap

> 跟踪 v2.3 后续可做的优化项。每条编号沿用 v2.3 会话内的 A 标号（A1-A10），
> 不重编号，便于回查 [[2026-06-29-run]] log 与 commit 历史。

最后更新：2026-06-29 v2.3 端到端首次跑通后

---

## 已完成（v2.3 落地）

- **A1** cluster agent `model: sonnet → haiku`（commit `beeffcd`）—— 预期 5m17s → < 2 分钟
- **A2** ~~sources.md meta-ai-blog reliability 改 degraded~~ —— 撤销，实际已是 degraded（Log 误判）
- **A3** cluster agent system prompt 加严字段约束（`topic_slug` not `slug`、`is_new` 必填）（commit `beeffcd`）

---

## 待办（按 ROI 排）

### A4 · cluster-merge.py 按 source 默认 topic 兜底

**问题**：cluster agent 自检要求 mappings 完全对齐 kept，偶尔漏。当前 cluster-merge.py 漏的兜底归 `applications`——粗糙。

**实施**：cluster-merge.py 加一个 `SOURCE_DEFAULT_TOPIC` 表，漏的条目按 `source_name` 兜底：
```python
SOURCE_DEFAULT_TOPIC = {
    'arxiv-api': 'research-papers',
    'huggingface-daily-papers': 'research-papers',
    'a16z-news-content': 'applications',    # tier3 评论默认杂项
    'state-of-ai': 'industry-moves',
    'the-batch': 'model-releases',           # 周刊主要讲模型
    # ...
}
```

**成本**：30 min（写表 + 测试）
**收益**：cluster agent 偶尔漏映射时归类更准；errors 数组的 `agent_missing_urls` 不再代表"丢条目"而代表"按 source 默认归类了"
**紧迫**：低（兜底已 work，只是更准）

---

### A5 · _seen-urls 预填脚本固化 `scripts/seen-urls-bootstrap.py`

**问题**：cold start（_seen-urls.json 不存在或损坏）时需要主会话手写 Python 扫历史 Daily 反推索引。本次 6-29 会话就手写过一次。

**实施**：
1. 新建 `scripts/seen-urls-bootstrap.py`：扫 `10-Daily/*.md` 提取 `[原文](url)` 链接 + 关联 `50-Zettel/*.md` 的 frontmatter `source_url`，构造完整 _seen-urls 节点。**默认不扫 target_date 当天**（避免循环）。
2. SKILL.md Phase 0 加自检：
   ```bash
   if [ ! -f 00-Inbox/_seen-urls.json ]; then
     python3 scripts/seen-urls-bootstrap.py --target-date=$TARGET_DATE --window-days=30
   fi
   ```

**成本**：50 min（30 min 脚本 + 20 min 改 SKILL）
**收益**：cold start 自动化，避免手写脚本（约 30 天一次）
**紧迫**：低（30 天一次频率不高，且当前 _seen-urls 已健康）

---

### A6 · digester 9 分钟性能诊断

**问题**：digester 跑 530s / 59K tokens / 6 个 tool_uses，输出 13K 字符 markdown。每条 14 秒，超出单条 summary 合理时间。

**诊断方向**：
1. spawn digester 时 prompt 加 `请用最少思考链` 看是否减时
2. agent system prompt 是否要求反复读 cluster.json 或 zettel？看 tool_uses=6 是什么操作
3. 是否在循环 self-check（system prompt 6 项自检的 LLM 实现可能慢）

**可能优化**：
- self-check 改成机械校验（脚本验证 url 去重 / wikilinks 不存在 / 等），不让 LLM 做
- 类似 cluster 思路，digester 输出"章节大纲 + 关键洞察"精简 JSON，主会话拼装 markdown

**成本**：60 min（诊断 + 可能改造）
**收益**：可能省 4-5 分钟/天，但风险高（可能没明显瓶颈）
**紧迫**：低（性能可观察但非阻塞）

---

### A7 · a16z LC 评论压成"📌 边角条"渲染

**问题**：6-29 跑 a16z 3 条评论（low_confidence + zettel_worthy=false）全进 applications 桶平铺，与"7000 万用户 Revolut 银行 ML 部署"这种真案例混在一起。Daily 阅读体验被稀释。

**实施**：
1. 改 `news-writer.md` system prompt 渲染规则：
   - 当一个 topic 内 LC 条目 ≥ 1 时，topic 段内拆 "## 主要" + "## 📌 边角观察" 两个子段
   - 边角条用更紧凑的渲染（标题 + 一句 rationale，无 frontmatter 表头）
2. 改 filter-criteria.md §5 文档化新渲染约定

**成本**：30 min 改 + 15 min 试跑
**收益**：Daily 阅读节奏改善，applications 桶不再杂质
**紧迫**：低（功能正常，UX 优化）

---

### A8 · Phase 6 Log 模板化 `scripts/build-log.py`

**问题**：当前 SKILL.md Phase 6 规定"主会话内联"写 99-Log/${TARGET_DATE}-run.md。每次跑 LLM 手写 100+ 行 markdown——浪费 token + 易出错（如本次 A2 误判 meta-ai-blog 状态就因人工读 sources.md 漏看）。

**实施**：
1. 新建 `scripts/build-log.py`：
   - 输入：filtered.json + cluster.json + writer-output.json + digester-output.json
   - 自动从文件读 stats + Phase timing + source 详情（包含从 sources.md 读 reliability）
   - 渲染 markdown 模板
2. SKILL.md Phase 6 改：主会话调脚本，不再手写

**成本**：60-90 min（脚本 + 模板 + SKILL 改）
**收益**：每天省 5-10 min 主会话手写；格式一致；source 状态从配置自动读不靠记忆
**紧迫**：中（长期收益高，但单次投入大）

---

### A9 · writer agent 降级试 sonnet 4.5 / haiku

**问题**：writer 跑 11m32s / 96K tokens。但 writer 是创作类工作（Daily 段落 + Zettel 正文），降级风险高。

**实施**：
1. 先备份当前 writer 输出（6-29 落盘的 9 张 Zettel 作为基线）
2. 改 `news-writer.md` `model: sonnet → sonnet 4.5`（如果有较小 sonnet 版本）或 haiku 试跑一次同样的 cluster.json
3. 人工对比 Zettel 内容质量 + Daily 渲染美感

**成本**：1 min 改 + 30 min 试跑 + 人工对比
**收益**：可能省 5 分钟/天，但内容质量可能下降
**紧迫**：低（更激进的优化，先看 A1 haiku 实测再判断）

---

### A10 · ~~filter-inline.py 写 pytest 单元测试~~

**决定**：不做。个人 vault 项目 overkill。`filter-inline.py` 已 dry-run + 真数据验证两次，规则改动频率低。回归测试靠每次跑后人工 review stats 即可。

---

## 决策原则

- **优先做**：成本 ≤ 30 min + 收益 ≥ 3 min/天 + 风险低
- **延后做**：成本 > 60 min 或风险高（如降级 writer model）
- **不做**：成本 > 90 min 且收益不明（如 A10）

## 与 v2.3 commit 链的对照

- v2.1 `9e050c2`：IPC 文件契约 + cluster is_new 严格判定
- v2.2 `60ddde7`：跨日去重 + a16z 脚本 fetcher
- v2.3 `fb92607`：filter/cluster 解决 32k 截断（架构）
- v2.3 `9b2da71`：6-29 首次成功跑通（产物）
- v2.3 `beeffcd`：A1+A3 cluster haiku + schema 加严

A4-A9 一旦实施，会以 `refactor(ai-news): A<N> ...` 命名 commit，便于在 git log 中按编号回查。
