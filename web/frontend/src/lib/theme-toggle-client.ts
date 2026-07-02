// AInews · 深色模式切换
// 事件委托挂在 document 上（不是查询单个 button 绑定）——ClientRouter 每次导航都会
// 重新渲染 Header，若直接绑定旧 button 引用，导航后按钮会失去点击响应。
// astro:page-load 在首次加载和每次 view transition 后都会触发，用来同步图标状态。

const STORAGE_KEY = 'ainews-theme'

function currentTheme(): 'light' | 'dark' {
  return document.documentElement.dataset.theme === 'dark' ? 'dark' : 'light'
}

function syncIcon() {
  const icon = document.querySelector<HTMLElement>('[data-theme-toggle] .material-symbols-outlined')
  if (icon) icon.textContent = currentTheme() === 'dark' ? 'light_mode' : 'dark_mode'
}

document.addEventListener('astro:page-load', syncIcon)

document.addEventListener('click', (e) => {
  const target = (e.target as HTMLElement).closest<HTMLElement>('[data-theme-toggle]')
  if (!target) return
  const next: 'light' | 'dark' = currentTheme() === 'dark' ? 'light' : 'dark'
  document.documentElement.dataset.theme = next
  localStorage.setItem(STORAGE_KEY, next)
  syncIcon()
})
