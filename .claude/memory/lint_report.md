---
name: 记忆健康检查报告
description: memory-lint 最新一次执行的检查结果与待处理项
type: lint
last_updated: 2026-06-27
---

# 记忆健康检查报告

> _执行时间: 2026-06-27 | Base commit: `8756e50` | Last synced: 2026-06-27_
>
> **如何使用**：NEED-HUMAN 条目末尾有 `<!-- id: xxxxxxxx -->` 标记。处理完或决定不处理时，在同段追加 `<!-- resolved: DATE, 简要原因 -->`，下次 lint 该条目自动跳过。

## 健康概览

| 检查项 | AUTO-FIX | NEED-HUMAN |
|--------|---------|-----------|
| 1 孤儿 / 2 幽灵 / 3A 引用 / 3B 双链 | 0 / 0 / 0 / 0 | — / — / 0 / 0 |
| 4 矛盾 / 5 过期 / 6 污染 | — | 0 / 0 / 0 |

**AUTO-FIX 已执行 1 项 | NEED-HUMAN 新列出 0 项 | 历史已 resolved 跳过 0 项**

---

## AUTO-FIX 已执行清单

- [x] MEMORY.md「引用」列已刷新（2 文件：architecture=1, vault-cli-facts=1；双向闭环计数）

---

## 条目级高频引用 Top（供 /memory-update 消费）

| 条目 | 跨文件次数 | 建议 |
|------|----------|------|
| — | — | 无候选（当前 2 个记忆文件均为整篇式叙述，无 ## 级 decisions/feedback 条目，无跨文件 `[[file.md#section]]` 引用） |

---

## NEED-HUMAN 待处理清单

✅ 无待处理项。

---

## 检查通过明细

| Phase | 通过情况 |
|---|---|
| 1 孤儿（索引→磁盘） | ✅ 2 索引条目全部磁盘存在 |
| 2 幽灵（磁盘→索引） | ✅ 3 个磁盘 .md 全部已索引（含 MEMORY.md / lint_report.md 排除项）；`_archive/` 归档目录已在 MEMORY.md "归档" 段明确登记，非幽灵 |
| 3A 引用存在性 | ✅ 2 条跨文件 `[[xxx]]` 引用目标全部存在 |
| 3B 双链对称性 | ✅ architecture ↔ vault-cli-facts 互引闭环 |
| 4 内容矛盾 | ✅ 无合并冲突标记；2 文件无逻辑/数值矛盾；项目无 pom/package/requirements 类依赖文件 |
| 5 过期检测 | ✅ 全部 last_updated=2026-06-27（today），距 WARN 阈值 30 天还有 30 天 |
| 6 可推断污染 | ✅ architecture 的"文件分布"段属架构层级（说明组织结构），非具体类名/方法/路径列表，按 skill 边界规则保留 |

## 备注

- `synonyms.md` 不存在 → 无矛盾检测候选，无需创建
- 当前 vault 体量小（2 记忆文件 + 1 归档），结构简单；待新增 decisions/feedback 类条目后，Phase 3C/8 引用计数才会有 synthesis 升级候选
