---
title: DevSecOps実装のためのCICDセキュリティチェックリスト
yaml_title: cicd-devsecops
created: 2024-03-15 16:11:37
updated: 2024-03-15 16:29:54
tags: 
aliases: 
emoji: 💭
published: true
topics:
  - devops
  - DevSecOps
  - cicd
type: tech
---

# はじめに

CICD 関連ツールが多すぎてちょっと整理したくなったので、**DevSecOps** を実践する場合にどんな対策が必要なのかまとめてみました。

**CICD を自動化しつつ、最低限の Security も担保しておきたい**方は、さらっと確認して抜け漏れがないかみてもらえるといいと思います。

## CICD の工程について

巷で有名な話題の図によると、DevOps のフローの中で関連度が高いのは下記の 5 つです。

- **CODE**
- **BUILD**
- **TEST**
- **RELEASE**
- **DEPLOY**

DevSecOps を実践する場合、**これらの各工程でどのような自動化ツールが使えるのか**をまとめてみました。

## CODE

- Secrets Check
	- 機密情報のハードコード防止
- Formatter
	- コードを綺麗に整形
- Linter
	- コードを静的に解析
	- 構文エラーなどを検知
- SCA
	- 依存ライブラリをチェック
	- dependabot, renovate などは自動で Update の PR 作成してくれる
- インフラコードの脆弱性検出
	- IaC の静的な解析ツール

## BUILD

- SAST
	- 静的なアプリケーションセキュリティテスト
- コンテナイメージの脆弱性検出
	- ビルドしたコンテナイメージに入っている package の脆弱性などを検出

## TEST

- 単体テスト
- 結合テスト
- E2E テスト
- 負荷テスト
- DAST
	- 動的なアプリケーションセキュリティテスト
- IAST
	- インタラクティブなアプリケーションセキュリティテスト
	- Agent を Application にいれて、ホスト側と通信を行いながらセキュリティテストを実行
	- ちょっとお高い
- Etc...
	- Security と同じで、Test は DevOps の各工程で実践可能なさまざまなテストが存在するので、お好みで入れましょう

## RELEASE

- Penetration テスト
	- アプリケーションに対する全体的なセキュリティテスト
	- かなりお高い

## DEPLOY

- アプリケーションのデプロイ
- インフラのプロビジョニング

# こちらもおすすめ

https://zenn.dev/yukionodera/articles/good-about-mise

https://zenn.dev/yukionodera/articles/arc-2-released

https://zenn.dev/yukionodera/articles/how-to-manage-images-with-obsidiann

# おわりに

やることいっぱいありますよね。

Security はやろうと思えば**際限のない領域**だと思うので、コストと相談しつつ導入していくといいと思います。

DevOps の各工程で目的に応じた Security 対策ができている場合は、DevSecOps として安定した環境を提供といっても過言ではないでしょう。
