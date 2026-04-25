#!/bin/bash
# Translate a Zenn article to English and open for Substack posting.
# Usage: bash scripts/post.sh articles/<slug>.md

set -e

ARTICLE=${1:?"Usage: $0 articles/<slug>.md"}
SLUG=$(basename "$ARTICLE" .md)
HTML="substack/${SLUG}-eng.html"

# Already translated — just open
if [ -f "$HTML" ]; then
  echo "Already translated → opening"
  open "$HTML"
  exit 0
fi

# Require ANTHROPIC_API_KEY
if [ -z "$ANTHROPIC_API_KEY" ]; then
  echo "Error: ANTHROPIC_API_KEY is not set"
  exit 1
fi

# Set up venv if needed
if [ ! -f ".venv/bin/python" ]; then
  echo "Setting up Python environment..."
  python3 -m venv .venv
  .venv/bin/pip install -q -r scripts/requirements.txt
fi

echo "Translating $ARTICLE ..."
NEW_FILES="$ARTICLE" .venv/bin/python scripts/translate_and_draft.py

echo "Opening in browser..."
open "$HTML"
