// @ts-check
import { defineConfig } from 'astro/config';

import preact from '@astrojs/preact';

import tailwindcss from '@tailwindcss/vite';

// AInews · Obsidian [[wikilink]] → <a> 转换（自建 mini remark 插件）
import { remarkWikiLink } from './src/lib/wiki-link.ts';

// https://astro.build/config
export default defineConfig({
  integrations: [preact()],

  markdown: {
    remarkPlugins: [remarkWikiLink],
    // Astro 内置 gfm + smartypants 保留（GFM 表格 / 任务列表原生支持）
  },

  vite: {
    plugins: [tailwindcss()]
  }
});
