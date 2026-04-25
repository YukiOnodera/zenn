#!/usr/bin/env python3
"""
Translates new Zenn articles (Japanese) to English and posts them as Substack drafts.

Triggered by GitHub Actions on push to main when articles/*.md changes.
Only processes NEW files with published: true in frontmatter.
"""

import os
import sys
import re
import requests
import anthropic
import markdown as md_lib
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SUBSTACK_DIR = REPO_ROOT / "substack"


def parse_frontmatter(content: str) -> tuple[dict, str]:
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    meta = yaml.safe_load(parts[1]) or {}
    return meta, parts[2].strip()


def translate_with_claude(source_content: str) -> tuple[str, str]:
    """Translate article using Claude. Returns (title_en, body_md)."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    meta, body = parse_frontmatter(source_content)
    title_ja = meta.get("title", "")

    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=4096,
        system=(
            "You are a technical writer translating Japanese engineering blog posts "
            "into English for a Substack newsletter focused on Datadog and Observability. "
            "Write naturally and precisely. Preserve all code blocks and ASCII diagrams exactly."
        ),
        messages=[
            {
                "role": "user",
                "content": f"""Translate the following Japanese Zenn article into English for Substack.

Original title: {title_ja}

Article body:
---
{body}
---

Requirements:
- Create an engaging English title (not a literal translation — make it clear and compelling)
- Translate the body naturally; do not add commentary or meta-notes
- Keep all code blocks, ASCII diagrams, and URLs unchanged
- Slightly expand the introduction to give international readers context
- Add this exact line at the end: "*Subscribe for more Datadog & Observability deep-dives.*"
- Do NOT include YAML frontmatter

Respond in this exact format (nothing before TITLE:):
TITLE: <English title>
---
<Article body in Markdown>""",
            }
        ],
    )

    response = message.content[0].text.strip()
    match = re.match(r"TITLE:\s*(.+?)\n---\n(.+)", response, re.DOTALL)
    if not match:
        raise ValueError(f"Unexpected Claude response format:\n{response[:200]}")

    title_en = match.group(1).strip()
    body_en = match.group(2).strip()
    return title_en, body_en


def make_session(cookie: str, pub_url: str) -> requests.Session:
    """Create an authenticated session using a Substack session cookie (substack.sid)."""
    from urllib.parse import urlparse
    parsed = urlparse(pub_url.rstrip("/"))
    origin = f"{parsed.scheme}://{parsed.netloc}"

    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Content-Type": "application/json",
        "Origin": origin,
        "Referer": f"{origin}/",
    })
    session.cookies.set("substack.sid", cookie, domain=".substack.com")
    session.cookies.set("substack.sid", cookie, domain=parsed.netloc)
    return session


def create_substack_draft(session: requests.Session, pub_url: str, title: str, body_md: str) -> str:
    """Post a draft to Substack. Returns the draft URL (empty string on failure)."""
    body_html = md_lib.markdown(body_md, extensions=["fenced_code", "tables"])
    pub_url = pub_url.rstrip("/")

    resp = session.post(
        f"{pub_url}/api/v1/drafts",
        json={
            "draft_title": title,
            "draft_subtitle": "",
            "draft_body": body_html,
            "draft_cover_image": None,
            "audience": "everyone",
            "type": "newsletter",
        },
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    draft_id = data.get("id", "")
    return f"{pub_url}/publish/post/{draft_id}" if draft_id else ""


def save_substack_file(slug: str, source_name: str, title: str, body: str, draft_url: str, published_zenn: bool):
    eng_path = SUBSTACK_DIR / f"{slug}-eng.md"
    content = f"""---
zenn_source: articles/{source_name}
published_zenn: {str(published_zenn).lower()}
substack_status: draft
substack_url: "{draft_url}"
---

# {title}

{body}
"""
    eng_path.write_text(content)
    print(f"Saved: {eng_path.relative_to(REPO_ROOT)}")


def update_readme(slug: str, source_name: str, draft_url: str):
    readme = SUBSTACK_DIR / "README.md"
    content = readme.read_text()
    eng_file = f"{slug}-eng.md"
    new_row = f"| [{eng_file}](./{eng_file}) | articles/{source_name} | ✓ | Draft | {draft_url or '—'} |"

    # Append row before the blank line after the table header separator
    content = content.replace(
        "|----|",
        f"|----|",
        1,
    )
    # Append new row at end of table (before the first blank line after the header)
    lines = content.splitlines()
    insert_at = None
    in_table = False
    for i, line in enumerate(lines):
        if line.startswith("|---"):
            in_table = True
            continue
        if in_table and not line.startswith("|"):
            insert_at = i
            break
    if insert_at is not None:
        lines.insert(insert_at, new_row)
        content = "\n".join(lines) + "\n"
    readme.write_text(content)


def process_file(filepath: str):
    path = Path(filepath)
    if not path.exists():
        print(f"Skip {filepath}: not found")
        return

    content = path.read_text()
    meta, _ = parse_frontmatter(content)

    if not meta.get("published", False):
        print(f"Skip {path.name}: published=false")
        return

    slug = path.stem
    eng_path = SUBSTACK_DIR / f"{slug}-eng.md"
    if eng_path.exists():
        print(f"Skip {path.name}: English version already exists")
        return

    print(f"Translating {path.name} ...")
    title_en, body_en = translate_with_claude(content)
    print(f"  → {title_en}")

    draft_url = ""
    cookie = os.environ.get("SUBSTACK_SESSION_COOKIE", "")
    pub_url = os.environ.get("SUBSTACK_PUBLICATION_URL", "")

    if cookie and pub_url:
        try:
            print("  → Posting to Substack ...")
            session = make_session(cookie, pub_url)
            draft_url = create_substack_draft(session, pub_url, title_en, body_en)
            print(f"  → Draft: {draft_url}")
        except Exception as e:
            print(f"  Warning: Substack post failed ({e})", file=sys.stderr)
    else:
        print("  → Substack credentials not configured — file only")

    save_substack_file(
        slug=slug,
        source_name=path.name,
        title=title_en,
        body=body_en,
        draft_url=draft_url,
        published_zenn=bool(meta.get("published", False)),
    )
    update_readme(slug, path.name, draft_url)


def main():
    new_files = os.environ.get("NEW_FILES", "").split()
    if not new_files:
        print("No new files to process")
        return
    for f in new_files:
        process_file(f)


if __name__ == "__main__":
    main()
