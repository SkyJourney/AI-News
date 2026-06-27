---
name: obsidian-vault-cli-facts
description: AInews vault 注册现状 + Obsidian 官方 CLI 的能力边界（无法注册新 vault，须 GUI 首开）
metadata:
  type: reference
---

**Obsidian 官方 CLI（1.12.7+，`/usr/local/bin/obsidian` → `/Applications/Obsidian.app/Contents/MacOS/obsidian-cli`）的能力边界**：
- CLI 是**运行中桌面应用的"遥控器"**，不是独立 headless 工具；应用没跑时所有命令报 `unable to find Obsidian`。
- **无法创建/注册全新 vault**：vault 相关命令只有 `vault`(看信息) / `vaults`(列出) / `vault:open`(仅 TUI 切换**已有** vault)，没有 create。"从 CLI 把普通文件夹开成 vault"是官方**尚未实现的功能请求**。
- 生成 `.obsidian/`、把目录登记为 vault 只能由 **Obsidian 应用本体首次"以文件夹打开为 vault"** 完成（GUI 操作，或 `open "obsidian://open?path=<dir>"` 触发后人工点确认弹窗）。
- 命令语法 `obsidian <command> [key=value ...]`；`file=` 按 wikilink 名解析、`path=` 按精确路径；agent 输出建议 `format=json`。

**AInews vault 注册现状（2026-06-27）**：已通过 GUI 成功注册——`.obsidian/` 已生成（`app.json` / `appearance.json` / `core-plugins.json` / `workspace.json`），CLI 已打通可用。vault `name=AInews`、`id=5a3c69ef6e15d242`、`path=/Volumes/Projects/AInews`、active=true。git 已 `init` 但**尚无首次提交**，工作区仅有 `CLAUDE.md`（106 字节）。

相关：[[ainews-project-architecture]]。
