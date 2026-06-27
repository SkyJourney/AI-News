#!/usr/bin/env bash
# source-health.sh — 对 references/sources.md 中所有 url 做 HEAD 检查
# 输出：单行 JSON {"alive":[{name,url,status}], "dead":[{name,url,status}], "checked_at":"..."}
# 实现：用 grep 抽出 name+url 配对，curl -I --max-time 10 检查
# 不解析 YAML（避免 yq 依赖），约定 sources.md 中每个 source 块以 `- name:` 起首、紧邻 `url:` 在 2-6 行内
# 使用：bash ${CLAUDE_SKILL_DIR}/scripts/source-health.sh

set -euo pipefail

SOURCES_MD="${SOURCES_MD:-$(dirname "$0")/../references/sources.md}"

if [[ ! -f "$SOURCES_MD" ]]; then
  echo '{"error":"sources.md not found","path":"'"$SOURCES_MD"'"}' >&2
  exit 2
fi

# 抽出 name + url 配对：用 awk 状态机扫描 yaml 列表
pairs=$(awk '
  /^[[:space:]]*-[[:space:]]*name:[[:space:]]*/ {
    sub(/^[[:space:]]*-[[:space:]]*name:[[:space:]]*/, "")
    name=$0
    next
  }
  /^[[:space:]]+url:[[:space:]]*/ {
    if (name != "") {
      sub(/^[[:space:]]+url:[[:space:]]*/, "")
      print name "\t" $0
      name=""
    }
  }
' "$SOURCES_MD")

if [[ -z "$pairs" ]]; then
  echo '{"error":"no sources parsed from sources.md"}' >&2
  exit 3
fi

alive_json=""
dead_json=""

while IFS=$'\t' read -r name url; do
  [[ -z "$url" ]] && continue
  # arXiv-style API endpoints 不接受裸 HEAD，必须带参数 GET
  if [[ "$url" == *"export.arxiv.org/api/query"* ]]; then
    probe_url="${url}?search_query=cat:cs.AI&max_results=1"
    method_args=(-sS -L --max-time 10 -o /dev/null)
  else
    probe_url="$url"
    method_args=(-sS -I -L --max-time 10 -o /dev/null)
  fi
  # 先用浏览器 UA 试（绕过 qbitai 等 anti-bot）
  ua="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
  status=$(curl "${method_args[@]}" -w "%{http_code}" -H "User-Agent: $ua" "$probe_url" 2>/dev/null || echo "000")
  # 浏览器 UA 失败时回退到无 UA（meta-ai-blog 类站点对浏览器 UA HEAD 返 400）
  if [[ ! "$status" =~ ^[23][0-9][0-9]$ ]]; then
    status=$(curl "${method_args[@]}" -w "%{http_code}" "$probe_url" 2>/dev/null || echo "000")
  fi
  entry='{"name":"'"$name"'","url":"'"$url"'","status":'"$status"'}'
  # 2xx/3xx 视为 alive；其余 dead
  if [[ "$status" =~ ^[23][0-9][0-9]$ ]]; then
    alive_json+="${alive_json:+,}$entry"
  else
    dead_json+="${dead_json:+,}$entry"
  fi
done <<< "$pairs"

checked_at=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo '{"alive":['"$alive_json"'],"dead":['"$dead_json"'],"checked_at":"'"$checked_at"'"}'
