// AInews · 顶栏全站搜索触发按钮（Preact island）
// v1：点击 alert 提示 v2 上线（v2 实现 pagefind 或 fuse.js 索引）
// 视觉：玻璃拟态 pill 带快捷键 hint

import { useState, useEffect } from 'preact/hooks'

export default function GlassSearchBar() {
  const [macOs, setMacOs] = useState(false)
  useEffect(() => {
    setMacOs(navigator.platform.toUpperCase().includes('MAC'))
  }, [])
  const modKey = macOs ? '⌘' : 'Ctrl'

  const onClick = () => {
    // v2 hook：打开搜索 modal
    alert('全站搜索计划 v2 上线（v1 请用浏览器 ⌘F）')
  }

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault()
        onClick()
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [])

  return (
    <button
      class="lumina-searchbar"
      onClick={onClick}
      aria-label="全站搜索（v2）"
    >
      <span class="material-symbols-outlined lumina-searchbar-icon">search</span>
      <span class="lumina-searchbar-hint">
        <kbd>{modKey}</kbd>
        <kbd>K</kbd>
      </span>
      <style>{`
        .lumina-searchbar {
          display: inline-flex;
          align-items: center;
          gap: 0.75rem;
          padding: 0.4rem 0.75rem 0.4rem 0.85rem;
          background: var(--surface-container);
          border: 1px solid var(--glass-border-panel);
          border-radius: var(--radius-full);
          color: var(--color-darkgray);
          font-family: var(--font-header);
          font-size: 0.8rem;
          cursor: pointer;
          transition: background 0.15s ease, border-color 0.15s ease;
        }
        .lumina-searchbar:hover {
          background: var(--surface-container-high);
          border-color: var(--color-secondary);
          color: var(--color-dark);
        }
        .lumina-searchbar-icon {
          font-size: 1.1rem;
        }
        .lumina-searchbar-hint {
          display: inline-flex;
          gap: 0.15rem;
        }
        .lumina-searchbar-hint kbd {
          font-family: var(--font-code);
          background: var(--surface-container-highest);
          color: var(--color-darkgray);
          padding: 0.1rem 0.35rem;
          border-radius: var(--radius-sm);
          font-size: 0.7rem;
          box-shadow: 0 1px 0 var(--color-lightgray);
        }
      `}</style>
    </button>
  )
}
