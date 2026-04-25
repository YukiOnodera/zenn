---
title: Zenn の記事を Qiita・dev.to・Substack に自動投稿するフローを作った
emoji: 🚀
type: tech
topics:
  - Zenn
  - Qiita
  - devto
  - Substack
  - Python
published: false
---

# はじめに

今回は、Zenn に書いた記事を Qiita・dev.to・Substack に自動投稿するフローを作った話をまとめます。

記事を書くたびに複数のプラットフォームへ手動で投稿するのは地味に手間がかかります。各プラットフォームの API を使えば自動化できるので、`post.sh` にまとめて一括実行できるようにしました。

# 全体フローの概要

投稿先は 3 つに分けて考えています。

| プラットフォーム | 言語 | 方式 |
|---|---|---|
| Qiita | 日本語（Zenn 原文） | API で全自動 |
| dev.to | 英語（Claude で翻訳） | API で全自動 |
| Substack | 英語（同上） | 半自動（コピペ） |

実行はすべて `post.sh` に集約しています。

```sh
# Qiita のみ
bash scripts/post.sh articles/<slug>.md --qiita

# Substack のみ（翻訳 + ブラウザで開く）
bash scripts/post.sh articles/<slug>.md

# すべて
bash scripts/post.sh articles/<slug>.md --all
```

# Qiita 投稿（日本語そのまま）

**Qiita API v2** を使い、Zenn の Markdown をそのまま POST します。

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

Zenn のフロントマターにある `topics` をそのままタグとして使えるので変換は不要です。

## Zenn 記法の自動変換

Qiita は Zenn 独自の記法を解釈しないため、以下を自動変換しています。

| Zenn 記法 | 変換後 |
|---|---|
| `:::message` | `>` blockquote |
| `:::message alert` | `> ⚠️` blockquote |
| `:::details タイトル` | `**タイトル**` + 本文 |
| `@[card](url)` | URL のみ |

## state.json で投稿管理

投稿済みかどうかを `qiita/state.json` で管理しています。

```json
{
  "my-article-slug": {
    "item_id": "abc123",
    "url": "https://qiita.com/items/abc123"
  }
}
```

再実行すると `item_id` を参照して PATCH（更新）に切り替わるため、べき等に動作します。

# dev.to 投稿（英語版）

英語版は事前に Claude で翻訳した `substack/<slug>-eng.md` を使います。

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

## canonical_url で SEO 対策

`canonical_url` に Zenn の記事 URL を設定することで、dev.to 側が「こちらは転載です」と検索エンジンに伝えてくれます。重複コンテンツのペナルティを避けられるので必ず設定しましょう。

:::message
dev.to のタグは最大 4 つ、英数字とアンダースコアのみ有効です。Zenn の topics から自動で変換しています。
:::

# Substack（半手動）

Substack は現状 API が公開されておらず、全自動は難しいです。代わりに以下の方法で対応しています。

1. Claude が Markdown を HTML に変換してブラウザで開く
2. `Cmd+A` → `Cmd+C` でコピー
3. Substack の New Article にペースト → Publish

手間ではありますが、Substack のエディタが HTML のペーストをそのまま受け付けてくれるのでフォーマットは崩れません。

# .env で認証情報を管理

各サービスのトークンは `.env` にまとめています。

```sh:.env.example
ANTHROPIC_API_KEY=sk-ant-...
QIITA_TOKEN=...
DEV_TO_API_KEY=...
ZENN_USERNAME=...
```

`post.sh` の先頭で `source .env` するため、毎回 export する必要はありません。`.env` は `.gitignore` に追加して誤コミットを防いでいます。

# おわりに

API さえあれば記事の配信先を増やすのは意外と手軽です。

Qiita と dev.to は完全自動化できたので、記事を書いたら `bash scripts/post.sh articles/<slug>.md --all` を叩くだけで配信できます。Substack の API が公開されることに期待しつつ、当面はこのフローで運用していきます。

# こちらもおすすめ

https://zenn.dev/yukionodera/articles/feat-pragent

https://zenn.dev/yukionodera/articles/aws-ecr-cost-debug

https://zenn.dev/yukionodera/articles/chezmoi-use-template
