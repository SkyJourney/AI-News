---
name: reference
description: AInews 外部资源、CLI 边界、调试入口、信息源指针——按需加载
type: reference
last_updated: 2026-06-27
commit: d729cc9
---

# AInews 外部参考

> 本文件聚合"不放在记忆里就要去翻代码/手册"的零碎事实。按主题分组，需要时按需加载。

---

## R1：Obsidian CLI 能力边界

**版本**：1.12.7+，路径 `/usr/local/bin/obsidian` → `/Applications/Obsidian.app/Contents/MacOS/obsidian-cli`

### 关键事实

- CLI 是**运行中桌面应用的"遥控器"**，不是独立 headless 工具
- 应用没跑时所有命令报 `unable to find Obsidian`
- 命令语法：`obsidian <command> [key=value ...]`
  - `file=` 按 wikilink 名解析
  - `path=` 按精确路径
  - agent 输出建议加 `format=json`

### 不能做什么

- ❌ **无法创建/注册全新 vault**——`vault` 相关命令只有 `vault`(看信息) / `vaults`(列出) / `vault:open`(仅 TUI 切换**已有** vault)
- ❌ "从 CLI 把普通文件夹开成 vault" 是官方**尚未实现的功能请求**

### 注册新 vault 的唯一路径

由 Obsidian 应用本体首次"以文件夹打开为 vault"完成：
- GUI 操作，或
- `open "obsidian://open?path=<dir>"` 触发后人工点确认弹窗

---

## R2：AInews vault 标识

首次注册：2026-06-27

| 字段 | 值 |
|---|---|
| name | `AInews` |
| id | `5a3c69ef6e15d242` |
| path | `/Volumes/Projects/AInews` |
| active | true |

`.obsidian/` 内入库共享配置：`app.json` / `appearance.json` / `core-plugins.json`
（其余 `workspace*.json` 被 `.gitignore` 忽略）

---

## R3：信息源元数据位置

**单一权威清单**（不在 vault 内）：

```
.claude/skills/ai-news/references/sources.md
```

14 个源完整登记，含 `name / tier / perspective / fetch_method / url / reliability / last_verified / notes`。

**配套文件**：

| 文件 | 用途 |
|---|---|
| `references/blacklist.md` | 死源黑名单（防"想当然"加回） |
| `references/filter-criteria.md` | 过滤/聚类/打标准则（含 §5 Tags 规范） |
| `references/vault-schema.md` | `/ai-news` 内部镜像参考，与 vault 根 `SCHEMA.md` 同步 |

### Tier 分布速查

- **Tier 1**（4）：openai-rss / deepmind-rss / arxiv-api / huggingface-daily-papers
- **Tier 2**（4）：import-ai / interconnects / qbitai / air-street-press
- **Tier 3**（6）：anthropic / meta-ai-blog / the-batch / jiqizhixin / a16z / state-of-ai
  - `meta-ai-blog` reliability=degraded
  - `state-of-ai` 是事件锁集型（平日 0 条正常）

---

## R4：调试入口

### 全源活性检查

```bash
bash /Volumes/Projects/AInews/.claude/skills/ai-news/scripts/source-health.sh
```

返回 JSON：`{alive: [...], dead: [...]}`，被 `/ai-news` Phase 0 强制调用。

### 单源调试

```bash
bash /Volumes/Projects/AInews/.claude/skills/ai-news/scripts/test-fetcher.sh <source_name>
```

输出：元数据 + 活性检查 + 内容采样 + spawn 命令模板。

> 已知坑：bash 3.2 下中文符号紧跟变量名会触发 unbound variable。脚本里已用 `${var}` brace + 中文换 ASCII 修过。

### arXiv 抓取（限流封装）

```bash
python3 /Volumes/Projects/AInews/.claude/skills/ai-news/scripts/arxiv-fetch.py
```

按 `cat:cs.AI/cs.LG + sortBy=submittedDate` 检索，返回 Atom XML。内置 3 秒/次限流（arXiv 礼仪）。**不要在主会话直接 curl arXiv**。

### Dry-run 编排

```
/ai-news --dry-run
```

只跑 Phase 0（references 复验 + 源健康 + 时效检查），不抓不写。

---

## R5：vault 内核心文档

| 文件 | 用途 |
|---|---|
| `SCHEMA.md` | vault 根公约（AI 写盘前必读，5 项自检清单） |
| `MOC.md` | Map of Content 总览导航（人工维护） |
| `README.md` | 项目说明 |
| `_base-by-topic.base` | Bases 视图：按主题分组 |
| `_base-by-source.base` | Bases 视图：按 source 切片 |
| `_base-latest-daily.base` | Bases 视图：Daily 时间线 + 健康度监控 |

---

## R6：6 个原生 subagent 位置

```
.claude/agents/
├── news-fetcher-rss.md
├── news-fetcher-api.md
├── news-fetcher-webfetch.md
├── news-filter.md
├── news-cluster.md
└── news-writer.md
```

被 `/ai-news` skill 在 SKILL.md 各 Phase 调度，可独立修改 system prompt 而不动 skill。

---

## R7：归档备查

```
.claude/memory/_archive/
├── architecture-snapshot-2026-06-27.md       # 旧版 ainews-project-architecture（已规范化拆分）
├── obsidian-cli-facts-snapshot-2026-06-27.md # 旧版 obsidian-vault-cli-facts（已并入 R1+R2）
└── ainews-source-matrix-snapshot-2026-06-27.md # 信息源 v1 实测调研（结论已落地 sources.md / blacklist.md）
```

> 归档文件**仅供历史溯源**（如"为何 a16z RSS 在黑名单 / 为何 Meta 更新慢"），不参与日常加载链。

---

## R8：全局环境清单

本机运行时清单见全局：

```
~/.claude/ENVIRONMENTS.md
```

AInews 用到的：
- **Python**：Miniconda 3.13.12（`arxiv-fetch.py` 跑这个）
- **Bash**：系统自带（macOS 3.2，注意中文坑见 R4）

---

## 相关记忆

- [[project_overview]] — 调试入口对应的组件
- [[decisions]] — 为何把信息源元数据放 references/ 而非 vault
