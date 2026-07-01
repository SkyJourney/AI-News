# web/ · Vault 前端站点

> Sprint 3 · F2 的前端展示层。当前处于 **F2.0 框架 POC 阶段**（3 选 1）。

## 当前状态：F2.0 POC 进行中

三个候选框架并存在 `poc-<framework>/` 子目录，各自独立跑一个最小 POC，用同一份评估维度打分，胜出者会被提升到 `web/` 根，其余目录删除。

### 三个候选

| 目录 | 框架 | 亮点 | 待验证 |
|---|---|---|---|
| `poc-quartz/` | Quartz 4（TS/Node） | 专为 Obsidian vault，wikilink/backlinks/graph 全内置 | 主题定制灵活度 |
| `poc-astro/` | Astro（TS/Node） | 通用性强、生态最大 | wikilink 需 remark 插件自配 |
| `poc-hugo/` | Hugo（Go 单二进制） | 极致构建速度、部署简单 | wikilink 需 render-hook 或主题支持 |

### 评估维度

| 维度 | 权重 |
|---|---|
| Wikilink 解析质量 | ⭐⭐⭐ |
| Backlinks 反查 | ⭐⭐⭐ |
| Frontmatter 驱动路由 | ⭐⭐ |
| 私有内容过滤 | ⭐⭐ |
| 部署产物 / Docker 挂载难度 | ⭐⭐ |
| 主题/排版空间 | ⭐⭐ |
| 定制难度（Pagefind/RSS/OG/阅读时长） | ⭐ |
| 学习成本 / 社区活跃度 | ⭐ |

### POC 输入范围

不做 sandbox 拷贝，三个候选各自 config 仓库根为 content 源，用框架自带 include/exclude 过滤——"配 content filter 的难度"本身是评估维度之一。

- **主输入**：`10-Daily/2026-07-01.md`
- **跨日反链测**：加入 `10-Daily/2026-06-30.md`（7-01 Daily 里有 `[[2026-06-30]]`，看 6-30 页面能否显示"被 7-01 引用"）
- **关联页**：7-01 Daily 展开的所有 wikilink 目标（Zettel / Topic / Original）
- **根级 md**：`MOC.md`、`SCHEMA.md`（测非目录内 md）
- **必须排除**：`.claude/`、`_archive/`、`99-Log/`、`00-Inbox/`、`_base-*.base`、frontmatter `visibility: private`

### 时间盒

- 每候选 ~1.5 小时（含 setup + build + 验证 + 打分）
- 汇总打分 + 决策报告 ~60 min
- **总 ~5 小时**（略压缩于 ROADMAP 原估 1.5 天）

### 产出

- 决策报告：`.claude/skills/ai-news/notes/F2.0-poc-report.md`
- 胜出者提升到 `web/`
- ROADMAP.md 顶部「已完成」追加 F2.0
- memory decisions.md 新增 D15

## F2.0 后目录规划（决策后）

```
web/
├── src/            # 内容适配/模板/组件（依框架而定）
├── public/         # 静态资源
├── nginx.conf      # F2.1 Docker Compose 用
├── Dockerfile      # F2.1 builder
└── package.json    # 依框架而定（Hugo 则无）
```

## 相关

- ROADMAP：`.claude/skills/ai-news/ROADMAP.md` Sprint 3
- 决策：`.claude/memory/decisions.md#D14`
- 落盘公约：`SCHEMA.md`
