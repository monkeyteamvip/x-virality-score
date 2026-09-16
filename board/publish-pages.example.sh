#!/usr/bin/env bash
# Publish board/index.html + board/data.json to YOUR GitHub Pages repo.
# Requires: gh auth login (repo scope). No tokens in this file.
set -euo pipefail
OWNER="${BOARD_OWNER:?set BOARD_OWNER to your GitHub user/org}"
REPO="${BOARD_REPO:?set BOARD_REPO e.g. x-virality-board}"
ROOT="$(cd "$(dirname "$0")" && pwd)"
BRANCH="${BOARD_BRANCH:-main}"

upload() {
  local path="$1"
  local file="$2"
  local msg="$3"
  local b64 sha
  b64=$(base64 -w0 "$file")
  sha=$(gh api "repos/$OWNER/$REPO/contents/$path" --jq .sha 2>/dev/null || true)
  if [ -n "${sha:-}" ]; then
    jq -n --arg msg "$msg" --arg content "$b64" --arg sha "$sha" --arg branch "$BRANCH" \
      '{message:$msg,content:$content,sha:$sha,branch:$branch}' \
      | gh api "repos/$OWNER/$REPO/contents/$path" -X PUT --input - >/dev/null
  else
    jq -n --arg msg "$msg" --arg content "$b64" --arg branch "$BRANCH" \
      '{message:$msg,content:$content,branch:$branch}' \
      | gh api "repos/$OWNER/$REPO/contents/$path" -X PUT --input - >/dev/null
  fi
  echo "uploaded $path"
}

# Create repo if missing (public)
if ! gh api "repos/$OWNER/$REPO" >/dev/null 2>&1; then
  gh repo create "$OWNER/$REPO" --public --description "My X Virality Score board" >/dev/null
  echo "created $OWNER/$REPO"
fi

upload index.html "$ROOT/index.html" "Update board index.html"
upload data.json "$ROOT/data.json" "Update board data.json"

# Enable Pages from main /
gh api "repos/$OWNER/$REPO/pages" -X POST --input - <<JSON >/dev/null 2>&1 || true
{"build_type":"legacy","source":{"branch":"$BRANCH","path":"/"}}
JSON

echo "Board URL (after Pages builds): https://${OWNER}.github.io/${REPO}/"
