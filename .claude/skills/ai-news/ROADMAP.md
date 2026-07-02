# /ai-news skill 演化 Roadmap

> 跟踪 v2.4 后续大方向：**F1 全量离线化**（60-Originals 层）→ **F2 前端站点**（私有化 docker 部署）。
> 老 v2.3 遗留优化项（A4-A9）按新方向做了合并/升级/改造，不再独立编号——见「合并说明」小节。
> 编号沿用 A/F/B 前缀，便于回查 [[2026-06-29-run]] / [[2026-07-01-run]] log 与 commit 历史。

最后更新：2026-07-02 · **F2 重启：Quartz 弃用 · 迁 Astro 5 自主前端完成**

---

## 已完成（v2.3 → v2.4 落地）

- **A1** cluster agent `sonnet → haiku`（commit `beeffcd`）
- **A2** ~~sources.md meta-ai-blog reliability~~ —— 撤销（Log 误判）
- **A3** cluster agent schema 加严：`topic_slug` / `is_new` 必填（commit `beeffcd`）
- **v2.4** fetcher IPC 改 Write 中转，根治 3 类边界 bug（commit `08cffbb`）
- **调度自动化**：Mac mini 定时任务 + Claude 非交互会话跑通（不再需要 launchd 独立配置）
- **F2.0** 框架 POC（2026-07-01，commit tbd）：~~采用 Quartz 5~~ —— **决策已推翻**（见下 F2 重启小节）。POC 报告仍归档：[`.claude/skills/ai-news/notes/F2.0-poc-report.md`](../../.claude/skills/ai-news/notes/F2.0-poc-report.md)。副产品：news-originalizer.md YAML frontmatter bug（`original_title` 含冒号未加引号）已修。
- **F2 重启：迁 Astro 5**（2026-07-02，commit tbd）：F2.4 Lumina 内容层接管走 Quartz override 路径实证失败（架构性 3 层 hack + 大小写目录重复 + trailing-slash 404 + 视觉严重偏离设计稿），彻底放弃 Quartz 框架，改 Astro 5 独立自主前端。M0-M6 全通：83 页 build 805ms · 11/11 route 200 · LAN `192.168.50.253:8801` 部署 · vault 5 collection + zod schema + backlinks 反向 map + Lumina 49 CSS 变量继承。详见 [`.claude/skills/ai-news/notes/F2-astro-completion-report.md`](../../.claude/skills/ai-news/notes/F2-astro-completion-report.md)。F2.4 决策上下文归档到 [`.claude/skills/ai-news/notes/_archive/`](../../.claude/skills/ai-news/notes/_archive/)。

---

## Sprint 1 · F1 · 60-Originals 全量离线化

**目标**：在 vault 加一层 `60-Originals/`，每天把 **10-Daily + 30-Digests 清单上的所有条目**的原文全文抓下来，规整成中文模板，供 10/20/40/50 全链路双链引用。产出后 vault 变成**自包含**，不依赖外部 URL。

### 设计要点

- **触发时机**：Phase 3 Cluster 之后新增 **Phase 3.5 Originalize**，遍历 cluster.json 里所有 `kept=true` 条目 spawn `news-originalizer`
- **命名**：`60-Originals/YYYY-MM-DD-HHMM-<slug>.md`，与 Zettel ID 同源（同 HHMM）便于精确配对
- **翻译模型**：`haiku`（够用，不需要深度推理）
- **翻译准则**：保留原文所有观点/细节/数据/专有名词；专有名词保留原词加括号中文解释
- **图片策略**（三级降级）：
  1. HTML `<img>` 有 URL → 下载到 `60-Originals/_assets/YYYY-MM-DD/<id>-<n>.<ext>`
  2. 下载失败（403/超时/CDN 挡）→ 保留原图 URL + 用 `alt`/`figcaption`/周围文字生成一句中文描述
  3. arXiv PDF 图无法抽 → 用 `> _图 Figure N：<描述>_` 占位 + 论文页锚点
- **frontmatter 追踪图片状态**：`images_attempted` / `images_saved`
- **失败不阻塞**：某条抓取失败仅标注 `fallback_notice`，不影响其他条目和后续 phase

### 模板

```yaml
---
id: YYYY-MM-DD-HHMM-<slug>
type: source-original
title: <中文标题>
original_title: <原文标题>
source_name: <sources.md 里的 name>
source_url: <原文 URL>
author: [<作者列表>]
published_at: YYYY-MM-DD
fetched_at: YYYY-MM-DDTHH:MM:SSZ
language: zh|en|...
translated: true|false
translation_engine: haiku
word_count: <int>
images_attempted: <int>
images_saved: <int>
related_zettels: [[...]]
related_topics: [[...]]
related_daily: [[YYYY-MM-DD]]
tags: [source-original, <language-*>]
---

# <中文标题>

> 原文：[<原文标题>](<source_url>) · <source_name> · <published_at>
> 抓取：<fetched_at> · 翻译：<engine> · <word_count> 字

## <一级标题按原文结构>
...
```

### 任务拆解

| # | 任务 | 成本 | 输出 |
|---|---|---|---|
| **F1.1** | vault schema 更新：60 目录约定 + `_assets/` 图片规范 + 命名规则 + 模板 | 30 min | `SCHEMA.md` + `references/vault-schema.md` 双份改动 |
| **F1.2** | `news-originalizer.md` subagent + `scripts/fetch-with-assets.py`（含图片下载） + `scripts/arxiv-fulltext.py`（HTML 版优先 + PDF 回退） | 150 min | 1 个 agent + 2 个脚本 |
| **F1.3** | SKILL.md 加 Phase 3.5 编排（cluster 后 spawn originalizer 并发池） + cluster.json schema 加 `original_id` 字段 | 60 min | SKILL 编排改动 |
| **F1.4** | 下游改造：news-writer 双链改 `[[60-Originals/<id>]]`；news-digester 可读 60 全文替代 cluster 摘要；MOC 加 60 层入口；3 个 `.base` 加 language/source_name 视图 | 90 min | 3 个 agent + MOC + `.base` |
| **F1.5** | 冷启动脚本升级 `scripts/seen-urls-bootstrap.py`：扫 10-Daily + 60-Originals 反推 _seen-urls（**吞并老 A5**） | 45 min | 1 个脚本 |
| **F1.6** | 全流程试跑 + 校准（挑一天回放，人工审 3-5 篇原文质量） | 60 min | 一次真跑 + Log 分析 |
| **A4'** | cluster-merge.py 按 source 默认 topic 兜底表（**升级 P-中**，F1 后所有 kept 条目要绑 topic，兜底重要性↑） | 30 min | 脚本改动 |

**F1 总投入**：~7.5 小时，可切成 3-4 个开发日。

---

## Sprint 2 · F1 后评估（~2h）

F1 落地后 pipeline 输入/输出结构都变了，几个待定项需要重新画像再决策：

### B1 · digester 重构评估

**背景**：老 A6 想诊断 digester 9 分钟性能。F1 后 digester 可以直接读 60-Originals 全文替代原来的 cluster 摘要，输入结构完全不同——**不是简单优化，是重构**。

**动作**：
1. F1 落地后跑一次，测新的 digester 时长 / token / tool_uses
2. 若时长 > 5 min：考虑改造为"读 60-Originals 摘要区（前 500 字）+ zettel_worthy 条目 TL;DR"的精简输入
3. 决定 system prompt 是否移除 LLM self-check（改机械校验脚本）

**成本**：60 min 评估 + 可能 60 min 改造

### A9' · writer 降级二次评估

**背景**：F1 后 writer 责任变小（不再嵌大量原文，改双链），复杂度下降。老 A9 因质量风险搁置。

**动作**：F1 稳定 3 天后，试跑 `sonnet 4.5` 或 `haiku`，对比 Zettel 质量。

**成本**：30 min 试跑 + 人工对比

---

## Sprint 3 · F2 · Vault 前端站点

**目标**：本地 docker compose 起 nginx，把 vault 转成前端可访问的站点。GitHub 做内容管理，前端页面做展示。**私有化部署**在 Mac mini 本地，后续通过内网穿透暴露公网。

### 需求（框架无关）

**必备**：
- **Markdown 解析**：CommonMark + GFM（表格、任务列表、脚注）
- **Vault 双链解析**：Wikilink `[[filename]]` / `[[filename|alias]]` / `[[filename#heading]]` → 站内 HTML 链接
- **反向链接**：每页底部展示"被谁引用"列表
- **Frontmatter 感知**：title / published_at / tags / related_* 字段驱动路由和聚合
- **主题化排版**：Typography 友好，代码块高亮，Callout 支持
- **自适应布局**：桌面 + 平板 + 手机三档
- **私有内容过滤**：排除 `.claude/` / `_archive/` / `99-Log/` / frontmatter `visibility: private` / tag `private`

**加分**：
- Pagefind 静态全文搜索（无需后端）
- Backlinks 图谱（Cytoscape / D3）
- RSS 输出（`/rss.xml`）
- OG image 自动生成
- 阅读时长估算
- 深色模式

### 路由设计

```
/                    → 首页（最新 Daily + 主题速览 + 站点地图）
/daily/[date]        → 每日简报（10-Daily）
/topics/[slug]       → 主题聚合（20-Topics）
/digests/[date]      → 每日分享版（30-Digests）
/deep-dives/[slug]   → 深度专题（40-Deep-Dives）
/zettel/[id]         → 原子卡（50-Zettel）
/originals/[id]      → 原文全文（60-Originals，F1 落地后启用）
/tags/[tag]          → 标签聚合
/sources/[name]      → 按信息源聚合（读 sources.md）
/search              → Pagefind
/rss.xml             → RSS 输出
```

### 框架候选（实施时详细比对）

| 候选 | 亮点 | 待验证 |
|---|---|---|
| Quartz 4 | 专为 Obsidian vault 设计，wikilink/backlinks/graph 全内置 | 主题定制灵活度 |
| Astro | 通用性强、生态丰富、SSG 首选 | wikilink 需自写 remark 插件 |
| Hugo | 极致构建速度 | Go template 学习曲线 |
| Zola | 单二进制部署简单 | 生态较小 |
| Docusaurus | 文档站成熟 | 偏 API 文档、内容站定制 |

**实施时**：先 POC 三个候选各半天，对比 wikilink 解析 + 部署产物 + 主题空间，再定。

### Docker Compose 编排

```yaml
# docker-compose.yml
services:
  builder:
    build: ./web             # Dockerfile: node + <chosen-framework>
    volumes:
      - .:/vault:ro           # vault 只读挂载
      - web-static:/output
    command: ["npm", "run", "build"]
    profiles: ["build"]       # 默认不启，靠 skill Phase 7 触发

  web:
    image: nginx:alpine
    ports:
      - "40801:80"            # 本机 localhost:40801 / 内网 192.168.50.253:40801
    volumes:
      - web-static:/usr/share/nginx/html:ro
      - ./web/nginx.conf:/etc/nginx/conf.d/default.conf:ro
    restart: unless-stopped

volumes:
  web-static:
```

**访问方式**：
- 开发/自用：`http://localhost:40801` / `http://192.168.50.253:40801`
- 公网：后续接内网穿透网关（frp / cloudflare tunnel / tailscale funnel）

### 与 skill 集成（新增 Phase 7 · Publish）

```
Phase 5 Digest → Phase 6 Log → Phase 7 Publish（新增）
                                    ↓
                     docker compose --profile build run --rm builder
                                    ↓
                          curl -sf http://localhost:40801/ >/dev/null
```

Phase 7 只是两行 bash：build + smoke test。skill 跑完自动更新站点，端到端闭环。

### 任务拆解

| # | 任务 | 成本 | 输出 |
|---|---|---|---|
| **F2.0** | ~~框架 POC~~ —— 决策已推翻，见下 | — | 归档到 `notes/F2.0-poc-report.md` |
| ~~F2.1-F2.4~~ | Quartz 5 vendor + Docker 部署 + wikilink + Lumina 视觉 | — | **全撤销** |
| **F2 重启 M0-M6** | ✅ Astro 5 独立自主前端 + Preact islands + Tailwind 4 + vaultLoader + 5 collection + 5 列表页 + 5 详情页 + / landing + LuminaBacklinks 分栏 + Lumina 49 tokens | ~40 min（含探索） | `web/frontend/` + 83 页 build + 报告 `notes/F2-astro-completion-report.md` |
| **F2.7** | Docker Compose + nginx + 内网穿透（frp / cloudflare tunnel）+ 端到端验证 | 3 h | 公网可访问 |
| **F2.8** | 生产化：@fontsource self-host + pagefind 搜索 + 深色模式 + Article Progress + Wikilink hover preview | 4 h | v2 二级功能 |

**F2 已完成**：~40 min（重启后）· 剩 F2.7 + F2.8 待做。

---

## 持续 · 边角优化

### A8' · Phase 全流程 Log 模板化（`scripts/build-log.py`）

**背景**：老 A8 想模板化 Phase 6 Log。F1 加 Phase 3.5，F2 加 Phase 7，Log 模板要覆盖全部 8 phase（0/1/2/3/3.5/4/5/6/7）。

**动作**：F2.6 完成后统一实现，一次覆盖全部 phase。不再单独立项，作为 F2.6 的收尾任务。

---

## 合并说明（老 A4-A9 归宿）

| 老编号 | 新归宿 | 变化 |
|---|---|---|
| A4 | **A4'**（Sprint 1 收尾） | P-低 → P-中，兜底表在 F1 全量抓取下更关键 |
| A5 | **F1.5** 吞并 | 冷启动脚本要同时扫 10-Daily + 60-Originals，一次写完 |
| A6 | **B1**（Sprint 2） | 从"性能诊断"改造为"输入结构变化后的重构评估" |
| A7 | **F2.3** 吞并 | 从 markdown 层拆段改到前端组件层区分，效果更好 |
| A8 | **A8'**（F2.6 收尾） | 覆盖全部 8 phase，与 F2 集成一次做完 |
| A9 | **A9'**（Sprint 2） | 保留 P-最低，F1 后 writer 责任变小，降级风险下降 |
| ~~A10~~ | 保持不做 | 个人 vault 项目 overkill |

---

## 决策原则

- **优先做**：F1 / F2 主线任务
- **合并做**：老 A 系列凡与新方向有交叉的，一次做完（省一次改）
- **延后做**：需要 F1 或 F2 落地后才能画像的评估类（B1 / A9'）
- **不做**：与主线正交、单次 ROI 低于 5 min/天的（部分 A10 类）

---

## 与 commit 链的对照

- v2.1 `9e050c2`：IPC 文件契约 + cluster is_new 严格判定
- v2.2 `60ddde7`：跨日去重 + a16z 脚本 fetcher
- v2.3 `fb92607`：filter/cluster 解决 32k 截断（架构）
- v2.3 `9b2da71`：6-29 首次成功跑通（产物）
- v2.3 `beeffcd`：A1+A3 cluster haiku + schema 加严
- v2.4 `08cffbb`：fetcher IPC 改 Write 中转
- v2.4 `5efad3b`：7-01 自动跑 20 Zettel/9 Topic/digest（MVP 达成）
- F1.x：`feat(ai-news): F1.<n> ...` 命名 commit
- F2.x：`feat(web): F2.<n> ...` 命名 commit
- B1 / A4' / A8' / A9'：`refactor(ai-news): <编号> ...` 命名 commit

一旦实施，编号命名让 git log 按前缀可回查。
