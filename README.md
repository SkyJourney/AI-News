# AInews

`/Volumes/Projects/AInews` = 「AI 资讯」的 Obsidian vault + 本地 git，全套采集管道在 `.claude/`。

- **vault** = 纯落盘知识库（存储 / 组织 / 检索）
- **采集** = `/ai-news` skill + 6 个原生 subagent（fetcher-{rss,api,webfetch} + filter + cluster + writer）

两层解耦。

---

## 目录

| 目录 | 用途 |
|---|---|
| `00-Inbox/` | 原始抓取、未消化（v1 未启用） |
| `10-Daily/` | 每日简报 |
| `20-Topics/` | 主题汇聚（append 模式） |
| `40-Deep-Dives/` | 人工专题深度研究 |
| `50-Zettel/` | 原子概念卡（Zettelkasten 时间戳 ID） |
| `90-Archive/` | 归档 |
| `99-Log/` | 运行日志 |

完整约定见 [SCHEMA.md](./SCHEMA.md)。

---

## 采集

```
/ai-news                  # 抓今天 14 个源 → 写 Daily + Zettel + Topic + Log
/ai-news --date=YYYY-MM-DD
/ai-news --dry-run        # 只跑 Phase 0 健康检查
```

skill 在 `.claude/skills/ai-news/SKILL.md`，5 phase 编排：Preflight → Fetch（12 并发 + retry）→ Filter → Cluster → Write → Log。

**调试单个 fetcher**：
```
bash .claude/skills/ai-news/scripts/test-fetcher.sh openai-rss
```

## 信息源管理

14 个源完整登记（tier / perspective / fetch_method / url / reliability / last_verified）：

→ [`.claude/skills/ai-news/references/sources.md`](.claude/skills/ai-news/references/sources.md)

死源黑名单（防"想当然"加回）：

→ [`.claude/skills/ai-news/references/blacklist.md`](.claude/skills/ai-news/references/blacklist.md)

新增 / 降级 / 拉黑某源：改对应 YAML，不需要动 vault。

## 调度（V2，未实施）

| 机制 | 适用性 | 决策 |
|---|---|---|
| Claude Code Desktop scheduled tasks | 本地、能访问本地 vault、应用须打开 | ✅ V2 首选 |
| `/loop` + CronCreate | 会话内、7 天过期 | 仅调试期 |
| Cloud Routines | 云端 fresh clone，无本地文件访问 | ❌ PASS |

V2 启用步骤见 `.claude/skills/ai-news/SKILL.md` 末尾。

---

## 项目上下文

- 当前架构 + 14 源摘要 → [.claude/memory/ainews-project-architecture.md](.claude/memory/ainews-project-architecture.md)
- Obsidian CLI 边界 → [.claude/memory/obsidian-vault-cli-facts.md](.claude/memory/obsidian-vault-cli-facts.md)
- 原始信息源调研快照（归档备查）→ `.claude/memory/_archive/`

## 状态

- 8 commit，2 次完整跑通验证（详见 99-Log）
- 14 alive 源 + 6 subagent + retry + Phase 1 防幻觉
- 待加：Bases 视图、MOC、单测脚本、低置信标记、tags 规范

最后更新：2026-06-27
