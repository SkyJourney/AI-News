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
    out.push({
      vaultDir,
      slug,
      filePath,
      frontmatter: parsed.data,
      body: parsed.content,
      wikilinks: extractWikilinks(parsed.content),
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

/** 只读缓存 API，用于跨 collection 反查（Backlinks / RelatedIntelligence 组件用） */
export async function getVaultCache(): Promise<VaultCache> {
  return loadVaultCache()
}
