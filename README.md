# AInews

把 `/Volumes/Projects/AInews` 做成「AI 资讯」的 Obsidian vault + 本地 git 管理。

- **vault** = 纯落盘知识库（存储 / 组织 / 检索）
- **采集管道** = Claude Code 的 `/ai-news` skill + `.claude/agents/` 内 6 个 subagent

两层解耦。

---

## 目录

| 目录 | 用途 |
|---|---|
| `00-Inbox/` | 原始抓取、未消化 |
| `10-Daily/` | 每日简报（汇总层） |
| `20-Topics/` | 主题汇聚笔记 |
| `40-Deep-Dives/` | 专题深度研究 |
| `50-Zettel/` | 原子概念卡（Zettelkasten） |
| `90-Archive/` | 归档 |
| `99-Log/` | 运行日志 |

完整约定见 [SCHEMA.md](./SCHEMA.md)。

---

## 采集（手动）

在本目录开 Claude Code 会话，输入：

```
/ai-news                  # 默认抓今天
/ai-news --date=YYYY-MM-DD
/ai-news --dry-run        # 只跑 Phase 0 健康检查不落盘
```

skill 在 `.claude/skills/ai-news/`，编排逻辑见 [SKILL.md](.claude/skills/ai-news/SKILL.md)（阶段二实施）。

## 信息源管理

12 个源的完整登记（tier / perspective / fetch_method / url / reliability / last_verified）：

→ [`.claude/skills/ai-news/references/sources.md`](.claude/skills/ai-news/references/sources.md)

死源黑名单（防止"想当然"加回）：

→ [`.claude/skills/ai-news/references/blacklist.md`](.claude/skills/ai-news/references/blacklist.md)

新增 / 降级 / 拉黑某源：直接改对应 YAML，不需要动 vault。

## 调度（V2 候选，未实施）

| 机制 | 适用性 | 决策 |
|---|---|---|
| Claude Code Desktop scheduled tasks | 本地、能访问本地 vault、应用须打开 | ✅ V2 首选 |
| `/loop` + CronCreate | 会话内、7 天过期 | 仅调试期 |
| Cloud Routines | 云端 fresh clone，无本地文件访问 | ❌ PASS |

V2 启用方式将在 SKILL.md 末尾给出（阶段二）。

---

## 项目上下文

- 架构决策、信息源矩阵、Obsidian CLI 事实 → `.claude/memory/*.md`
- 项目记忆引导 → [CLAUDE.md](./CLAUDE.md)
- 实施 Plan（v2）→ `~/.claude/plans/misty-splashing-hopcroft.md`

最后更新：2026-06-27
