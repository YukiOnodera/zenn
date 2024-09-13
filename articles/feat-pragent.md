---
title: PR-Agent というAIツールを導入してみた
yaml_title: feat-pragent
created: 2024-09-13 17:41:21
updated: 2024-09-13 17:54:59
tags: 
aliases: 
emoji: 📘
published: true
published_at: 2024-09-24 09:00
topics:
  - Github
  - AI
  - Productivity
type: tech
---
# はじめに

 Review 周りの効率化のために、PR-Agent と言う新たな AI ツールを導入しました。ここではその機能の概要や有効化した機能、設定等について解説していきます。

## 1. PR-Agent の概要

### PR-Agent とは何か

PR-Agent は、GitHub でのプルリクエスト（PR）やレビュー作業を効率化するための AI ツールの一つです。このツールは、PR のタイトルや説明を自動生成し、コードレビューや改善提案も行うことができます。

https://pr-agent-docs.codium.ai/

### 導入の背景と目的

PR-Agent 導入の背景には、プルリクエストの作成やレビューに対する個人的な手間や、チーム内での運用課題がありました。

具体的には、修正の規模に応じたレビューの必要性や、誰がレビューを行うべきかの不透明さ、技術的な習熟度の違いによるレビュー品質のばらつきが問題となっていました。

これらの課題を解決するために、以下の記事を参考にして PR-Agent の導入を検討しました。

https://tech.layerx.co.jp/entry/2023/09/01/102612

https://engineering.mercari.com/blog/entry/20231223-mercoin-github-actions/

導入の目的は、**PR 作成を効率化することと、チーム内でのレビューの仕組みを改善し、技術的な習熟度の差によるレビューのばらつきを解消**することです。

## 2. PR-Agent の主要機能

PR-Agent には主に以下の 3 つの機能があります。

1. **Describe**: プルリクエストの概要やタイトルを自動で作成します。
2. **Review**: コードのレビューを自動で行い、問題点を指摘します。
3. **Improve**: 改善点を提案し、コードの修正を支援します。

## 3. インフラ SRE チームでの導入プロセス

### 導入の決定から実施までの流れ

導入の決定に至るまで、自分が機能を検証し、導入を決定しました。現在は試験的に導入していますが、チーム内の反応を見ながら横展開する予定です。

## 4. 有効化した機能

ここでは、有効化した具体的な機能について、具体的な設定ファイルを基に説明します。

### .github/workflows/pr_agent.yml

```toml
on:
  pull_request:
    types: [opened, reopened, ready_for_review]
  issue_comment:
jobs:
  pr_agent_job:
    if: ${{ github.event.sender.type != 'Bot' }}
    runs-on: ubuntu-latest
    permissions:
      issues: write
      pull-requests: write
      contents: write
    name: Run pr agent on every pull request, respond to user comments
    steps:
    - name: PR Agent action step
      id: pragent
      uses: Codium-ai/pr-agent@main
      env:
        OPENAI_KEY: ${{ secrets.OPENAI_KEY }}
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        github_action_config.auto_review: "true" # enable\disable auto review
        github_action_config.auto_describe: "true" # enable\disable auto describe
        github_action_config.auto_improve: "true" # enable\disable auto improve
```

このファイルは、PR エージェントを実行するためのワークフローを定義しています。ワークフローのトリガーは、PR が作成された場合や、PR にコメントが投稿された場合です。ワークフローが実行されると、以下の 3 つの機能が自動で実行されるよう設定されています。

1. **Describe (自動説明)**
2. **Review (自動レビュー)**
3. **Improve (自動改善)**

### .pr_agent.toml

```toml
# https://pr-agent-docs.codium.ai/
# https://github.com/Codium-ai/pr-agent/blob/main/pr_agent/settings/configuration.toml

[config]
ignore_pr_labels = ['renovate']

[ignore]
glob = ['*.lock.hcl','*.sops.yaml','*.toml']

[pr_description]
generate_ai_title = true
final_update_message = true
extra_instructions="""\
Emphasize the following:
- Please use Japanese for everything.
- Titles should have a prefix following the commitlint pattern, such as feat:, chore:, test:, fix:, docs:, style:, refactor:, perf:, etc.
"""

[pr_reviewer]
require_tests_review = false
require_can_be_split_review	= true
num_code_suggestions = 3
inline_code_comments = true
enable_auto_approval = true
maximal_review_effort = 3
extra_instructions="""\
Emphasize the following:
- Please use Japanese for everything.
"""

[pr_code_suggestions]
num_code_suggestions = 3
rank_suggestions = true
commitable_code_suggestions = true
demand_code_suggestions_self_review = true
extra_instructions="""\
Emphasize the following:
- Please use Japanese for everything.
"""

```

こちらは、PR エージェントの詳細な設定ファイルです。このファイルで、各機能の動作条件や挙動を細かく設定しています。

### **[Config] セクション**

まず、`ignore_pr_labels` 設定により、特定のラベル（例：'renovate'）が付いている PR に対してはエージェントを動作させないようにしています。例えば、`Renovate` が自動生成する PR については、エージェントの処理を無視する設定となっています。また、`ignore` セクションでは、エージェントを動作させないファイルパターン（例：`*.lock.hcl`、`*.sops.yaml`、`*.toml`）を指定しています。

### **[PR Description] セクション**

ここでは、PR のタイトルを自動生成する設定や、ディスクリプションが完了した際に追加コメントを投稿する設定を行っています。さらに、日本語で記載するよう指定し、タイトルにはコミットリントパターンに従ったプレフィックス（`feat:`、`chore:`、`test:` など）を付ける指示を追加しています。

![](/images/feat-pragent-20240913054815.png)

### **[PR Reviewer] セクション**

レビュー機能に関する設定では、まず全て日本語で記載するよう指示しています。さらに、PR が 5 段階評価で「3」以下であれば、自動的に承認する機能を有効化しています。評価が「4」以上の場合、エージェントによる自動承認は行われず、別のレビュアーによる確認が必要となります。この評価はプルリクエストのレビューに要するとされる労力をもとに設定されています。

また、レビューによって指摘された改善点をコード内にコメントする機能や、PR が大きすぎる場合に分割の提案を行う機能も有効化しています。コード改善の提案は最大 3 件までに制限しています。

![](/images/feat-pragent-20240913054802.png)

### **[PR Code Suggestions] セクション**

最後に、コード改善提案に関する設定です。こちらでも、全て日本語で記載するよう指定し、コード改善の提案数は 3 件までとしています。この機能は現在、試験的に運用しており、具体的な活用方法を模索しています。

![](/images/feat-pragent-20240913054750.png)

## 5. PR-Agent の使用方法

### 基本的な操作手順

PR-Agent の操作方法には、以下の 2 種類があります。

1. プルリクエストを作成した際に自動的に実行される方法
2. プルリクエストのコメント欄に特定のコマンドを入力して実行する方法

    コメントを入力するだけで簡単に操作できるため、ぜひ使ってみてください。例えば、プルリクエストの内容が大きく変更された場合、「Describe」機能を使用して PR のタイトルや説明を再作成することができます。また、「Review」や「Improve」機能を使って、コードの改善点や脆弱性を発見することも可能です。

### 困った時は

`/help` とコメントすると、使い方を教えてくれます。

![](/images/feat-pragent-20240913054702.png)

![](/images/feat-pragent-20240913054649.png)

### Chrome 拡張機能

Chrome の拡張機能を追加すると、PR-Agent のマニュアルでの実行がさらに便利になるのでおすすめです。

![](/images/feat-pragent-20240913054620.png)

[PR-Agent: AI-Powered Code Reviews & Chat - Chrome Web Store](https://chromewebstore.google.com/detail/pr-agent-ai-powered-code/ephlnjeghhogofkifjloamocljapahnl?hl=en)

## 6. PR-Agent の設定

### 初期設定の手順

初期設定の手順は以下の通りです。

1. OpenAI トークンの発行
2. GitHub Actions のワークフローを追加
3. PR-Agent の設定ファイルを追加
4. OpenAI トークンをシークレットとして GitHub Actions に追加

### カスタマイズ可能な項目

PR-Agent は GitHub Actions 以外にも様々な方法で実行可能です。今回は最も簡単で、利用用途に合った GitHub Actions を使用しています。

# こちらもおすすめ

https://zenn.dev/yukionodera/articles/good-about-mise

https://zenn.dev/yukionodera/articles/datadog-asm-protection

https://zenn.dev/yukionodera/articles/how-to-manage-images-with-obsidiann

# おわりに

ものすごく便利ですが、その分コストもかかります。

ただ、新しい人材を一人雇うよりからはかなり安上がりなので、検討の余地は十分あると思います。
