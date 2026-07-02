// AInews · Content Collections 定义
// 5 大 vault 目录各定义一个 collection，走自定义 vaultLoader
// zod schema 直接来自 vault 落盘公约（.claude/skills/ai-news/references/vault-schema.md）
// backlinks 字段由 vaultLoader 注入（跨 collection 反向 map）

import { defineCollection, z } from 'astro:content'
import { vaultLoader } from './lib/vault-loader'
import { VAULT_DIRS } from './lib/slug-utils'

/** 通用 backlinks / wikilinks 字段（由 vaultLoader 注入到所有 collection） */
const linkFields = {
  wikilinks: z.array(z.string()).default([]),
  backlinks: z
    .array(
      z.object({
        fromSlug: z.string(),
        fromDir: z.enum(Object.keys(VAULT_DIRS) as [string, ...string[]]),
      }),
    )
    .default([]),
}

const daily = defineCollection({
  loader: vaultLoader('daily'),
  schema: z.object({
    created: z.coerce.date(),
    status: z.enum(['published', 'draft']).default('published'),
    entry_count: z.number(),
    sources_alive: z.number(),
    sources_dead: z.number(),
    topics: z.array(z.string()).default([]),
    tags: z.array(z.string()).default([]),
    previous_daily: z.string().optional(),
    ...linkFields,
  }),
})

const topics = defineCollection({
  loader: vaultLoader('topics'),
  schema: z.object({
    created: z.coerce.date(),
    updated: z.coerce.date(),
    entry_total: z.number(),
    ...linkFields,
  }),
})

const zettel = defineCollection({
  loader: vaultLoader('zettel'),
  schema: z.object({
    created: z.coerce.date(),
    updated: z.coerce.date().optional(),
    status: z.enum(['draft', 'published']).default('draft'),
    source: z.string(),
    source_url: z.string().url(),
    topic: z.string(),
    tags: z.array(z.string()).default([]),
    ...linkFields,
  }),
})

const originals = defineCollection({
  loader: vaultLoader('originals'),
  schema: z.object({
    id: z.string(),
    type: z.literal('source-original'),
    title: z.string(),
    original_title: z.string().optional(),
    source_name: z.string(),
    source_url: z.string().url(),
    author: z.array(z.string()).default([]),
    published_at: z.coerce.date(),
    fetched_at: z.coerce.date(),
    language: z.string(),
    translated: z.boolean(),
    translation_engine: z.string().optional(),
    word_count: z.number(),
    images_attempted: z.number().default(0),
    images_saved: z.number().default(0),
    fallback_notice: z.string().optional(),
    related_daily: z.string().optional(),
    related_zettels: z.array(z.string()).default([]),
    related_topics: z.array(z.string()).default([]),
    tags: z.array(z.string()).default([]),
    ...linkFields,
  }),
})

const deepDives = defineCollection({
  loader: vaultLoader('deepDives'),
  schema: z.object({
    // v1 空目录，schema 预留 v2 结构
    created: z.coerce.date().optional(),
    title: z.string().optional(),
    tags: z.array(z.string()).default([]),
    ...linkFields,
  }),
})

export const collections = {
  daily,
  topics,
  zettel,
  originals,
  'deep-dives': deepDives,
}
