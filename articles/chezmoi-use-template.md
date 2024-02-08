---
title: chezmoi 管理のdotfiles でマシン毎に設定を変えたい
yaml_title: chezmoi-use-template
created: 2023-12-17 17:03:30
updated: 2024-02-09 08:53:13
tags: 
aliases: 
emoji: 😊
published: true
published_at: 2023-12-18
topics:
  - chezmoi
  - config
  - dotfiles
type: tech
---

# はじめに

chezmoi で、マシン毎に dotfiles の設定を変える方法についてまとめます。

# 問題

chezmoi では、リポジトリを利用して dotfiles の管理を行うことで、マシン間での dotfiles の共有が簡単にできます。

しかし、基本的な使い方では、マシン毎で生じる設定の差分を埋めることができません。

# 解決方法

chezmoi の template 機能を使えば、その問題は解決できます。

まず、template ファイルを作成します。

```
# 新しくファイルを追加する場合
chezmoi add --template ~/.ssh/config

# 既存ファイルをtemplate にする場合
chezmoi chattr +template ~/.ssh/config
```

次に、template ファイルを修正します。

chezmoi 環境で template ファイルを修正することが可能です。

```
# chezmoi 環境に移動
chezmoi cd

# template ファイル名を確認
git status

# template ファイルを編集(お好みのエディタで)
code private_dot_ssh/config.tmpl
```

template ファイル内では様々なロジックが利用できますが、簡単なのは if 文です。

[Templating - chezmoi](https://www.chezmoi.io/user-guide/templating/#introduction) に詳細な説明があるので、参考にしてみてください。

```
{{ if eq .chezmoi.os "darwin" }}
# darwin
{{ else if eq .chezmoi.os "linux" }}
# linux
{{ else }}
# other operating system
{{ end }}
```

条件分岐に利用できる値は、data コマンドで確認できます。

```
chezmoi data
```

自分は下記の条件で、各マシンの設定を記載していました。

```
{{ if eq .chezmoi.hostname "Private PC" -}}
# Private PC contents
{{ else -}}
# Else contents
{{ end -}}
```

template ファイルの修正が完了したら、正しく設定されているかテストしましょう。

```
chezmoi execute-template < private_dot_ssh/config.tmpl
```

問題なければ、リモートリポジトリに apply して完了です。

# おわりに

簡単に chezmoi でマシン毎に設定を切り替えることができるようになりました。

chezmoi はまだまだ色々応用が効きそうなので、必要になり次第色々調べてみます。

# 参考

[Templating - chezmoi](https://www.chezmoi.io/user-guide/templating/#introduction)
