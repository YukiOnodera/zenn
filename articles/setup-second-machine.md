---
title: chezmoi を サブマシンにも導入する
yaml_title: setup-second-machine
created: 2023-12-17 15:14:53
updated: 2023-12-17 15:52:57
tags: 
aliases: 
emoji: ✨
published: true
topics:
  - chezmoi
  - dotfiles
  - config
type: tech
---
# はじめに

chezmoi で管理している dotfiles をサブマシンでセットアップするときの手順を整理していきます。

# Setup

chezmoi をインストール後、下記のコマンドで chezmoi 環境を init します。

この時点では、dotfiles がローカルマシンに適用されることはありません。

```shell
# Https接続
chezmoi init https://github.com/$GITHUB_USERNAME/dotfiles.git

# SSH接続
chezmoi init git@github.com:$GITHUB_USERNAME/dotfiles.git
```

次に、ローカル環境と chezmoi 環境の差分を確認します。

```
chezmoi diff
```

ここで全てのファイルに問題がなければ、apply しましょう。

```
chezmoi apply -v
```

自分の場合は、仕事用 PC の環境をプライベートに持ってくる形だったので、ここでかなりの修正が必要であることがわかりました。

まず、問題がないファイルだけを、先に apply しましょう。 

下記のように、ファイルごとの適用が可能です。

```
 chezmoi apply ~/.bashrc
```

修正が必要なファイルについては、edit コマンドで個別のファイルを修正しましょう。

```
chezmoi edit $FILE
```

merge コマンドを利用しても良いです。 

デフォルトでは vimdiff を使った merge 作業画面に入ります。

自分は慣れなかったので、基本 edit コマンドで作業してました。

```
chezmoi merge $FILE
```

修正が完了したら、apply コマンドでローカル環境への適用を行なってください。

また、[リモートリポジトリへの適用](https://zenn.dev/yukionodera/articles/how-to-manage-dotfiles#dotfiles-%E3%82%92-git-push-%E3%81%97%E3%81%9F%E3%81%84%E6%99%82) も忘れないようにしましょう。

メインマシンなどでリモートリポジトリの最新の状況を反映するには、update コマンドを実行します。

```
chezmoi update -v
```

# おわりに

これでサブマシンのセットアップができるようになりました。

一度慣れてしまえばそんなに手こずらないと思います。

今回は割愛しましたが、マシン毎に適用する設定を切り替えることもできるので、別のタイミングでまとめておきます。

**Have a happly chezmoi life!**

# 参考

[chezmoi を使った dotfiles の管理方法](https://zenn.dev/yukionodera/articles/how-to-manage-dotfiles#dotfiles-%E3%82%92-git-push-%E3%81%97%E3%81%9F%E3%81%84%E6%99%82)

[chezmoi - chezmoi](https://www.chezmoi.io/)
