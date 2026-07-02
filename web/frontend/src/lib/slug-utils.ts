// AInews · vault slug 工具
// vault 目录 → 前端 URL segment 的归一化映射
// 用于 wikilink 路由、backlinks 分组、collection ID 生成

/** vault 5 大目录 → 前端 URL segment（小写） */
export const VAULT_DIRS = {
  daily: '10-Daily',
  topics: '20-Topics',
  deepDives: '40-Deep-Dives',
  zettel: '50-Zettel',
  originals: '60-Originals',
} as const

/** 前端 URL segment（用于生成 href） */
export const URL_SEGMENTS = {
  daily: 'daily',
  topics: 'topics',
  deepDives: 'deep-dives',
  zettel: 'zettel',
  originals: 'originals',
} as const

export type VaultDir = keyof typeof VAULT_DIRS
export type UrlSegment = (typeof URL_SEGMENTS)[VaultDir]

/**
 * 根据 slug 命名规则判定归属目录
 * - `YYYY-MM-DD-HHMM-*` (17+ 字符, 双日期) → originals
 * - `YYYYMMDDHHMM-*` (12 位数字 + slug) → zettel
 * - `YYYY-MM-DD` (10 字符) → daily
 * - 其他 → topics（默认）
 */
export function classifySlug(slug: string): UrlSegment {
  // Originals: 2026-07-01-0901-<slug>
  if (/^\d{4}-\d{2}-\d{2}-\d{4}-/.test(slug)) return URL_SEGMENTS.originals
  // Zettel: 202607010919-<slug>
  if (/^\d{12}-/.test(slug)) return URL_SEGMENTS.zettel
  // Daily: 2026-07-01
  if (/^\d{4}-\d{2}-\d{2}$/.test(slug)) return URL_SEGMENTS.daily
  // 其他都当 topic slug
  return URL_SEGMENTS.topics
}

/**
 * 生成 wikilink 目标 URL
 * @example
 *   slugToHref('2026-07-01')                → '/daily/2026-07-01/'
 *   slugToHref('202607010919-async-pipeline') → '/zettel/202607010919-async-pipeline/'
 *   slugToHref('model-releases')             → '/topics/model-releases/'
 */
export function slugToHref(slug: string): string {
  const segment = classifySlug(slug)
  return `/${segment}/${slug}/`
}

/** vault filepath 相对根 → slug（stem，去 .md 和目录前缀） */
export function filePathToSlug(relativePath: string): string {
  // 例：'10-Daily/2026-07-01.md' → '2026-07-01'
  const parts = relativePath.split('/')
  const filename = parts[parts.length - 1]
  return filename.replace(/\.md$/, '')
}

/** 目录中文标签（用于 backlinks 分栏 header） */
export const DIR_LABELS: Record<UrlSegment, string> = {
  daily: '每日简报',
  topics: '主题',
  'deep-dives': '深度专题',
  zettel: '原子卡片',
  originals: '原文归档',
}
