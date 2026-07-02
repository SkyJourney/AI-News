// AInews · 自建 mini remark wiki-link 插件
// 把 markdown 里的 [[slug]] 或 [[slug|display]] 转成 mdast link 节点
// 参考格式：`<a class="wikilink" href="/{segment}/{slug}/">{display}</a>`

import { visit } from 'unist-util-visit'
import type { Root, Text, Link, PhrasingContent } from 'mdast'
import type { Plugin } from 'unified'
import { slugToHref } from './slug-utils'

const WIKI_LINK_RE = /\[\[([^\]]+)\]\]/g

/**
 * 把一段 text 拆成 (Text | Link)[] —— 每个 [[wiki]] 变 Link 节点
 * @returns 若无 wikilink 返回 null，否则返回拆分后的节点数组
 */
function splitTextByWikilink(value: string): PhrasingContent[] | null {
  if (!value.includes('[[')) return null
  const parts: PhrasingContent[] = []
  let lastIndex = 0
  let m: RegExpExecArray | null
  WIKI_LINK_RE.lastIndex = 0
  while ((m = WIKI_LINK_RE.exec(value)) !== null) {
    // 前置普通文本
    if (m.index > lastIndex) {
      parts.push({ type: 'text', value: value.slice(lastIndex, m.index) } as Text)
    }
    const raw = m[1].trim()
    // alias 语法 [[target|display]]
    const [rawTarget, rawDisplay] = raw.split('|').map((s) => s.trim())
    // section 链接 [[target#heading]]（v1 不支持，剥掉）
    const target = rawTarget.split('#')[0].trim()
    const display = rawDisplay ?? target
    parts.push({
      type: 'link',
      url: slugToHref(target),
      title: null,
      children: [{ type: 'text', value: display } as Text],
      data: {
        hProperties: { className: ['wikilink'], 'data-wiki-target': target },
      },
    } as Link)
    lastIndex = m.index + m[0].length
  }
  if (parts.length === 0) return null
  // 剩余尾部
  if (lastIndex < value.length) {
    parts.push({ type: 'text', value: value.slice(lastIndex) } as Text)
  }
  return parts
}

/** remark 插件 · 遍历所有 text 节点，把 [[wiki]] 拆成 link */
export const remarkWikiLink: Plugin<[], Root> = () => {
  return (tree) => {
    visit(tree, 'text', (node, index, parent) => {
      if (!parent || index == null) return
      // 跳过 code / inlineCode 里的 text（visit 默认不进 code，但保险）
      const parentType = (parent as { type: string }).type
      if (parentType === 'code' || parentType === 'inlineCode') return
      const replacement = splitTextByWikilink((node as Text).value)
      if (!replacement) return
      ;(parent as { children: PhrasingContent[] }).children.splice(
        index,
        1,
        ...replacement,
      )
      return index + replacement.length // 跳过我们刚插入的节点
    })
  }
}
