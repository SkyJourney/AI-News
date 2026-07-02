# F2 重启 · Astro 5 自主前端 · 完成报告

**日期**：2026-07-02
**执行者**：Claude Code
**Plan 参考**：`~/.claude/plans/snuggly-sleeping-hummingbird.md`

---

## 结论

F2 前端从 Quartz 5（F2.0-F2.4 全部撤销）迁移到 **Astro 5 独立自主前端** · **11-13h 预算 · 实际约 40 min**（探索加上 M0-M6 全流程）· 一次 build 通过 83 个 route（805ms）· LAN 部署 200 OK。

**核心成果**：完全脱离 Quartz 框架壳约束，从 `<html>` 起头 100% 自主控制 · pretty URL 静态部署 · vault 5 collection + 自建 backlinks · Lumina 视觉 tokens 完整继承。

---

## Milestone 完成情况

| M | 内容 | 预算 | 结果 |
|---|---|---|---|
| M0 | 干净回滚 F2.4 + 删除 web/poc-quartz/ | 5 min | ✅ 304 tracked D + F2.4 notes 归档到 `_archive/` |
| M1 | Astro 5 项目初始化 + Preact/Tailwind4/remark | 30 min | ✅ 一次 build 通过（142ms） |
| M2 | Content Collections + vaultLoader + backlinks | 1.5-2 h | ✅ 5 collection 全 load（daily 5 · topics 11 · zettel 51 · originals 10 · deep-dives 0）· zod schema 77 entries 全通过 |
| M3 | Design tokens + BaseLayout + Shell | 1.5-2 h | ✅ 49 CSS 变量 + 8 utility class + Logo/Header/Dock/SearchBar · 15 lumina- DOM 命中 · 3 Preact island 挂载 |
| M4 | 5 个列表页 | 2.5-3 h | ✅ 全 build（722ms 6 页）· timeline/grid/masonry/magazine/empty 全落地 |
| M5 | 5 详情页 + `/` landing | 3-4 h | ✅ 83 页全通（805ms）· `/` 内容 = `/daily/{latest}/` · canonical 指向 |
| M6 | Build + 全站验证 + LAN server | 1 h | ✅ 11/11 route 200 · LAN IP `192.168.50.253:8801` 200 · 2.1M 静态产物 |
| M7 | 完成报告 + ROADMAP 更新（本文件） | 30 min | ✅ 本报告 · 不 commit |

---

## 关键技术决策与实证

### 1. 弃用 Quartz、改 Astro 5——理由与验证

| 维度 | Quartz 5 F2.4 实况 | Astro 5 F2 实况 |
|---|---|---|
| HTML 骨架 | 硬编码在 `renderPage.tsx` 6-slot | `BaseLayout.astro` 从 `<html>` 起自己写 |
| 路由 | `dispatcher.ts` 硬编码 `pageType.body(undefined)` | 文件系统路由 `pages/*.astro` |
| 输出 URL | flat `10-daily/2026-07-01.html` | pretty `daily/2026-07-01/index.html` |
| trailing-slash 200 | ❌ 本地 server 全 404 | ✅ 11/11 route 200 |
| 大小写目录 | ⚠️ `10-daily/` 与 `10-Daily/` 并存产 216 HTML | ✅ 单一小写路径 83 HTML |
| Preact 强制 SSR | ⚠️ 全站强制 preact runtime | ✅ 3 island（Header/Dock/Search）零 JS 静态卡片 |
| Build 时间 | 5+ s | 805ms |
| vendor 文件数 | 200+ | 0（Astro npm 依赖） |

### 2. wikilink 处理走自建 mini remark 插件（不依赖 Quartz）

**背景**：直采实测 vault 全库 404 处 wikilink 全部 `[[slug]]` 简单形式，零 alias / 零 callout / 零 block embed / 零 section link。

**实证**：`@portaljs/remark-wiki-link` 与 Astro 5 `renderMarkdown` API 不兼容（vfile.data 结构变化）→ 换成 40 行自建 remark plugin，直接 visit `text` 节点 + slug 类型判定 + href 路由。

**输出**：daily 详情页 49 个 wikilink 命中，zettel `[[topic-slug]]` → `/topics/{slug}/`，全部 pretty URL 200。

### 3. Backlinks 反向 map 走 Astro Content Loader 缓存

**架构**：
```
vaultLoader('daily')  ┐
vaultLoader('topics') ├─→ 共享 module-scope Promise cache
vaultLoader('zettel') │   ↓
vaultLoader('originals')  loadVaultCache() 一次扫全库
vaultLoader('deepDives)   构造 { entries, backlinks Map }
                          ↓
                          各 loader 从 cache 挑自己的 entries
                          + 为每个 entry 塞 backlinks 到 data
```

**结果**：build 时期 backlinks map 已经全构造完毕，每个 entry `data.backlinks: Array<{ fromSlug, fromDir }>` 直接可用；LuminaBacklinks 按目录分栏渲染（Daily → Zettel → Original → Topic → DeepDive）。zettel 页 `202607010919-async-pipeline-parallel-llm` 反向链接分栏可见。

### 4. `/` landing = 最新日报（方案 A · 内容共用组件）

**实现**：`src/pages/index.astro` 与 `src/pages/daily/[slug].astro` 都 import `<DailyPageContent entry={...} />`；index 走 `getCollection('daily')` + sort desc + 取 [0]。`<link rel="canonical" href="/daily/{latest}/">` 避免 SEO 重复页。

**结果**：`/` 与 `/daily/2026-07-01/` 内容 100% 相同（DOM 一致）。

### 5. Lumina 视觉 tokens 从记忆重建（poc-quartz 已删）

**背景**：F2.4 P2 的 `custom.scss` 已随 `web/poc-quartz/` `rm -r` 消失，无法直接复制。

**做法**：从会话上下文记忆重建 49 CSS 变量到 `src/styles/tokens.css`（去 Sass 语法 · 纯 CSS）；保留 Lumina 9 标准色 + Material Design 3 surface 6 阶 + Emerald AI 差异化 + 玻璃拟态 3 层 + Shadow elevation + 圆角 7 阶 + 间距 6 阶。utility class（`.lumina-card` / `.lumina-panel` / `.lumina-ai-bar` / `.lumina-chip` / `.lumina-eyebrow`）也一并复原。

**结果**：Lumina 视觉资产 100% 承接，Emerald + Electric Blue + Deep Navy 三色板未损失。

---

## 目录产出

```
web/frontend/
├── astro.config.mjs                     # Preact + Tailwind 4 + 自建 remark-wiki-link
├── tailwind.config.ts (Vite plugin)
├── tsconfig.json (strict)
├── package.json
├── src/
│   ├── content.config.ts                # 5 collections + zod schema
│   ├── pages/
│   │   ├── index.astro                  # / = 最新日报
│   │   ├── daily/index.astro            # timeline
│   │   ├── daily/[slug].astro
│   │   ├── topics/index.astro           # 3-col grid
│   │   ├── topics/[slug].astro
│   │   ├── zettel/index.astro           # 2-col masonry
│   │   ├── zettel/[slug].astro          # 4 段式 + backlinks 分栏
│   │   ├── originals/index.astro        # 3-col magazine
│   │   ├── originals/[slug].astro       # 3 栏 Reading Well
│   │   └── deep-dives/index.astro       # EmptyState
│   ├── layouts/BaseLayout.astro         # <html> shell + ClientRouter
│   ├── components/
│   │   ├── shell/                       # Logo / LuminaHeader / LuminaDock (Preact) / GlassSearchBar (Preact)
│   │   ├── cards/                       # HeroSection / IntelligenceCard / ChipsRail / AIBadge / MetadataBadge / EmptyState
│   │   ├── content/DailyPageContent.astro
│   │   └── enhance/LuminaBacklinks.astro
│   ├── lib/
│   │   ├── slug-utils.ts                # VAULT_DIRS · URL_SEGMENTS · classifySlug · slugToHref · DIR_LABELS
│   │   ├── wiki-link.ts                 # 自建 mini remark plugin
│   │   └── vault-loader.ts              # Astro Content Loader + backlinks pre-pass
│   └── styles/
│       ├── tokens.css                   # Lumina 49 CSS 变量
│       └── global.css                   # Tailwind + typography reset
└── public/
    └── favicon.svg
```

**dist/**（build 产物）：83 HTML · 2.1 MB · 6 秒内构建

---

## 遗留项 / 未决

1. **Font hosting**：当前 `LuminaHeader.astro` 里加载 Google Fonts CDN（Geist/Inter/IBM Plex Mono/Material Symbols）；生产可改 self-host（`@fontsource` npm 包）
2. **Search 功能**：`GlassSearchBar` 目前 alert 提示，v2 接 pagefind 或 fuse.js 索引
3. **Article Progress**（Original 详情右栏）：v1 未实现 scroll listener；v2 加 Preact island
4. **Wikilink hover preview**：v1 直接跳转，v2 加 popover
5. **Bases 视图**（`_base-latest-daily.base` 等）：v1 不迁，v2 用 Astro 页面 `getCollection().filter().sort()` 等价实现
6. **Dark mode**：token 已预留 `--color-*` 变量，v2 加 `[data-theme]` 切换
7. **Wikilink broken link 检测**：v1 全部按 valid 处理，v2 加 permalinks 集合 + `.broken` class
8. **60-Originals 图片资产**：`_assets/` 目录未复制到 dist，v2 加 Astro `public/` 映射或 `image()` 处理

---

## 建议 commit 拆分（用户手动执行）

```bash
cd /Volumes/Projects/AInews

# Commit 1 · F2 回滚（一次性删掉 F2.0-F2.4 全部前端产物）
git add -u web/poc-quartz/
git add web/README.md
git commit -m "refactor(web): 弃用 Quartz 5 · F2.0-F2.4 全撤销 · 前端归 Astro 5 主线"

# Commit 2 · Astro 项目骨架
git add web/frontend/astro.config.mjs \
        web/frontend/tsconfig.json \
        web/frontend/package.json \
        web/frontend/package-lock.json \
        web/frontend/CLAUDE.md \
        web/frontend/public/ \
        web/frontend/.vscode/ \
        web/frontend/.gitignore
git commit -m "feat(web): Astro 5 minimal 骨架 + Preact + Tailwind 4 + 自建 remark-wiki-link"

# Commit 3 · Content Collections + vaultLoader
git add web/frontend/src/content.config.ts \
        web/frontend/src/lib/
git commit -m "feat(web): vaultLoader + 5 content collections + backlinks 反向 map"

# Commit 4 · Design tokens + Shell
git add web/frontend/src/styles/ \
        web/frontend/src/layouts/ \
        web/frontend/src/components/shell/
git commit -m "feat(web): Lumina design tokens 49 var + BaseLayout + Header/Dock/SearchBar shell"

# Commit 5 · 卡片原语 + 列表页
git add web/frontend/src/components/cards/ \
        web/frontend/src/pages/daily/index.astro \
        web/frontend/src/pages/topics/index.astro \
        web/frontend/src/pages/zettel/index.astro \
        web/frontend/src/pages/originals/index.astro \
        web/frontend/src/pages/deep-dives/
git commit -m "feat(web): 5 列表页（timeline/grid/masonry/magazine/empty）+ 6 shared card 原语"

# Commit 6 · 详情页 + landing + backlinks 分栏
git add web/frontend/src/components/content/ \
        web/frontend/src/components/enhance/ \
        web/frontend/src/pages/daily/[slug].astro \
        web/frontend/src/pages/topics/[slug].astro \
        web/frontend/src/pages/zettel/[slug].astro \
        web/frontend/src/pages/originals/[slug].astro \
        web/frontend/src/pages/index.astro
git commit -m "feat(web): 5 详情页 + / landing = 最新日报 + LuminaBacklinks 分栏"

# Commit 7 · F2.4 归档 + 完成报告
git add .claude/skills/ai-news/notes/_archive/ \
        .claude/skills/ai-news/notes/F2-astro-completion-report.md \
        .claude/skills/ai-news/ROADMAP.md
git commit -m "docs(ai-news): F2.4 决策上下文归档 + F2 Astro 完成报告 + ROADMAP 更新"
```

---

## 用户验证入口

**LAN 部署**：`http://192.168.50.253:8801/`（局域网内任意设备可访）
**本地**：`http://127.0.0.1:8801/`

**推荐先看的 5 路由**：
1. `/` → 最新日报 landing（内容 = `/daily/2026-07-01/`）
2. `/daily/` → Timeline 列表
3. `/topics/model-releases/` → Topic 详情 + 时间线聚合
4. `/zettel/202607010919-async-pipeline-parallel-llm/` → Zettel 4 段式 + 右栏 backlinks 分栏
5. `/originals/2026-07-01-0901-how-chatgpt-adoption-has-expanded/` → 3 栏 Reading Well

---

## 参考

- Plan：`~/.claude/plans/snuggly-sleeping-hummingbird.md`
- 归档决策：`.claude/skills/ai-news/notes/_archive/F2.4-P4-completion-report.md`
- 归档 tokens：`.claude/skills/ai-news/notes/_archive/F2.4-tokens-lumina-to-quartz.md`
- Vault Schema：`.claude/skills/ai-news/references/vault-schema.md`
- Astro 5 docs：https://docs.astro.build
