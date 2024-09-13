---
title: "IaC の品質も自動で管理する時代: pre-commit と静的解析ツールの導入のススメ"
yaml_title: infra-iac-ci
created: 2024-09-06 16:45:05
updated: 2024-09-13 17:41:32
tags: 
aliases: 
emoji: 🐷
published: true
published_at: 2024-09-17 09:00
topics:
  - Terraform
  - github
  - security
type: tech
---
# はじめに

インフラストラクチャコード（IaC）の品質が、**作成者によって大きくバラついてしまう**ことがありませんか？

手作業に頼らずに、IaC（主に Terraform）の品質を自動的に保証する方法があれば、ミスを減らし、より一貫したコード品質を保てるでしょう。

そこで今回は、**pre-commit** を利用して複数の静的解析ツールを自動で実行し、コードの品質やセキュリティの脆弱性をチェックする仕組みを紹介します。

https://pre-commit.com/

この仕組みにより、コミット時に問題が検出されるとコミットが失敗するため、一定の品質が保証されます。

この記事では、導入した仕組みの詳細について説明します。

# 使用したツール一覧

今回の導入で使用したツールは以下の通りです.

- **pre-commit** - コードのコミット時にフックを設定して自動的に解析を実行。
- **OpenTofu** - Terraform と互換性あり、主に OpenTofu ベースの環境で利用。
- **TFLint** - Terraform 用の Linter で構成やベストプラクティスのチェックを実行。
- **Checkov** - IaC のセキュリティスキャンを行う静的解析ツール。
- **terraform-docs** - Terraform のドキュメントを自動生成。

:::message

なお、この記事では OpenTofu を使用していますが、Terraform 環境でも同様の設定が可能です。Terraform を利用している場合は、"tofu" を "terraform" と読み替えてください。

:::

# Pre-commit の導入手順

## 1. 設定ファイルの作成

まずは、pre-commit の設定ファイルを作成します。以下が設定の例です。

```yaml
repos:
- repo: https://github.com/tofuutils/pre-commit-opentofu
  rev: v1.0.2 # Get the latest from: https://github.com/tofuutils/pre-commit-opentofu/releases
  hooks:
  - id: tofu_fmt
  - id: tofu_validate
  - id: tofu_tflint
  - id: tofu_checkov
    args:
    - --args=--config-file __GIT_WORKING_DIR__/.checkov.yaml
  - id: tofu_docs
    args:
    - --hook-config=--path-to-file=README.md
    - --hook-config=--add-to-existing-file=true
    - --hook-config=--create-file-if-not-exist=true
```

## 2. 各ツールのフックの詳細

設定ファイルで指定した各フックについて説明します。

- **tofu_fmt**  
    `tofu fmt` コマンドを実行し、Terraform ファイルのフォーマットを整えます。
    
- **tofu_validate**  
    `tofu validate` コマンドで構文エラーがないかをチェックします。
    
- **tofu_tflint**  
    `tflint` を実行して、構文の検証だけでなく、設定値の問題もチェックします。
    
- **tofu_checkov**  
    Checkov を利用して、セキュリティの脆弱性をスキャンします。Checkov に関する詳細は下記をご参照ください
	- https://zenn.dev/articles/feat-checkov
	    
- **tofu_docs**  
    Terraform ファイルを解析し、リソースに関するドキュメント（README.md）を自動生成します。

> terraform の場合はこちら
> https://github.com/antonbabenko/pre-commit-terraform

## 3. Pre-commit のインストール

次に、pre-commit をインストールして設定を反映させます。

```shell
brew install pre-commit checkov tflint terraform-docs jq
pre-commit install
```

# こちらもおすすめ

https://zenn.dev/yukionodera/articles/good-about-mise

https://zenn.dev/yukionodera/articles/datadog-asm-protection

https://zenn.dev/yukionodera/articles/how-to-manage-images-with-obsidiann

# おわりに

pre-commit と静的解析ツールを導入することで、IaC に関する品質を自動的にチェックし、リスクを最小限に抑えることが可能です。これにより、コードの一貫性を保ち、セキュリティやコンプライアンスの強化にもつながります。

今後も、この仕組みを活用して、より高品質な IaC コードを管理していきましょう!
