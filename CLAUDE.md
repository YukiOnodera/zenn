# Zenn ブログリポジトリ

## 概要

[Zenn](https://zenn.dev) に投稿するための技術ブログリポジトリ。zenn-cli を使って管理している。

## 記事の作成

```shell
# 新しい記事を作成
npx zenn new:article --slug 記事のスラッグ --type tech --emoji 🔖

# プレビュー
npx zenn preview
```

## 記事フォーマット

`articles/` 配下に Markdown ファイルを置く。フロントマターの形式：

```yaml
---
title: 記事タイトル
emoji: 🔖
type: tech        # tech or idea
topics:
  - トピック1
  - トピック2
published: true   # false にすると下書き
---
```

## 執筆スタイル

- 日本語で書く
- 読者は日本語話者のエンジニア
- 技術的に正確で実践的な内容を重視する
- コマンドやコードは必ずコードブロックで示す
- 見出しは `#`（h1）から始め、階層を整える
- 「はじめに」で背景・目的を説明し、「まとめ」で要点を締める構成が多い

## 重要なルール

- `articles/` 内の Markdown ファイルのみ編集対象
- `package.json` や `package-lock.json` は記事追加では変更しない
- 認証情報・APIキー・個人情報は絶対にファイルに書かない
