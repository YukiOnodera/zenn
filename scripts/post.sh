#!/bin/bash
# Translate a Zenn article to English and open for Substack posting.
# Optionally post to Qiita / dev.to.
#
# Usage:
#   bash scripts/post.sh articles/<slug>.md             # Substack only
#   bash scripts/post.sh articles/<slug>.md --qiita     # Qiita only
#   bash scripts/post.sh articles/<slug>.md --devto     # dev.to only (requires English version)
#   bash scripts/post.sh articles/<slug>.md --all       # Substack + Qiita + dev.to

set -e

# Load .env if present
if [ -f ".env" ]; then
  set -a; source .env; set +a
fi

ARTICLE=${1:?"Usage: $0 articles/<slug>.md [--qiita|--devto|--all]"}
shift
MODE="substack"
for arg in "$@"; do
  case "$arg" in
    --qiita) MODE="qiita" ;;
    --devto) MODE="devto" ;;
    --all)   MODE="all" ;;
  esac
done

SLUG=$(basename "$ARTICLE" .md)
HTML="substack/${SLUG}-eng.html"

run_substack() {
  if [ -f "$HTML" ]; then
    echo "Already translated → opening"
    open "$HTML"
    return
  fi

  if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "Error: ANTHROPIC_API_KEY is not set"
    exit 1
  fi

  setup_venv

  echo "Translating $ARTICLE ..."
  NEW_FILES="$ARTICLE" .venv/bin/python scripts/translate_and_draft.py

  echo "Opening in browser..."
  open "$HTML"
}

run_qiita() {
  if [ -z "$QIITA_TOKEN" ]; then
    echo "Error: QIITA_TOKEN is not set"
    exit 1
  fi

  setup_venv

  echo "Posting $ARTICLE to Qiita..."
  .venv/bin/python scripts/post_qiita.py "$ARTICLE"
}

run_devto() {
  if [ -z "$DEV_TO_API_KEY" ]; then
    echo "Error: DEV_TO_API_KEY is not set"
    exit 1
  fi

  if [ -z "$ZENN_USERNAME" ]; then
    echo "Error: ZENN_USERNAME is not set"
    exit 1
  fi

  setup_venv

  echo "Posting $ARTICLE to dev.to..."
  .venv/bin/python scripts/post_devto.py "$ARTICLE"
}

setup_venv() {
  if [ ! -f ".venv/bin/python" ]; then
    echo "Setting up Python environment..."
    python3 -m venv .venv
    .venv/bin/pip install -q -r scripts/requirements.txt
  fi
}

case "$MODE" in
  substack) run_substack ;;
  qiita)    run_qiita ;;
  devto)    run_devto ;;
  all)      run_substack; run_qiita; run_devto ;;
esac
