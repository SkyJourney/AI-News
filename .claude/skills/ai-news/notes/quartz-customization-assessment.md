# Quartz 5 自定义能力评估

日期：2026-07-01
调研触发：F2.0 决策后（[[decisions#D15]]），F2.1-F2.7 落地前需要摸清"Quartz 能被改造到什么程度"，避免中途撞墙。

## TL;DR

**Quartz 5 有清晰的 5 层定制入口 + 3 类 upgrade-safe 定制策略**。绝大部分品牌化/布局改造靠"配置 + custom.scss + TS override"即可完成，**无需碰 upstream 源码**。真正需要写代码的场景：新组件、新 page-type、新 Bases view、新 frame——每种都是"写一个独立 preact 组件文件 + 注册"的量级（≤ 半天）。

**结论**：Quartz 5 的定制能力足以支撑 F2.1-F2.7 全部需求，包括"完全自定义 web UI"（dashboard 首页 / 2 栏改 3 栏 / 卡片流详情页）。

## 定制层级 5 层（从易到难）

| 层 | 位置 | 修改内容 | 是否 upgrade-safe | 典型场景 | 成本 |
|---|---|---|---|---|---|
| **① 配置层** | `quartz.config.yaml` | pageTitle / 字体 / 色板 / 插件启用 / 每插件的 `layout.position` + `layout.priority` | ✅ upgrade-safe | 品牌名、色调、开关插件、调左右栏顺序 | 5 min |
| **② 样式层** | `quartz/styles/custom.scss` | 任意 CSS 覆盖（用 `.className` 或 `[data-frame="..."]` 选择器）| ⚠️ 半安全（修改 `variables.scss` 会被 upgrade 覆盖，但 `custom.scss` 是官方约定的用户 override 位置）| 微调排版 / 加自定义 UI 元素（如顶栏 banner）/ Bases 表格斑马纹 | 15-60 min |
| **③ 组件重排** | `quartz.ts` TS override `loadQuartzLayout({...})` | 用代码替换 `byPageType.<type>` 的组件槽位（left/right/beforeBody/pageBody/footer）；可以插入自定义组件、条件渲染、包装现有组件 | ✅ upgrade-safe（自己的 quartz.ts 归自己）| dashboard 首页 pageBody / 3 栏改 2 栏（`right: []`）/ 某类页替换组件顺序 | 1-3 h |
| **④ 自定义组件/插件** | 独立 git repo，写 `QuartzComponent` + `package.json` 声明 category | 一个"社区插件"repo（本地写也可，通过 `npx quartz plugin add <path>` 装）；4 类：Transformer / Filter / Emitter / PageType；额外可注册 Bases View 或 Page Frame | ✅ upgrade-safe（独立仓库，不进 quartz upstream） | 加 AInews 首页 dashboard / 加"每日速览"卡片 / 加自定义 Bases 视图（如 kanban / timeline / heatmap） | 半天-2 天 |
| **⑤ 修改 upstream** | `quartz/` 目录内 | 直接改 quartz core 代码（`components/frames/`、`plugins/loader/`、`build.ts`）| ❌ 会被 `npx quartz upgrade` 冲突 | 极少需要——只有当所有其他层都无解时才走 | 因场景而异，且承担合并冲突成本 |

## POC 期实测（本会话）

**已跑通的实验**（全部 upgrade-safe 层）：

1. **配置层**：`quartz.config.yaml` 里
   - `pageTitle: AInews` + `pageTitleSuffix: " · AI 资讯"` → 生效（HTML `<title>` 里出现"· AI 资讯"）
   - 主题色板全换（`secondary: "#c8511a"` 橙调等 9 个变量）→ 生效（`public/index-*.css` 里可 grep 到新色值）

2. **样式层**：`quartz/styles/custom.scss` 加
   - 顶部 `body::before` 品牌横条 → 生效（可 grep 到 `AInews · POC · F2.0 已完成 · F2.1 待启` 出现在最终 CSS）
   - `.internal:hover` 波浪下划线 + `.bases-table` 斑马纹 → 生效

3. **rebuild 时长**：8.5s（比首次 12s 快，plugin 已缓存）

## AInews F2.4 品牌化具体动作清单

### 必做（① 配置层 + ② 样式层，upgrade-safe）

- [ ] `quartz.config.yaml`
  - [ ] `pageTitle: AInews`
  - [ ] `pageTitleSuffix: " · AI 资讯"`（HTML title 的后缀）
  - [ ] 主题色改品牌色板（当前 POC 用了暖橙 `#c8511a`，最终待定）
  - [ ] `configuration.locale: "zh-CN"`（当前 en-US；影响 i18n 组件如 backlinks/relatedPages 的文案）
  - [ ] **关 latex 插件**：`- source: github:quartz-community/latex` 那条改 `enabled: false`——vault 里的 `$500M` / `$100 亿` 会被误认数学模式
- [ ] `quartz/styles/custom.scss`
  - [ ] AInews 品牌 typography（如果不用 Google Fonts 而用本地字体，改 `configuration.theme.fontOrigin: local` + 挂载字体文件）
  - [ ] Bases 表格斑马纹 + hover 高亮
  - [ ] 修 `.callout` 的中文视觉（Obsidian callout 在 Quartz 里默认西文风格）
- [ ] `content/index.md`（Welcome 首页）：写 AInews 项目说明 + MOC 入口 + 今日速览

### 可选（③ 组件重排，需 quartz.ts 改 TS）

- [ ] Daily 页在 pageBody 上方加"上一日 / 下一日"跳转组件（自定义组件 + TS override）
- [ ] 60-Originals 页去掉 backlinks 栏（原文归档不需要反链），改成"关联 Zettel / 关联 Daily"横向卡片
- [ ] Topic 页 pageBody 加"主题时间线"视图（用现有的 timeline 类 Bases view 或自定义）

## "完全自定义 web UI" 可行性（如你想要 dashboard 风格首页 / 2 栏改 3 栏 / 卡片流详情页）

| 需求 | 方案 | 层级 | 工作量 | 说明 |
|---|---|---|---|---|
| **3 栏改 2 栏**（去右栏） | `layout.byPageType.<type>.positions.right: []`（YAML）| ① | 5 min | 已有官方示例（`folder`/`tag` 页就是这么做的）|
| **完全无侧栏**（全宽） | `layout.byPageType.<type>.template: full-width` | ① | 5 min | Quartz 内置 3 种 frame：default / full-width / minimal |
| **AInews Dashboard 首页**（今日速览 + 主题热力图 + 最近 Original 卡片流）| 写自定义 `HomePage` component + 在 `content/index.md` 前加特殊 frontmatter 触发 or TS override | ③ or ④ | 半天 | ①：写一个 preact 组件（读 `allFiles` 计算数据）+ TS override 覆盖 `byPageType.content.pageBody` 仅在 slug=index 时；②：写为独立 community plugin |
| **60-Originals 详情页卡片流**（左侧原文全文、右侧作者/日期/相关卡片、底部相关 Zettel）| 自定义 page-type plugin OR 自定义 frame + `layout.byPageType.originals.template: xxx` | ④/⑤ | 1-2 天 | Bases plugin 是先例（`bases-page` 是自己的 page type + frame）|
| **首页替换成 Bases dashboard**（把 4 个 base 视图并排嵌到首页） | 用 iframe or transclusion 嵌入 4 个 `.base.html`；或写一个 `MultiBase` 组件读多个 base | ③ | 3-4 h | Quartz 已渲染 `.base.html` 为 iframe-able 页面 |
| **自定义 Bases 视图**（比如 heatmap / kanban / calendar 视图）| 通过 `ViewRegistry` 注册新视图 | ④ | 4-8 h | Quartz 5 新特性："Bases Views" 是独立插件类别 |
| **完全接管首页布局**（把 header + sidebar 全去掉，只留自定义 dashboard）| 写自定义 frame + `layout.byPageType.content.template: dashboard`；仅对 index 生效需 TS override 条件判断 | ④+⑤ 交界 | 半天 | 参考 `MinimalFrame.tsx`（用于 404 页）的实现 |
| **主题级换肤**（Karpathy 风、Obsidian 官方风、blog 风）| Community plugin：`github:saberzero1/quartz-themes` 已在 obsidian 模板里挂着，切换 `options.theme: default → xxx` | ① | 1 min | 现成插件，几十种主题可选 |

**结论**：即使做"AInews Dashboard 首页 + 卡片流详情页 + 自定义 Bases 视图"这种全套定制，总工作量 ≤ 3 天，且核心工作是写 preact 组件（不是"和 Quartz 内部斗争"）。

## 关键架构点（写代码前要理解的 5 件事）

1. **Quartz 5 = 静态站生成器**：所有页面在 build 时生成 HTML，运行时纯静态。任何"动态"效果（搜索、深色模式、SPA 导航）都是纯前端 JS。**没有服务器端逻辑**——若 AInews 想加"评论"、"用户"、"计数"等，需要第三方服务（如 giscus/plausible），Quartz 不会给你后端。
2. **组件是 preact SSR**：`QuartzComponent` 是 preact 函数组件，构建时用 `preact-render-to-string` 渲染成 HTML 字符串写到 `.html` 文件。`useState`/`useEffect` 在这里无用；交互靠 `.beforeDOMLoaded` / `.afterDOMLoaded` 挂普通 JS。
3. **layout 系统是 slot-based**：8 个槽位（`head`/`header`/`beforeBody`/`pageBody`/`afterBody`/`left`/`right`/`footer`），每个槽位放一到多个 `QuartzComponent`；plugin 通过 `layout.position` + `layout.priority` 声明自己想去的槽位；用户可以在 `quartz.config.yaml` 覆盖插件的 layout 或在 `quartz.ts` TS override 里完全重排。
4. **frame 系统控制槽位布局**：3 个内置 frame（default 3 栏 / full-width 无侧栏 / minimal 只有 content+footer）；新 frame 通过 plugin 声明或直接放 `quartz/components/frames/` 后注册。frame 名会写到 `.page[data-frame="..."]` 上供 CSS 选择器差异化样式。
5. **plugin 是独立 git repo**：写自己的 plugin 意味着写一个独立 git 仓库（或本地路径），有 `src/index.ts` + `tsup.config.ts` + `package.json`。装到 Quartz：`npx quartz plugin add github:you/plugin` 或者 `npx quartz plugin add <local-path>`。用 `quartz.lock.json` 锁 commit hash。

## Upgrade 兼容性策略

Quartz 5 有 `npx quartz upgrade` 命令拉 upstream 更新。定制要保持 upgrade-safe：

**✅ Upgrade-safe 修改**（放心改）：
- `quartz.config.yaml` — 用户配置
- `quartz/styles/custom.scss` — 官方约定的用户 style override 位置
- `quartz.ts` — 用户级 TS override（`loadQuartzLayout({...})` 参数）
- `content/` — 你的笔记
- 自己的 plugin 仓库（独立 git repo）

**⚠️ 会合并冲突的修改**（改前想清楚）：
- `quartz/styles/base.scss` / `variables.scss` — 基础样式，upgrade 会覆盖
- `quartz/components/frames/*` — 自定义 frame 建议走 plugin route 而不是塞进 core
- `quartz/plugins/*` — Quartz core 插件目录
- `quartz/build.ts` / `bootstrap-cli.mjs` / `worker.ts` — 构建管道

**❌ 别改**（除非你打算永久 fork）：
- 任何 `.quartz/` 里的东西（是 plugin 缓存目录，`plugin install` 会重建）

## POC 期发现的注意点

1. **quartz-themes 插件是"预安装"的第三方主题库**（829M，已 gitignore）——切换 `theme: default → foo` 即可，无需自己写 CSS 变量
2. **中文与 LaTeX `$` 冲突**：F2.4 品牌化必做项之一是关 latex 插件或改 `renderEngine` 配置
3. **Bases 视图有 5 个 tab**：POC 已确认 `_base-originals.base` 会渲染出 5 个视图 tab（按 source / language / 时间线 / fallback / 卡片）——这些视图定义在 vault 的 `.base` 文件里，Quartz 5 的 bases-page 插件直接消费。**如果要加新视图形态**（如 heatmap / calendar），有两条路：改 vault `.base` 文件加视图声明（依赖 Obsidian Bases 支持），或写 Quartz plugin 注册新 Bases View 类型（ViewRegistry）
4. **build 时长可预期**：POC 实测 12s（首次） / 8s（增量 rebuild）；vault 涨到 500 md 估计 30-50s；有 workerpool（>128 md 才启用），并发处理

## F2.4 落地路径推荐

**Phase 1（0.5 天）** — 配置层 + custom.scss 基础品牌化：
- pageTitle / locale / 色板 / 关 latex / typography
- custom.scss 加中文排版微调 + Bases 表格美化
- 用 `theme: default` 或试装 `saberzero1/quartz-themes` 里的 blog 主题

**Phase 2（1 天）** — 组件重排 + Welcome 首页：
- 写 AInews Home component（今日速览 + 最近 Original 卡片流 + 主题标签云）
- 通过 TS override `byPageType.content.pageBody` 仅在 `slug=index` 时替换
- 或直接改 `content/index.md`（如果 dashboard 用 markdown 表达就够）

**Phase 3（可选，0.5-1 天）** — 独立 plugin：
- 如果 Phase 2 的 Home 组件后期想复用/分享/让别人也用，抽成独立 `ainews-dashboard` plugin

**跳过 Phase 4/5（暂时）**：自定义 frame / 修改 upstream 都不做，保持 upgrade-safe。

## POC 遗留 & 后续动作

- **本报告涉及的 POC 实验**（quartz.config.yaml pageTitle 改动、custom.scss 品牌化条、quartz.config.yaml 色板改动）**是实验代码**——commit 前**要么正式化**（作为 F2.4 的一部分）**要么回滚**。当前状态：未 commit，可选择继续保留作为 F2.4 起点。
- Quartz dev server 仍在 http://localhost:8801/ 运行（POC 期保留），本会话结束时可关。

## 相关

- Quartz 官方架构：`web/poc-quartz/docs/advanced/architecture.md`
- 组件创作指南：`web/poc-quartz/docs/advanced/creating components.md`
- Layout 系统：`web/poc-quartz/docs/layout.md`
- 46 个内置插件详细文档：`web/poc-quartz/docs/plugins/*.md`
- F2.0 决策报告：[[F2.0-poc-report]]
