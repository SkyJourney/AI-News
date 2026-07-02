#!/usr/bin/env bash
# test-fetcher.sh — 单源调试入口，不必跑全 /ai-news pipeline
# 用法: bash test-fetcher.sh <source_name>
# 输出: 元数据 + 活性 + 内容采样 + 后续 spawn 命令模板

set -euo pipefail

SOURCE_NAME="${1:?用法: test-fetcher.sh <source_name>，如 openai-rss}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCES_MD="$SCRIPT_DIR/../references/sources.md"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

# === 1. 从 sources.md 抽出该 source 块 ===
BLOCK=$(awk -v target="$SOURCE_NAME" '
  /^[[:space:]]*-[[:space:]]*name:[[:space:]]*/ {
    n=$0; sub(/^[[:space:]]*-[[:space:]]*name:[[:space:]]*/, "", n)
    in_block = (n == target)
    if (in_block) print "  name: " n
    next
  }
  in_block && /^[[:space:]]+(url|fetch_method|tier|perspective|reliability|fallback|last_verified|notes):/ { print }
  /^[[:space:]]*-[[:space:]]*name:/ { in_block=0 }
' "$SOURCES_MD")

if [[ -z "$BLOCK" ]]; then
  echo "❌ source '$SOURCE_NAME' 不在 sources.md。可用源：" >&2
  grep -E '^[[:space:]]*-[[:space:]]*name:' "$SOURCES_MD" | sed 's/^[[:space:]]*-[[:space:]]*name:[[:space:]]*/  /' >&2
  exit 1
fi

echo "=== 1. 源元数据 ==="
echo "$BLOCK"
echo ""

URL=$(echo "$BLOCK" | awk '/^[[:space:]]*url:/ {print $2; exit}')
FETCH=$(echo "$BLOCK" | awk '/^[[:space:]]*fetch_method:/ {print $2; exit}')

# === 2. 活性检查（与 source-health.sh 同逻辑） ===
echo "=== 2. 活性 (HEAD with UA → fallback no-UA) ==="
if [[ "$URL" == *"export.arxiv.org/api/query"* ]]; then
  PROBE="${URL}?search_query=cat:cs.AI&max_results=1"
  ARGS=(-sS -L --max-time 10 -o /dev/null)
else
  PROBE="$URL"
  ARGS=(-sS -I -L --max-time 10 -o /dev/null)
fi
status=$(curl "${ARGS[@]}" -w "%{http_code}" -H "User-Agent: $UA" "$PROBE" 2>/dev/null || echo "000")
[[ ! "$status" =~ ^[23] ]] && status=$(curl "${ARGS[@]}" -w "%{http_code}" "$PROBE" 2>/dev/null || echo "000")
echo "HTTP $status"
echo ""

# === 3. 内容采样 ===
echo "=== 3. 内容采样 ==="
case "$FETCH" in
  rss)
    echo "(raw RSS/Atom 前 60 行，便于看条目结构)"
    curl -sS -L --max-time 30 -H "User-Agent: $UA" "$URL" 2>/dev/null | head -60
    ;;
  webfetch)
    echo "(HTML 前 60 行，看页面结构)"
    curl -sS -L --max-time 30 -H "User-Agent: $UA" "$URL" 2>/dev/null | head -60
    ;;
  api)
    if [[ "$SOURCE_NAME" == "arxiv-api" ]]; then
      echo "(arxiv-fetch.py 抽 3 条解析后标题)"
      "$HOME/miniconda3/envs/ai-news/bin/python3" "$SCRIPT_DIR/arxiv-fetch.py" --max 3 2>/dev/null \
        | "$HOME/miniconda3/envs/ai-news/bin/python3" -c "import json,sys; d=json.load(sys.stdin); [print(f'  [{e[\"published\"][:10]}] {e[\"title\"]}') for e in d.get('entries', [])[:3]]" \
        || echo "(arxiv-fetch.py 失败)"
    elif [[ "$SOURCE_NAME" == "huggingface-daily-papers" ]]; then
      today=$(date +%F)
      echo "(HF Daily Papers @ ${today}, top 3)"
      curl -sS --max-time 15 -H "User-Agent: $UA" "${URL}?date=${today}" \
        | "$HOME/miniconda3/envs/ai-news/bin/python3" -c "import json,sys; d=json.load(sys.stdin); print(f'  count={len(d)}'); [print(f'  - {p.get(\"paper\",{}).get(\"title\",\"?\")}') for p in d[:3]]" 2>/dev/null \
        || echo "(empty or parse error；可能要试 yesterday)"
    else
      echo "(未知 api 类型: $SOURCE_NAME)"
    fi
    ;;
  *)
    echo "(未知 fetch_method: $FETCH)"
    ;;
esac
echo ""

# === 4. 后续 spawn 命令模板 ===
echo "=== 4. Claude 会话 spawn 命令模板 ==="
echo "在 Claude Code 会话中复制下面这段（替换 notes 为 sources.md 里实际 notes）："
echo ""
cat <<EOF
Agent(news-fetcher-${FETCH}):
  prompt:
    Fetch source ${SOURCE_NAME}:
    - name: ${SOURCE_NAME}
    - url: ${URL}
    - notes: <copy from sources.md>

    Follow your system prompt to output JSON.
EOF
