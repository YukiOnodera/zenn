#!/usr/bin/env python3
"""
Translates new Zenn articles (Japanese) to English and saves them to substack/.

Triggered by GitHub Actions on push to main when articles/*.md changes.
Only processes NEW files with published: true in frontmatter.
"""

import os
import re
import anthropic
import yaml
import markdown as md_lib
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


def strip_recommendations(body: str) -> str:
    """Remove the Zenn-specific '# こちらもおすすめ' section."""
    return re.sub(r"\n# こちらもおすすめ\n[\s\S]*$", "", body).rstrip()


def translate_with_claude(source_content: str) -> tuple[str, str]:
    """Translate article using Claude. Returns (title_en, body_md)."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    meta, body = parse_frontmatter(source_content)
    body = strip_recommendations(body)
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

    return match.group(1).strip(), match.group(2).strip()


def save_translation(slug: str, source_name: str, title: str, body: str):
    eng_path = SUBSTACK_DIR / f"{slug}-eng.md"
    eng_path.write_text(f"""---
zenn_source: articles/{source_name}
substack_status: pending
substack_url: ""
---

# {title}

{body}
""")
    print(f"Saved: {eng_path.relative_to(REPO_ROOT)}")

    # Generate HTML for copy-pasting into Substack
    body_html = md_lib.markdown(body, extensions=["fenced_code", "tables", "nl2br"])
    html_path = SUBSTACK_DIR / f"{slug}-eng.html"
    html_path.write_text(f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{ font-family: Georgia, serif; max-width: 680px; margin: 40px auto; padding: 0 20px; line-height: 1.7; color: #222; }}
  h1, h2, h3 {{ font-family: -apple-system, sans-serif; }}
  pre {{ background: #f4f4f4; padding: 16px; border-radius: 4px; overflow-x: auto; }}
  code {{ font-family: 'Courier New', monospace; font-size: 0.9em; }}
  pre code {{ background: none; }}
  hr {{ border: none; border-top: 1px solid #ddd; margin: 2em 0; }}
</style>
</head>
<body>
<h1>{title}</h1>
{body_html}
</body>
</html>
""")
    print(f"Saved: {html_path.relative_to(REPO_ROOT)}")


def update_readme(slug: str, source_name: str):
    readme = SUBSTACK_DIR / "README.md"
    content = readme.read_text()
    eng_file = f"{slug}-eng.md"
    new_row = f"| [{eng_file}](./{eng_file}) | articles/{source_name} | ✓ | Pending | — |"

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
        readme.write_text("\n".join(lines) + "\n")


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
    if (SUBSTACK_DIR / f"{slug}-eng.md").exists():
        print(f"Skip {path.name}: English version already exists")
        return

    print(f"Translating {path.name} ...")
    title_en, body_en = translate_with_claude(content)
    print(f"  → {title_en}")

    save_translation(slug, path.name, title_en, body_en)
    update_readme(slug, path.name)


def main():
    new_files = os.environ.get("NEW_FILES", "").split()
    if not new_files:
        print("No new files to process")
        return
    for f in new_files:
        process_file(f)


if __name__ == "__main__":
    main()
