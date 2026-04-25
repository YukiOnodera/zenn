---
zenn_source: articles/zenn-multi-platform-auto-post.md
substack_status: pending
substack_url: ""
---

# Cross-Posting Zenn Articles to Qiita, dev.to, and Substack with a Single Script

# Introduction

In this post, I'll walk through the workflow I built to automatically cross-post articles I write on Zenn (a Japanese tech blogging platform) to Qiita, dev.to, and Substack.

If you write on multiple platforms, you've probably felt the friction: every time you publish a post, you end up copy-pasting it into two or three different editors, re-formatting things that don't render the same way, and tweaking tags for each service. It's a small chore, but it adds up — and it's exactly the kind of repetitive task that should be scripted away.

Since each platform exposes (or at least tolerates) some form of programmatic publishing, I wrapped everything in a single `post.sh` so I can fan out a single Markdown file to all destinations with one command. Here's how it's put together.

# Overall Flow

I split the destinations into three categories:

| Platform | Language | Method |
|---|---|---|
| Qiita | Japanese (Zenn original) | Fully automated via API |
| dev.to | English (translated with Claude) | Fully automated via API |
| Substack | English (same as above) | Semi-automated (copy & paste) |

Everything is invoked through `post.sh`:

```sh
# Qiita only
bash scripts/post.sh articles/<slug>.md --qiita

# Substack only (translate + open in browser)
bash scripts/post.sh articles/<slug>.md

# Everything
bash scripts/post.sh articles/<slug>.md --all
```

# Posting to Qiita (Japanese, as-is)

I use the **Qiita API v2** and POST the Zenn Markdown directly.

```python
import json, urllib.request

payload = {
    "title": meta.get("title", slug),
    "body": qiita_body,
    "tags": [{"name": t} for t in topics],
    "private": False,
}
req = urllib.request.Request(
    "https://qiita.com/api/v2/items",
    data=json.dumps(payload).encode(),
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    method="POST",
)
urllib.request.urlopen(req)
```

The `topics` field in Zenn's frontmatter can be reused as Qiita tags directly, so no conversion is needed.

## Auto-converting Zenn-specific syntax

Qiita doesn't understand Zenn's custom Markdown extensions, so I rewrite them on the fly:

| Zenn syntax | Converted to |
|---|---|
| `:::message` | `>` blockquote |
| `:::message alert` | `> ⚠️` blockquote |
| `:::details Title` | `**Title**` + body |
| `@[card](url)` | URL only |

## Tracking posts with state.json

I track which articles have already been posted in `qiita/state.json`:

```json
{
  "my-article-slug": {
    "item_id": "abc123",
    "url": "https://qiita.com/items/abc123"
  }
}
```

If you re-run the script, it looks up the `item_id` and switches to a PATCH (update), so the operation is idempotent.

# Posting to dev.to (English version)

For the English version, I use `substack/<slug>-eng.md`, which is pre-translated with Claude.

```python
import json, urllib.request

payload = {
    "article": {
        "title": title,
        "body_markdown": body,
        "published": True,
        "tags": tags,
        "canonical_url": f"https://zenn.dev/{zenn_username}/articles/{slug}",
    }
}
req = urllib.request.Request(
    "https://dev.to/api/articles",
    data=json.dumps(payload).encode(),
    headers={"api-key": api_key, "Content-Type": "application/json"},
    method="POST",
)
urllib.request.urlopen(req)
```

## SEO with canonical_url

By setting `canonical_url` to the Zenn article URL, dev.to tells search engines, "this is a republished version." This avoids the duplicate-content penalty, so always set it when cross-posting.

:::message
dev.to allows up to 4 tags, and they must contain only alphanumerics and underscores. The script normalizes Zenn's `topics` automatically.
:::

# Substack (semi-manual)

Substack doesn't currently expose a public API, so full automation isn't really feasible. Instead, I do the following:

1. Claude converts the Markdown to HTML, which is then opened in a browser
2. `Cmd+A` → `Cmd+C` to copy
3. Paste into Substack's New Article editor → Publish

It's not zero-effort, but Substack's editor accepts pasted HTML cleanly, so the formatting carries over without breaking.

# Managing credentials with .env

Tokens for each service live in a single `.env` file:

```sh:.env.example
ANTHROPIC_API_KEY=sk-ant-...
QIITA_TOKEN=...
DEV_TO_API_KEY=...
ZENN_USERNAME=...
```

`post.sh` does a `source .env` at the top, so I don't have to export them every time. The file is added to `.gitignore` to prevent accidental commits.

# Wrapping Up

As long as a platform exposes an API, adding it as a publishing destination is surprisingly low-effort.

Qiita and dev.to are now fully automated, so once I've finished writing, all I do is run `bash scripts/post.sh articles/<slug>.md --all`. I'll keep hoping Substack opens up an API someday, but for now this hybrid flow does the job.

# You Might Also Like

https://zenn.dev/yukionodera/articles/feat-pragent

https://zenn.dev/yukionodera/articles/aws-ecr-cost-debug

https://zenn.dev/yukionodera/articles/chezmoi-use-template

*Subscribe for more Datadog & Observability deep-dives.*
