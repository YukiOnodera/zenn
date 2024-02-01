---
title: Zenn x Obsidian x Github 環境で記事に画像を入れる方法
yaml_title: how-to-manage-images-with-obsidiann
created: 2024-01-30 12:59:39
updated: 2024-01-31 10:46:00
tags: 
aliases: 
emoji: 🐥
published: true
topics:
  - zenn
  - obsidian
  - github
type: tech
---

# はじめに

ここでは、**Obsidian 上で zenn の記事を執筆しつつ、記事の中で画像も取り扱いたい**という方に向けて、どのような設定をすればそれが実現できるのか、解説していこうと思います。

私の現在の環境は、zenn の記事を Obsidian 上で執筆し、Github 経由で zenn に Upload するという構成です。

この環境では、文字だけの執筆であればほとんど手を加えずに、zenn の記事を作成できますが、画像を取り扱うためには、いくつか手を加える必要があります。

> 今まで Obsidian 以外のエディタで画像の添付に苦労していた方は、Obsidian の利用を検討しつつ、ぜひ参考にしてみてください！

# 目指すところ

この記事通りに設定すると、**画像を記事にペーストするだけで、zenn に画像付きの記事を Upload できる**環境が完成します。

# 設定方法

まず、zenn の記事を管理しているリポジトリのルートを Vault として開いてください。

次に、下記のコミュニティプラグインが必要になるので、インストールしておきましょう。

- **Paste image rename**
- **Linter**

インストールと有効化を行ったら、各種設定を進めていきます。

## ファイルとリンク

まず、設定画面を開き、**ファイルとリンク**設定に移動しましょう。

いくつか項目があるので、下記の画像の通りに設定してください。

ファイル拡張子の設定はどちらでも問題ありません。

![](/images/how-to-manage-images-with-obsidiann-20240131102456.png)

## Paste Image Rename

次に、Paste image rename のプラグイン設定を行います。

Obsidian では、画像を添付したときに、自動で画像に名前がつけられます。

**デフォルトの命名のままだと画像名に空白が入ってしまい、zenn ではうまく扱えなくなってしまう**ので、そこを修正するために、このプラグインを利用します。

必須の設定内容は、

- **Auto rename 有効化**
- **Image name pattern の指定** (空白がなければお好みのもので問題なし)

私の設定はこのようになっています。

特にこだわりがなければ、Image name pattern は `{{fileName}}-{{DATE:YYYYMMDDhhmmss}}` で良いと思います。

![](/images/how-to-manage-images-with-obsidiann-20240131103047.png)

## Linter

最後に Linter の設定です。

Linter の設定画面を開き、右から 2 番目の Custom タブから、**Custom Regex Replacement** を設定します。

下記の正規表現をそれぞれの欄に入力しましょう。

- `\!\[\]\(images/`
- `gm`
- `![](/images/`

わかりずらい方は下記の画像も参考にしてください。

![](/images/how-to-manage-images-with-obsidiann-20240131103409.png)

これを行わないと、画像パスが zenn の方で認識できないままなので、この設定も必須になります。

# おわりに

設定は以上になります！

これで、**画像を記事にペーストするだけで、zenn に画像付きの記事を Upload できる**環境が完成です。
