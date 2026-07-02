# AInews · Astro 5 静态站点构建镜像
# 仅用于 F2.7 Publish 的 builder profile：docker compose --profile build run --rm builder
# vault 5 目录（10-Daily/20-Topics/40-Deep-Dives/50-Zettel/60-Originals）由 compose 只读挂载，
# 运行时才拿到当天最新内容——不烘进镜像，避免每次内容更新都要重建镜像。
FROM node:22-alpine

WORKDIR /app/web/frontend

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

CMD ["npm", "run", "build"]
