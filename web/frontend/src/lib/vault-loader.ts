// AInews · vault Content Loader
// 从仓库根的 vault 目录读取 markdown，构造 Astro Content Collection entry
// 关键能力：跨 collection backlinks 反向 map（一次全库扫描 · 结果缓存）

import type { Loader } from 'astro/loaders'
import { readFile, readdir, stat } from 'node:fs/promises'
import path from 'node:path'
import matter from 'gray-matter'
import { VAULT_DIRS, type VaultDir, filePathToSlug } from './slug-utils'

/** vault 根 = 仓库根，相对本文件位置 = ../../../.. */
const VAULT_ROOT = path.resolve(import.meta.dirname, '../../../..')

/** 单篇 markdown 的原始解析结果 */
interface RawEntry {
  vaultDir: VaultDir
  slug: string
  filePath: string
  frontmatter: Record<string, unknown>
  body: string
  wikilinks: string[] // 该文档里出现的所有 [[link]] 目标 slug（去重）
}

/** 缓存：全库解析结果 + backlinks 反向 map */
interface VaultCache {
  entries: RawEntry[] // 所有目录的原始 entry
  /** slug → 引用它的 (fromSlug, fromVaultDir) 列表 */
  backlinks: Map<string, Array<{ fromSlug: string; fromDir: VaultDir }>>
}

let cache: VaultCache | null = null
let cachePromise: Promise<VaultCache> | null = null

/** 从一段 markdown body 里提取所有 [[link]] 目标 slug（含 alias 语法 [[a|b]] 取 a 部分） */
function extractWikilinks(body: string): string[] {
  const re = /\[\[([^\]]+)\]\]/g
  const set = new Set<string>()
  let m: RegExpExecArray | null
  while ((m = re.exec(body)) !== null) {
    const raw = m[1].trim()
    // alias 语法 [[target|display]]，取 target
    const target = raw.split('|')[0].trim()
    // 剥掉 #section 部分
    const clean = target.split('#')[0].trim()
    if (clean) set.add(clean)
  }
  return Array.from(set)
}

/**
 * originals 正文开头的 H1 标题与 frontmatter.title 冗余（Astro 详情页已单独渲染一份 H1）：
 * - 旧模板：`# 标题` + `> 原文/抓取` 引用块（agent 曾主动写入，已改模板不再生成，历史文件仍有）
 * - arxiv 通道：原文 HTML/PDF 结构自带 `# 论文标题`（脚本抓取产物，非 agent 主动添加），无引用块跟随
 * 两种情况都只 strip 开头这个 H1（及紧跟的引用块，如果有），不影响其后的正文内容
 * 找不到该模式时原样返回，不影响不以 # 开头的文件
 */
function stripOriginalsHeader(body: string): string {
  // gray-matter 解析出的 content 开头常带一个前导换行，^\s* 兜底吃掉
  // 引用块（若有）后偶尔跟一条原文自带的 --- 分隔线，不吃掉会让剩余 body 以 --- 开头
  // 被 Astro markdown processor 误判成新的 YAML frontmatter 块导致 build 崩溃，一并吃掉
  return body.replace(/^\s*#[^\n]*\n+(?:(?:>.*\n)+\n*(?:---\n+)?)?/, '')
}

/** 扫描单个 vault 目录，产出 RawEntry[] */
async function scanVaultDir(vaultDir: VaultDir): Promise<RawEntry[]> {
  const absDir = path.join(VAULT_ROOT, VAULT_DIRS[vaultDir])
  let files: string[]
  try {
    files = await readdir(absDir)
  } catch {
    return [] // 目录不存在（v1 阶段可能）
  }
  const out: RawEntry[] = []
  for (const filename of files) {
    if (!filename.endsWith('.md') || filename.startsWith('.')) continue
    const filePath = path.join(absDir, filename)
    const st = await stat(filePath)
    if (!st.isFile()) continue
    const raw = await readFile(filePath, 'utf-8')
    const parsed = matter(raw)
    const slug = filePathToSlug(filename)
    let body = parsed.content
    if (vaultDir === 'originals') {
      // 去重：正文开头与 frontmatter 冗余的标题+引用块（详情页已单独渲染）
      body = stripOriginalsHeader(body)
      // 图片是相对路径 _assets/YYYY-MM-DD/xxx.ext（相对 60-Originals/ 本身）
      // sync-assets.mjs 把 _assets/ 物理复制到 public/originals-assets/，这里改写成绝对路径
      // 避免浏览器按当前详情页 URL（/originals/{slug}/）错误解析相对路径导致 404
      body = body.replace(/([("])_assets\//g, '$1/originals-assets/')
    }
    out.push({
      vaultDir,
      slug,
      filePath,
      frontmatter: parsed.data,
      body,
      wikilinks: extractWikilinks(body),
    })
  }
  return out
}

/** 一次全库扫描 + 构造 backlinks 反向 map，结果缓存到 module scope */
async function loadVaultCache(): Promise<VaultCache> {
  if (cache) return cache
  if (cachePromise) return cachePromise
  cachePromise = (async () => {
    const allDirs: VaultDir[] = ['daily', 'topics', 'deepDives', 'zettel', 'originals']
    const entries: RawEntry[] = []
    for (const d of allDirs) {
      const dirEntries = await scanVaultDir(d)
      entries.push(...dirEntries)
    }
    const backlinks = new Map<string, Array<{ fromSlug: string; fromDir: VaultDir }>>()
    for (const entry of entries) {
      for (const target of entry.wikilinks) {
        if (!backlinks.has(target)) backlinks.set(target, [])
        backlinks.get(target)!.push({ fromSlug: entry.slug, fromDir: entry.vaultDir })
      }
    }
    cache = { entries, backlinks }
    return cache
  })()
  return cachePromise
}

/**
 * 工厂函数：给一个 vaultDir 返回一个 Astro Content Loader
 * Loader 内部会触发一次全库扫描（幂等缓存），然后 push 属于本 dir 的 entry 到 store
 */
export function vaultLoader(vaultDir: VaultDir): Loader {
  return {
    name: `vault-loader:${vaultDir}`,
    async load({ store, logger, renderMarkdown }) {
      store.clear()
      const { entries, backlinks } = await loadVaultCache()
      const mine = entries.filter((e) => e.vaultDir === vaultDir)
      logger.info(`${vaultDir}: ${mine.length} entries`)
      for (const entry of mine) {
        const rendered = await renderMarkdown(entry.body)
        const bls = backlinks.get(entry.slug) ?? []
        store.set({
          id: entry.slug,
          data: {
            ...entry.frontmatter,
            wikilinks: entry.wikilinks,
            backlinks: bls,
          },
          body: entry.body,
          rendered,
        })
      }
    },
  }
}

/**
 * 只读缓存 API，用于跨 collection 反查（Backlinks / RelatedIntelligence 组件、
 * wiki-link.ts 断链判定 + hover 预览都用这个）。
 * 内部按 module 单例记忆化，只有第一次调用会触发全库扫描；后续调用直接拿 resolved 值。
 */
export async function getVaultCache(): Promise<VaultCache> {
  return loadVaultCache()
}
