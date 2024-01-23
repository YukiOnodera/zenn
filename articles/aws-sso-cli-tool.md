---
title: AWS SSO CLI という有能ツールのすヽめ
yaml_title: aws-sso-cli-tool
created: 2024-01-23 11:08:07
updated: 2024-01-23 12:00:42
tags: 
aliases: 
emoji: 🙌
published: true
published_at: 2024-01-23 11:00
topics:
  - AWS
  - SSO
  - IdentityStore
  - CLI
type: tech
---
# はじめに

普段 AWS へログインするときに SSO ログインをしていて、AWS CLI も SSO 経由で利用している方必見のツールがあります。

それがこちらです！

https://synfinatic.github.io/aws-sso-cli/

AWS SSO CLI という、そのまんまの名前をしたツールになります。

なぜこれが必見かというと、

- ローカルに配置される**認証情報が暗号化**される
	- aws-vault と同じパッケージを利用している
- `aws sso login` コマンドを**実行しなくても良い**
	- 認証が必要になったら、aws コマンド実行時に勝手にログイン認証を進めてくれる
- `$HOME/.aws/config` を**動的に管理**できる

今回は、このツールの導入方法、使い方、おすすめの設定などを紹介します。

# Install

まずは Tool をインストールしましょう。

[Installation](https://synfinatic.github.io/aws-sso-cli/quickstart/#installation)

Brew での Install がおすすめです。

```sh
brew install aws-sso-cli
```

# Setup

次に初期設定となります。

[Guided Configuration](https://synfinatic.github.io/aws-sso-cli/quickstart/#guided-configuration)

```sh
aws-sso config
```

設定するためのウィザードが出るので、指示に従って進めましょう。

# Auto Completion

お好みで補完機能も設定できるので、欲しい人はやっておきましょう。

[Enabling auto-completion in your shell](https://synfinatic.github.io/aws-sso-cli/quickstart/#enabling-auto-completion-in-your-shell)

# 使い方

メインでよく使うのは２つとなります。

```sh
aws-sso list
```

AWS のアカウントや Profile 一覧を見ることができます。

```sh
aws-sso config-profiles
```

`$HOME/.aws/config` を Update したい場合はこちらのコマンドで Update が可能です。

# おすすめの設定

ウィザードを実施すると、`$HOME/.aws-sso/config.yaml` に設定ファイルが作成されます。

デフォルトの設定に加えて、下記の設定を追加すると使いやすくなるのでおすすめです。

```config.yaml
ConfigVariables:
  output: json
ListFields:
- AccountIdPad
- AccountName
- AccountAlias
- RoleName
- Profile
AutoConfigCheck: true
```

## 設定値の詳細
- ConfigVariables
	- Profile に追加する設定をここで指定できる
- ListFields
	- `aws-sso list` コマンドで表示されるカラムの指定
- AutoConfigCheck
	- 定期的に SSO の権限に更新があったかチェックしてくれる機能
# おわりに

これで SSO による煩わしい作業が多少軽減されるのではないでしょうか？

AWS のログインに SSO を利用している方はぜひ導入しましょう。

# 参考

https://synfinatic.github.io/aws-sso-cli/
