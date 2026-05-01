# Substack Articles

Zenn記事（日本語）を英語に翻訳してSubstackに投稿するためのディレクトリ。

---

## 記事を書いてから投稿するまでの手順

### Step 1: 記事を書く（`/write-article` スキル）

Claude Codeで `/write-article` を実行。以下の対話が発生する：

| Phase | 内容 | 人間の操作 |
|-------|------|------------|
| 0 ヒアリング | Claudeが質問 | 学んだことを入力 |
| 1 スタイル研究 | 自動 | なし |
| 2 リサーチ | 自動 | なし |
| 3 アウトライン | Claudeが提示 | **承認する** |
| 4 執筆 | 自動 | なし |
| 5 レビュー | 自動 | なし |
| 6 PR作成 | 自動 | **PRをマージする**（GitHub） |
| [zenn-multi-platform-auto-post-eng.md](./zenn-multi-platform-auto-post-eng.md) | articles/zenn-multi-platform-auto-post.md | ✓ | Pending | — |
| [datadog-log-pipeline-overview-eng.md](./datadog-log-pipeline-overview-eng.md) | articles/datadog-log-pipeline-overview.md | ✓ | Pending | — |
| [datadog-apm-python-instrumentation-eng.md](./datadog-apm-python-instrumentation-eng.md) | articles/datadog-apm-python-instrumentation.md | ✓ | Pending | — |

### Step 2: ローカルに反映

```bash
git checkout main && git pull
```

### Step 3: 翻訳 → HTML生成 → ブラウザで開く

```bash
bash scripts/post.sh articles/<slug>.md
```

- `ANTHROPIC_API_KEY` が必要（`~/.zshrc` に設定しておく）
- 初回のみ `.venv` のセットアップが走る（数十秒）
- ブラウザに翻訳済みHTMLが自動で開く

### Step 4: Substackに投稿

1. ブラウザで開いたHTMLを**全選択（`Cmd+A`）→ コピー（`Cmd+C`）**
2. [Substack](https://odryk.substack.com) → **New Article**
3. タイトルを入力（HTMLには含まれていないので手動）
4. 本文エリアに**ペースト**
5. 内容確認して**Publish**

### Step 5: 翻訳ファイルをコミット

```bash
git add substack/ && git commit -m "add: <slug> English draft" && git push
```

投稿後、`substack/<slug>-eng.md` のフロントマターも更新しておくと管理しやすい：

```yaml
substack_status: published
substack_url: "https://odryk.substack.com/p/..."
```

---

## Translation Status

| File | Zenn Source | Zenn Published | Substack Status | Substack URL |
|------|-------------|----------------|-----------------|--------------|
| [datadog-node-agent-cluster-agent-eng.md](./datadog-node-agent-cluster-agent-eng.md) | articles/datadog-node-agent-cluster-agent.md | Draft | Published | [link](https://open.substack.com/pub/odryk/p/why-datadog-uses-two-agents-in-kubernetes) |
| [20231215-ddagent-eks-eng.md](./20231215-ddagent-eks-eng.md) | articles/20231215-ddagent-eks.md | ✓ | Pending | — |
| [datadog-asm-protection-eng.md](./datadog-asm-protection-eng.md) | articles/datadog-asm-protection.md | ✓ | Pending | — |
