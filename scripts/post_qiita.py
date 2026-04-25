#!/usr/bin/env python3
"""
Post a Zenn article to Qiita via API.
Usage: python scripts/post_qiita.py articles/<slug>.md

Requires: QIITA_TOKEN environment variable
State:    qiita/state.json  (tracks item_id per slug)
"""

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
QIITA_DIR = REPO_ROOT / "qiita"
STATE_FILE = QIITA_DIR / "state.json"
QIITA_API = "https://qiita.com/api/v2"


def parse_frontmatter(content: str) -> tuple[dict, str]:
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    meta = yaml.safe_load(parts[1]) or {}
    return meta, parts[2].strip()


def convert_zenn_to_qiita(body: str) -> str:
    """Convert Zenn-specific syntax to Qiita-compatible Markdown."""
    # :::message alert ... :::
    body = re.sub(
        r":::message alert\n(.*?):::",
        lambda m: "\n".join(
            f"> ⚠️ {line}" if i == 0 else f"> {line}"
            for i, line in enumerate(m.group(1).strip().splitlines())
        ),
        body,
        flags=re.DOTALL,
    )
    # :::message ... :::
    body = re.sub(
        r":::message\n(.*?):::",
        lambda m: "\n".join(f"> {line}" for line in m.group(1).strip().splitlines()),
        body,
        flags=re.DOTALL,
    )
    # :::details Summary\ncontent\n:::
    body = re.sub(
        r":::details (.+?)\n(.*?):::",
        lambda m: f"**{m.group(1).strip()}**\n\n{m.group(2).strip()}",
        body,
        flags=re.DOTALL,
    )
    # @[card](url) → url
    body = re.sub(r"@\[card\]\((.+?)\)", r"\1", body)
    # @[tweet](url) → url
    body = re.sub(r"@\[tweet\]\((.+?)\)", r"\1", body)
    # @[youtube](id) → YouTube URL
    body = re.sub(
        r"@\[youtube\]\((.+?)\)",
        r"https://www.youtube.com/watch?v=\1",
        body,
    )
    return body


def replace_zenn_recommendations(body: str, state: dict, zenn_username: str) -> str:
    """Replace Zenn recommendation URLs with Qiita URLs; remove if not in state."""
    pattern = rf"https://zenn\.dev/{re.escape(zenn_username)}/articles/([a-z0-9_-]+)"

    def replacer(match):
        slug = match.group(1)
        if slug in state:
            return state[slug]["url"]
        return ""

    body = re.sub(pattern, replacer, body)
    # Remove lines that became empty after URL replacement (bare zenn links)
    lines = [l for l in body.splitlines() if l.strip()]
    return "\n".join(lines)


def warn_local_images(slug: str, body: str):
    local_images = re.findall(r"!\[.*?\]\(/images/" + slug + r"/.*?\)", body)
    if local_images:
        print(f"⚠️  {len(local_images)} local image(s) found — they won't render on Qiita.")
        print("   Upload them to Qiita manually or host externally, then update the article.")


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}


def save_state(state: dict):
    QIITA_DIR.mkdir(exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")


def qiita_request(method: str, path: str, data: dict, token: str, retries: int = 3) -> dict:
    url = f"{QIITA_API}{path}"
    payload = json.dumps(data).encode()
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method=method,
    )
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            if e.code == 429 and attempt < retries - 1:
                wait = 60 * (attempt + 1)
                print(f"Rate limited. Waiting {wait}s before retry {attempt + 1}/{retries - 1}...")
                time.sleep(wait)
            else:
                print(f"Qiita API error {e.code}: {body}")
                raise


def post_to_qiita(slug: str, meta: dict, body: str, token: str, state: dict):
    tags = [{"name": t} for t in (meta.get("topics") or [])]
    if not tags:
        tags = [{"name": "Datadog"}]

    zenn_username = os.environ.get("ZENN_USERNAME", "")
    qiita_body = convert_zenn_to_qiita(body)
    qiita_body = replace_zenn_recommendations(qiita_body, state, zenn_username)
    warn_local_images(slug, qiita_body)

    payload = {
        "title": meta.get("title", slug),
        "body": qiita_body,
        "tags": tags,
        "private": not meta.get("published", False),
    }

    item_id = state.get(slug, {}).get("item_id")
    if item_id:
        qiita_request("PATCH", f"/items/{item_id}", payload, token)
        url = state[slug]["url"]
        print(f"Updated: {url}")
    else:
        result = qiita_request("POST", "/items", payload, token)
        item_id = result["id"]
        url = result["url"]
        state[slug] = {"item_id": item_id, "url": url}
        save_state(state)
        print(f"Posted: {url}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/post_qiita.py articles/<slug>.md")
        sys.exit(1)

    token = os.environ.get("QIITA_TOKEN")
    if not token:
        print("Error: QIITA_TOKEN is not set")
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Error: {sys.argv[1]} not found")
        sys.exit(1)

    content = path.read_text()
    meta, body = parse_frontmatter(content)

    if not meta.get("published", False):
        print(f"Skip {path.name}: published=false")
        sys.exit(0)

    slug = path.stem
    state = load_state()
    post_to_qiita(slug, meta, body, token, state)


if __name__ == "__main__":
    main()
