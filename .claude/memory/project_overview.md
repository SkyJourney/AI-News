---
name: project_overview
description: AInews 项目定位、技术栈、目录结构、核心组件——新会话 1 分钟建立全局认知
type: project
last_updated: 2026-07-01
commit: 9b48c6a
---

# AInews 项目总览

## 定位

`/Volumes/Projects/AInews` 同时是两件东西：

1. **Obsidian vault**（知识库本体）——AI 资讯的存储、组织、检索层
2. **采集管道**（自动化层）——通过 Claude Code skill + subagent 从 14 个信息源抓取并落盘

两层在仓库内**物理同居、逻辑解耦**：vault 只管"存什么、怎么链"，skill 只管"抓什么、写哪里"。

## 技术栈

| 维度 | 选型 | 备注 |
|---|---|---|
| 知识库 | Obsidian 1.12.7+ | vault id=`5a3c69ef6e15d242`、name=`AInews` |
| 视图 | Obsidian Bases（1.9+ 原生） | 替代 Dataview，frontmatter 即数据 |
| 采集编排 | Claude Code skill | `/ai-news`，`disable-model-invocation: true` |
| 子任务 | Claude Code subagent × 8（含 script fetcher + digester） | 原生 Agent，不依赖第三方 MCP |
| 调度 | Mac mini cron + Claude 非交互 | v2.4 MVP 达成，取代原 launchd 方案 |
| 抓取通道 | WebFetch / Bash + curl / arXiv & HF API | 三路并发 |
| 健康检查 | `scripts/source-health.sh`（bash + curl） | Phase 0 强制门 |
| 版本控制 | 本地 git | 远程未挂载，纯本地工作流 |

## 目录结构

### vault 层（Obsidian 直接看的）

```
/Volumes/Projects/AInews/
├── 00-Inbox/              # Phase 1 fetch JSON 缓存（v2 激活，配套 --from-cache flag）
├── 10-Daily/              # 每日简报（vault 双链版），writer 写
├── 20-Topics/             # 主题汇聚（append 模式），cluster + 人手维护
├── 30-Digests/            # 每日分享/打印版（去 wikilink、URL 展开），digester 写
├── 40-Deep-Dives/         # v2 weekly/monthly digester 预留（≥7 天历史后启用） + 人工专题
├── 50-Zettel/             # 原子卡，时间戳 ID（YYYYMMDDHHmm-slug）
├── 90-Archive/            # 人工归档
├── 99-Log/                # 运行日志，每次 /ai-news 写一份
├── _base-by-topic.base    # Bases 视图：按主题分组
├── _base-by-source.base   # Bases 视图：按 source 切片
├── _base-latest-daily.base# Bases 视图：Daily 时间线 + 健康监控
├── MOC.md                 # vault 总览导航（人工维护）
├── SCHEMA.md              # vault 落盘根公约（AI 写文件前必读）
└── README.md              # 项目说明
```

> ⚠️ **vault 内没有 `30-Sources/`**——信息源元数据全部归 skill `references/sources.md` 单一权威，避免双写漂移。

### 工具层（`.claude/`，Obsidian 默认不索引）

```
.claude/
├── skills/ai-news/
│   ├── SKILL.md                       # 7 phase 编排（Preflight→Fetch→Filter→Cluster→Write→Digest→Log→Git Sync）
│   ├── references/
│   │   ├── sources.md                 # 14 源单一权威清单
│   │   ├── blacklist.md               # 死源黑名单（防"想当然"加回）
│   │   ├── vault-schema.md            # writer/digester 镜像参考（与 vault/SCHEMA.md 同步）
│   │   └── filter-criteria.md         # 过滤/聚类/打标准则
│   └── scripts/
│       ├── source-health.sh           # 全源活性检查（curl 并发）
│       ├── arxiv-fetch.py             # arXiv API 封装（3 秒限流）
│       └── test-fetcher.sh            # 单源调试入口
├── agents/                            # 8 个原生 subagent
│   ├── news-fetcher-rss.md
│   ├── news-fetcher-api.md
│   ├── news-fetcher-webfetch.md
│   ├── news-fetcher-script.md         # v2.2 新增：调 scripts/ 内专用抓脚本（a16z）
│   ├── news-filter.md                 # DEPRECATED（v2.3 起 Phase 2 改主会话内联 filter-inline.py）
│   ├── news-cluster.md
│   ├── news-writer.md
│   └── news-digester.md               # v2 新增：cluster topics → 30-Digests 分享版
└── memory/                            # 本目录，跨会话持久化
```

## 未来层指针（尚未落地）

| 层 | 位置 | 引入时机 | 详见 |
|---|---|---|---|
| 60-Originals | vault 根 | F1 落地后 | [[decisions#D14]] · ROADMAP Sprint 1 |
| web/ | 仓库根 | F2 落地后 | [[decisions#D14]] · ROADMAP Sprint 3 |
| news-originalizer.md | `.claude/agents/` | F1 落地后 | ROADMAP F1.2 |

## 核心组件职责

| 组件 | 职责 | 关键约束 |
|---|---|---|
| `/ai-news` skill | 7 阶段总编排，参数解析、Phase 0 健康门、Phase 1 并发 + retry + inbox 缓存 | 仅手动触发；alive 源 < 3 暂停问用户；支持 `--from-cache` |
| `news-fetcher-rss/api/webfetch` | 抓单源、输出 entry JSON | 必带 `low_confidence` 字段；不主观拒绝 |
| `news-filter` | 去重 + 信噪过滤 | 读 `filter-criteria.md` 决策 |
| `news-cluster` | 主题分桶，标 `zettel_worthy` | ≥ 2 条才独立成桶；自动创建新 topic |
| `news-writer` | 写 Daily / Topic / Zettel（vault 双链版） | frontmatter 必齐；Daily 写"昨日回顾"段 |
| `news-digester` | 写 30-Digests 分享版（去 wikilink、URL 展开） | 与 writer 并列消费 cluster topics；含事实性硬约束自检 |
| Obsidian Bases | 动态视图（按主题 / source / 时间线） | frontmatter 即数据源 |

## 信息源池（14 个，1 个 degraded）

按 tier 分层（详见 [[reference]] 与 `.claude/skills/ai-news/references/sources.md`）：

- **Tier 1 主力**（4）：OpenAI / DeepMind / arXiv API / HuggingFace Daily Papers
- **Tier 2 聚合分析**（4）：Import AI / Interconnects / 量子位 / Air Street Press
- **Tier 3 WebFetch 兜底**（6）：Anthropic / Meta AI / The Batch / 机器之心 / a16z / State of AI
  - `meta-ai-blog` reliability=degraded（80+ 天无更新）
  - `state-of-ai` 是"事件锁集"型源（平日 0 条正常）

## 触发与调试

| 操作 | 命令 |
|---|---|
| 全量跑今天 | `/ai-news` |
| 指定日期 | `/ai-news --date=YYYY-MM-DD` |
| 仅健康检查 | `/ai-news --dry-run`（只跑 Phase 0） |
| 单源调试 | `bash .claude/skills/ai-news/scripts/test-fetcher.sh <name>` |
| 全源活性 | `bash .claude/skills/ai-news/scripts/source-health.sh` |

## 相关记忆

- [[project_progress]] — 已落地阶段与待办
- [[decisions]] — 关键架构决策与理由
- [[feedback]] — 协作规范
- [[reference]] — 外部资源指针
