---
name: 记忆健康检查报告
description: memory-lint 最新一次执行的检查结果与待处理项
type: lint
last_updated: 2026-06-27
---

# 记忆健康检查报告

> _执行时间: 2026-06-27 | Base commit: `d729cc9` | Last synced: 2026-06-27_
>
> **如何使用**：NEED-HUMAN 条目末尾有 `<!-- id: xxxxxxxx -->` 标记。处理完或决定不处理时，在同段追加 `<!-- resolved: DATE, 简要原因 -->`，下次 lint 该条目自动跳过。

## 健康概览

| 检查项 | AUTO-FIX | NEED-HUMAN |
|--------|---------|-----------|
| 1 孤儿 / 2 幽灵 / 3A 引用 / 3B 双链 | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 |
| 4 矛盾 / 5 过期 / 6 污染 | — | 0 / 0 / 0 |

**AUTO-FIX 已执行 1 项 | NEED-HUMAN 新列出 0 项 | 历史已 resolved 跳过 0 项**

---

## AUTO-FIX 已执行清单

- [x] MEMORY.md「引用」列已重算（双向闭环计数）：overview=4 / progress=3 / decisions=4 / feedback=2 / reference=2

---

## 条目级高频引用 Top（供 /memory-update 消费）

| 条目 | 跨文件次数 | 建议 |
|------|----------|------|
| project_overview | 4 | 已是必读文件，无需升级 |
| decisions | 4 | 已是必读文件，无需升级 |
| project_progress | 3 | 已是必读文件 |
| feedback | 2 | 已是必读文件 |
| reference | 2 | 仍按需加载（reference 类不必每次会话加载） |

---

## NEED-HUMAN 待处理清单

✅ 无待处理项。

---

## 检查通过明细

| Phase | 通过情况 |
|---|---|
| 1 孤儿（索引→磁盘） | ✅ 6 索引条目全部磁盘存在（含 lint_report） |
| 2 幽灵（磁盘→索引） | ✅ 5 个核心 .md 全部已索引；MEMORY.md 为索引文件本体不计；`_archive/` 已在 MEMORY.md 归档段登记 |
| 3A 引用存在性 | ✅ 12 条跨文件 `[[xxx]]` 引用目标全部存在（lint_report 内 `[[file]]` `[[xxx]]` 为模板占位符，不计） |
| 3B 双链对称性 | ✅ overview ↔ progress / decisions / feedback / reference 互引闭环 |
| 4 内容矛盾 | ✅ 无合并冲突标记；5 文件无逻辑/数值矛盾；版本号一致（commit=d729cc9） |
| 5 过期检测 | ✅ 全部 last_updated=2026-06-27（today），距 WARN 阈值 30 天还有 30 天 |
| 6 可推断污染 | ✅ overview "目录结构"段属架构层级（说明组织结构），非具体类名/方法/路径列表，按 skill 边界规则保留 |

## 备注

- 旧版 `ainews-project-architecture.md` 与 `obsidian-vault-cli-facts.md` 已迁入 `_archive/` 加 `-snapshot-2026-06-27` 后缀
- 本次记忆体系完全重建，遵循 memory-sync skill 标准（overview/progress/decisions/feedback/reference 五件套）
- decisions 11 条、feedback 9 条均带 What+Why+How 三段结构，未来 lint 可基于 ## 级 anchor 做条目级引用统计
