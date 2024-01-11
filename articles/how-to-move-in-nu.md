---
title: Nushell でのファイルシステムの歩き方
yaml_title: how-to-move-in-nu
created: 2024-01-09 12:42:02
updated: 2024-01-11 17:05:55
tags: 
aliases: 
emoji: 🐡
published: true
topics:
  - Nushell
  - Nu
  - zsh
  - shell
type: tech
---
# はじめに

今回は、[Moving around your system | Nushell](https://www.nushell.sh/book/moving_around.html) を通して、Nushell 内での動き方を実践してみます。

# Viewing Directory Contents & Glob Patterns (wildcards)

ディレクトリの中身を見るには、他のシェルと変わらず `ls` コマンドを使用します。

Nu だと wild card を利用することができるようです。

```nu
~> ls P*                                                                   
╭───┬──────────┬──────┬───────┬──────────────╮
│ # │   name   │ type │ size  │   modified   │
├───┼──────────┼──────┼───────┼──────────────┤
│ 0 │ Pictures │ dir  │ 128 B │ 2 months ago │
│ 1 │ Public   │ dir  │ 128 B │ 3 months ago │
╰───┴──────────┴──────┴───────┴──────────────╯
```

ネストも可能でした。

```nu
~> ls t*/*.md                                                              
╭───┬──────────────┬──────┬──────┬────────────────╮
│ # │     name     │ type │ size │    modified    │
├───┼──────────────┼──────┼──────┼────────────────┤
│ 0 │ test/test.md │ file │  0 B │ 25 seconds ago │
╰───┴──────────────┴──────┴──────┴────────────────╯
```

しかしこちらに関しては、zsh などでも同じようなことができました。

```zsh
> ls t*/*.md
test/test.md
```
## Changing the Current Directory

ディレクトリ移動も、他のシェルと変わらず `cd` コマンドで移動できます。

```nu
~> cd test/
~/test>
```

しかし Nu では、cd コマンドなしでもディレクトリ移動が可能になっていました。

```nu
~> ./test/
~/test> 
```

これは他のシェルにはない機能ですね。

## Filesystem Commands

`mv`, `cp`, `rm`, `mkdir` コマンドあたりも他のシェルと同様に使えるようです。

こちらも Nu 特有の使い方というのは見受けられませんでしたが、`mv`, `cp` コマンドなどで移動先を指定するときに出てくる補完機能がかなり使いやすかったです。

ネイティブで入っているのもいいですね。

# おわりに

今回の章は割と短かったので、さらっと Nu について学習できてよかったです。

ここまで使っていていいなと思ったポイントは、Plugin などを追加しなくても補完機能やシェルの UI が綺麗に整備されているとこでした。

そういった意味では、意外と初心者向けのシェルでもあるのかもしれないなと思った次第です。

# 参考

[Moving around your system | Nushell](https://www.nushell.sh/book/moving_around.html)
