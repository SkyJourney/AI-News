# /ai-news skill 演化 Roadmap

> 跟踪 v2.4 后续大方向：**F1 全量离线化**（60-Originals 层）→ **F2 前端站点**（私有化 docker 部署）。
> 老 v2.3 遗留优化项（A4-A9）按新方向做了合并/升级/改造，不再独立编号——见「合并说明」小节。
> 编号沿用 A/F/B 前缀，便于回查 [[2026-06-29-run]] / [[2026-07-01-run]] log 与 commit 历史。

最后更新：2026-07-02 · **F2 重启：Quartz 弃用 · 迁 Astro 5 自主前端完成** + 内容质量优化补丁（`83c20b2`）+ F2.7 本地 Docker 部署 + F2.8 生产化 6/7 项

---

## 已完成（v2.3 → v2.4 落地）

- **A1** cluster agent `sonnet → haiku`（commit `beeffcd`）
- **A2** ~~sources.md meta-ai-blog reliability~~ —— 撤销（Log 误判）
- **A3** cluster agent schema 加严：`topic_slug` / `is_new` 必填（commit `beeffcd`）
- **v2.4** fetcher IPC 改 Write 中转，根治 3 类边界 bug（commit `08cffbb`）
- **调度自动化**：Mac mini 定时任务 + Claude 非交互会话跑通（不再需要 launchd 独立配置）
- **F2.0** 框架 POC（2026-07-01，commit tbd）：~~采用 Quartz 5~~ —— **决策已推翻**（见下 F2 重启小节）。POC 报告仍归档：[`.claude/skills/ai-news/notes/F2.0-poc-report.md`](../../.claude/skills/ai-news/notes/F2.0-poc-report.md)。副产品：news-originalizer.md YAML frontmatter bug（`original_title` 含冒号未加引号）已修。
- **F2 重启：迁 Astro 5**（2026-07-02，commit `e992215`）：F2.4 Lumina 内容层接管走 Quartz override 路径实证失败（架构性 3 层 hack + 大小写目录重复 + trailing-slash 404 + 视觉严重偏离设计稿），彻底放弃 Quartz 框架，改 Astro 5 独立自主前端。M0-M6 全通：83 页 build 805ms · 11/11 route 200 · LAN `192.168.50.253:8801` 部署 · vault 5 collection + zod schema + backlinks 反向 map + Lumina 49 CSS 变量继承。详见 [`.claude/skills/ai-news/notes/F2-astro-completion-report.md`](../../.claude/skills/ai-news/notes/F2-astro-completion-report.md)。F2.4 决策上下文归档到 [`.claude/skills/ai-news/notes/_archive/`](../../.claude/skills/ai-news/notes/_archive/)。
- **F2 内容质量优化补丁**（2026-07-02，commit `83c20b2`）：originals 图片资产接入 build（`scripts/sync-assets.mjs` 物理复制 + `vault-loader.ts` 路径重写 `_assets/` → `/originals-assets/`，修复此前图片全部 404）；zettel 瀑布流 `<a>` 嵌套 `<a>` 布局撕裂修复；Zettel frontmatter 加 `title`/`title_original` 中文标题字段并回填 59 篇历史 Zettel；Topic 日期聚合改倒序并重排 11 篇历史文件；**D17** conda 环境固定（独立 env `ai-news`，根治 python3 版本漂移）+ **D18** originals 抓取域名级 UA override。详见 [[decisions#D17]] / [[decisions#D18]]。
- **F2.7 本地 Docker 部署**（2026-07-02，commit `412159b`）：内网穿透明确划出范围，收窄为纯 LAN 本地部署。首版新增 `web/frontend/Dockerfile`（node:22-alpine builder）+ `web/docker-compose.yml`（builder profile 只读挂载 vault 5 目录 + nginx 常驻服务）+ `web/nginx.conf`（pretty URL try_files）。SKILL.md 新增 **Phase 8 · Publish**（Phase 7 Git Sync 之后，独立于 git push 结果）。本地验证：137 页 build 通过，`localhost:8801` 与 LAN `192.168.50.253:8801` 全路由 200（含图片资产）。**⚠️ 已被下面的部署编排重构取代**：build 阶段的 Docker 化被判断是过度设计，`Dockerfile`/`docker-compose.yml`/`nginx.conf` 三件套已改为「本地 npm run build + rsync 到 `/Volumes/Docker/data/ainews/` + compose 挪到 `/Volumes/Docker/compose/ainews/` 只跑 nginx」；第二轮又把 rsync/compose up/冒烟测试从 SKILL.md 里抽成外部 `deploy.sh` + 仓库根 `.env` 指针，见「部署编排」小节。
- **F2.8 生产化 6/7 项**（2026-07-02，3 个独立 commit，逐批 build + Docker + Playwright 实测）：
  - 批次1 `a0d5b71`：wikilink 断链检测（`remarkWikiLink` 改异步插件 await 全库缓存判定，命中 tokens.css 里预埋已久但从未接上的 `a.wikilink.broken` 样式）+ hover 预览（内联 `data-preview-title/excerpt`，popover 用安全 DOM 方法拼节点）。踩坑：同步存取器读到了 astro.config.mjs 与 content.config.ts 两条 import 链各自独立的模块实例，改异步 `await getVaultCache()` 才规避
  - 批次2 `3d38682`：深色模式（tokens.css `[data-theme='dark']` 全套覆盖 + FOUC 防护 inline script + document 级事件委托的切换按钮，适配 ClientRouter 每次导航重渲染 Header）+ Article Progress（originals 详情页右栏滚动进度条 Preact island）+ 字体 self-host（`@fontsource/geist-sans` + `@fontsource/inter` + `@fontsource/ibm-plex-mono` + `material-symbols` 取代 Google Fonts CDN）
  - 批次3 `6bc9411`：Pagefind 全文搜索（`GlassSearchBar.tsx` 从 alert 桩改真实浮层，`createPortal` 挂 `document.body` 绕开 Header `backdrop-filter` 的 fixed 定位包含块问题；excerpt 高亮不用 `dangerouslySetInnerHTML`，改正则拆分 `<mark>` + 手动解码实体后走 Preact 安全文本节点）
  - **Bases 视图迁移降为 v2 之后再看**：4 个 `.base` 文件（by-source/by-topic/latest-daily/originals）本质是面向运营的内部分组视图，非面向读者的站点功能，暂不占 F2.8 工时

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

**目标**：本地 docker compose 起 nginx，把 vault 转成前端可访问的站点。GitHub 做内容管理，前端页面做展示。**私有化部署**在 Mac mini 本地，LAN 内访问——2026-07-02 明确**不做内网穿透/公网暴露**，范围收窄为纯本地部署。

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

### 部署编排（已实现，见 `/Volumes/Docker/compose/ainews/docker-compose.yml`）

> **build 不进 Docker**：`npm run build` 直接在宿主机本地 Node 环境跑（跟本次会话里一直在用的方式一样），产物用 `rsync -a --delete` 同步进 `/Volumes/Docker/data/ainews/`。`astro build` 每次自动清空 `dist/` 陈旧文件，`rsync --delete` 兜底同步删除，不会有旧页面残留。
>
> **Docker 只用来跑 nginx**：compose 文件 + `nginx.conf` 不放仓库内，统一放本机 Docker 编排目录 `/Volumes/Docker/compose/ainews/`（与其他本机项目同构，如 `panwatch`/`fundval-live`）；数据放 `/Volumes/Docker/data/ainews/`（同样与其他项目同构）。顶层 `name: ainews-web` 钉死 project 名。**更新就是一次 rsync，nginx 容器永远不用重建/重启**（`up -d` 只在首次部署或宿主机重启后才真正生效）。
>
> 曾经设计过"builder 容器 + 具名 Docker volume"的方案（`web/frontend/Dockerfile` + `ainews-web-builder` 镜像），实测后判断是过度设计——build 阶段引入 Docker 除了环境隔离没有额外收益，却换来"每次都要过一遍镜像 build/run"的复杂度，已撤销（Dockerfile/.dockerignore 已删）。
>
> **发布逻辑进一步与仓库/skill 解耦**：rsync + 确保 nginx 在跑 + 冒烟测试这段封进 `/Volumes/Docker/compose/ainews/deploy.sh`（不进仓库）；仓库根 `.env`（不进 git，见 `.env.example`）只存一行 `AINEWS_DEPLOY_SCRIPT=/Volumes/Docker/compose/ainews/deploy.sh` 指针。SKILL.md 因此不硬编码任何 `/Volumes/Docker/...` 路径——换机器只需要重新写一份 `.env`，deploy.sh 内部细节对 skill 完全透明。

- `web`（`nginx:alpine` 常驻，容器名 `ainews-web`）：只读挂载 `/Volumes/Docker/data/ainews:/usr/share/nginx/html` + `nginx.conf`，端口 `8801:80`
- `deploy.sh`：接收一个 dist 目录参数，`rsync -a --delete` 到数据目录 → `docker compose up -d web`（幂等）→ `curl` 冒烟，失败非 0 退出

**访问方式**：`http://localhost:8801/` / LAN `http://192.168.50.253:8801/`（**范围内不做公网暴露**）

### 与 skill 集成（Phase 8 · Publish，已实现见 SKILL.md）

```
Phase 6 Log → Phase 7 Git Sync → Phase 8 Publish
                                       ↓
                    npm run build（本地 Node，不进 Docker，仓库自己的事）
                                       ↓
        source .env → "$AINEWS_DEPLOY_SCRIPT" <dist目录>
                                       ↓
          （脚本内部：rsync --delete → docker compose up -d web → curl 冒烟）
```

Phase 8 独立于 Phase 7（不依赖 git push 是否成功，直接读本地工作区当前内容）。

### 任务拆解

| # | 任务 | 成本 | 输出 |
|---|---|---|---|
| **F2.0** | ~~框架 POC~~ —— 决策已推翻，见下 | — | 归档到 `notes/F2.0-poc-report.md` |
| ~~F2.1-F2.4~~ | Quartz 5 vendor + Docker 部署 + wikilink + Lumina 视觉 | — | **全撤销** |
| **F2 重启 M0-M6** | ✅ Astro 5 独立自主前端 + Preact islands + Tailwind 4 + vaultLoader + 5 collection + 5 列表页 + 5 详情页 + / landing + LuminaBacklinks 分栏 + Lumina 49 tokens | ~40 min（含探索） | `web/frontend/` + 83 页 build + 报告 `notes/F2-astro-completion-report.md` |
| **F2.7** | ✅ nginx 本地部署（LAN-only，内网穿透已划出范围）+ SKILL.md Phase 8 Publish 编排。**两轮重构**：① build 去 Docker 化，改本地 `npm run build` + `rsync --delete`；② 发布逻辑从 SKILL.md 抽成 `/Volumes/Docker/compose/ainews/deploy.sh`，仓库根 `.env`（不进 git）存一行指针，skill 不再硬编码本机路径 | ~30 min + 两轮重构 ~25 min | `/Volumes/Docker/compose/ainews/{docker-compose.yml,nginx.conf,deploy.sh}` + 仓库根 `.env.example`，137 页 build 通过 · 本地/LAN `8801` 全路由 200 |
| **F2.8** | ✅ 生产化 6/7 项：Wikilink broken link 检测 + hover preview（批次1 `a0d5b71`）· 深色模式 + Article Progress + @fontsource self-host（批次2 `3d38682`）· Pagefind 搜索（批次3 `6bc9411`）。~~Bases 视图迁移~~ 降为 v2 之后再看（面向运营的内部视图，非读者站点功能，见下） | ~2.5 h（3 批次） | 3 个独立 commit，逐批 build + Docker + Playwright 实测通过 |

**F2 已完成**：~40 min（重启后）+ 内容质量优化补丁（`83c20b2`）+ F2.7 本地 Docker 部署（LAN-only，commit `412159b`）+ F2.8 生产化 6/7 项（3 批次）· Sprint 3 主线基本收尾，剩 Bases 视图迁移待评估是否值得做。

---

## 持续 · 边角优化

### A8' · Phase 全流程 Log 模板化（`scripts/build-log.py`）

**背景**：老 A8 想模板化 Phase 6 Log。F1 加 Phase 3.5，F2 加 Phase 8（Phase 7 Git Sync 是既有阶段，非 F2 新增），Log 模板要覆盖全部 10 个 phase 标记（0/1/2/3/3.5/4/5/6/7/8）。

**动作**：F2.8 完成后统一实现，一次覆盖全部 phase。不再单独立项，作为 F2.8 的收尾任务。

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
