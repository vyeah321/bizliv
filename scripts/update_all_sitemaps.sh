#!/bin/bash
# BizLivポートフォリオ全体 sitemap.xml 自動更新スクリプト（ローカルcron用）
# 各プロパティのリポジトリでgenerate_sitemap.pyを実行し、
# sitemap.xmlに実質的な差分があればローカルにコミットする（pushは手動）。
# lastmodはファイルの実際のmtimeから算出されるため、ローカルの永続的な
# 作業ディレクトリでは編集がない日は差分が出ない（GitHub Actionsの
# fresh checkoutだとmtimeが毎回リセットされ毎日コミットが発生していた）。

PYTHON="/usr/bin/python3"
GIT="/usr/bin/git"
export PATH="/opt/homebrew/bin:/usr/bin:/bin:${PATH}"

LOG_FILE="/Users/atsuvu/bizliv/bizliv/sitemap_update.log"

export GIT_AUTHOR_NAME="BizLiv Sitemap Bot"
export GIT_AUTHOR_EMAIL="bot@bizliv.life"
export GIT_COMMITTER_NAME="BizLiv Sitemap Bot"
export GIT_COMMITTER_EMAIL="bot@bizliv.life"

REPOS=(
  "/Users/atsuvu/bizliv/bizliv"
  "/Users/atsuvu/bizliv/bizliv-coach"
  "/Users/atsuvu/bizliv/bizliv-design"
  "/Users/atsuvu/bizliv/bizliv-apps"
)

update_repo() {
  local repo_dir="$1"
  echo "----- $(basename "$repo_dir") -----"
  cd "$repo_dir" || { echo "ディレクトリ移動に失敗"; return 1; }

  "$GIT" fetch origin main || { echo "git fetch失敗"; return 1; }
  "$GIT" merge --ff-only origin/main || { echo "origin/mainとfast-forwardできないため中断"; return 1; }

  "$PYTHON" scripts/generate_sitemap.py || { echo "generate_sitemap.py失敗"; return 1; }

  if "$GIT" diff --quiet -- sitemap.xml; then
    echo "差分なし。スキップ。"
    return 0
  fi

  "$GIT" add -- sitemap.xml
  "$GIT" commit -m "sitemap.xmlを自動更新" || { echo "git commit失敗"; return 1; }
  echo "sitemap.xmlをローカルにコミットしました(pushは未実施)。"
}

{
  echo "===== $(date '+%Y-%m-%d %H:%M:%S') sitemap自動更新開始 ====="
  for repo in "${REPOS[@]}"; do
    update_repo "$repo"
  done
  echo "===== 終了 ====="
} >> "$LOG_FILE" 2>&1
