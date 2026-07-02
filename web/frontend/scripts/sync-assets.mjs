// AInews · 同步 vault 60-Originals/_assets 图片资产到 public/originals-assets
// build/dev 前跑一次：物理复制而非 symlink，保证产物自包含，兼容未来 F2.7 docker 部署
// （builder 容器只读挂载 vault，build 时把图片拷进 public，dist 不依赖宿主机路径）
import { cp, rm, access } from 'node:fs/promises'
import path from 'node:path'

const SRC = path.resolve(import.meta.dirname, '../../../60-Originals/_assets')
const DEST = path.resolve(import.meta.dirname, '../public/originals-assets')

async function main() {
  try {
    await access(SRC)
  } catch {
    console.log('[sync-assets] 60-Originals/_assets 不存在，跳过同步')
    return
  }
  await rm(DEST, { recursive: true, force: true })
  await cp(SRC, DEST, { recursive: true })
  console.log(`[sync-assets] ${SRC} → ${DEST} 同步完成`)
}

main()
