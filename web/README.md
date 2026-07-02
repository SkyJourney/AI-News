# web/ · Vault 前端站点

> Sprint 3 · F2 的前端展示层。当前采用 **Astro 5**（F2 重启阶段）。

## 当前架构：`web/frontend/` · Astro 5

- **Astro 5** + `@astrojs/preact`（islands）+ `@tailwindcss/vite`（Tailwind 4）
- **内容解析**：Astro 内置 `@astrojs/markdown-remark` + `remark-wiki-link`（vault wikilink 全库简单形式，无需 vendor Quartz）
- **数据契约**：Content Collections（zod schema）+ 自定义 `vaultLoader`（读 vault 5 目录 + 构造 backlinks 反向 map）
- **构建产物**：`dist/` 纯静态 HTML，`build.format: 'directory'`（pretty URL）
- **IA**：`/` = 最新一天日报；5 tab 导航 → 5 个列表页 → 详情页；顶栏 Logo 点击回 `/`

## 目录

```
web/
├── frontend/          # Astro 5 项目根（v1）
│   ├── src/
│   │   ├── pages/     # 路由（index / daily / topics / zettel / originals / deep-dives / 404）
│   │   ├── layouts/   # BaseLayout / ArticleLayout
│   │   ├── components/  # shell / cards / content / enhance / lists
│   │   ├── content.config.ts  # 5 collections + custom loader
│   │   ├── lib/       # vaultLoader / wiki-link / slug-utils / ast-extract
│   │   └── styles/    # tokens.css（Lumina 49 CSS 变量）+ global.css
│   ├── astro.config.mjs
│   └── package.json
└── README.md
```

## 历史阶段（已归档）

| 阶段 | 决策 | 状态 |
|---|---|---|
| F2.0（2026-07-01） | 框架 POC 3 选 1（Quartz/Astro/Hugo）→ 选 Quartz 5 | 结论已推翻 |
| F2.4 P1-P4（2026-07-01/02） | Lumina 视觉层 + 内容层 override Quartz | 弃用，回滚 |
| F2 重启（2026-07-02） | 弃用 Quartz、改 Astro 5 自主前端 | **当前** |

回滚原因：Quartz 5 架构强约束（dispatcher 硬编码 `pageType.body(undefined)`、renderPage 6-slot layout、扁平 HTML 输出）导致本地服务器 trailing-slash 404、大小写目录重复、视觉严重偏离设计稿；Lumina override 需绕 3 层 hack。详见归档决策：
- `.claude/skills/ai-news/notes/_archive/F2.4-P4-completion-report.md`
- `.claude/skills/ai-news/notes/_archive/F2.4-tokens-lumina-to-quartz.md`

## 相关

- ROADMAP：`.claude/skills/ai-news/ROADMAP.md` Sprint 3
- 决策：`.claude/memory/decisions.md`
- 落盘公约：`SCHEMA.md`
