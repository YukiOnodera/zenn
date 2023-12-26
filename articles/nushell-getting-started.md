---
title: 最近話題の Nushell の Quick Tour やってみた
yaml_title: nushell-getting-started
created: 2023-12-26 12:13:15
updated: 2023-12-26 18:28:19
tags: 
aliases: 
emoji: 🙌
published: true
published_at: 2023-12-27
topics:
  - Nushell
  - zsh
  - shell
type: tech
---
# はじめに

Nushell というシェルが気になっていたので、[Quick Tour | Nushell](https://www.nushell.sh/book/quick_tour.html#quick-tour) をやってみました。

# 事前準備
## Installing Nu

まずは Nu の Install です。

Nu の Install 方法はニーズに合わせて様々な方法が用意されています。

[Installing Nu | Nushell](https://www.nushell.sh/book/installation.html#installing-nu)

自分は brew でインストールしました。

`nu` を実行すると、Nushell が起動できます。

```shell
nu
     __  ,
 .--()°'.' Welcome to Nushell,
'|, . ,'   based on the nu language,
 !_-(_\    where all data is structured!

Please join our Discord community at https://discord.gg/NtAbbGn
Our GitHub repository is at https://github.com/nushell/nushell
Our Documentation is located at https://nushell.sh
Tweet us at @nu_shell
Learn how to remove this at: https://nushell.sh/book/configuration.html#remove-welcome-message

It's been this long since Nushell's first commit:
4yrs 7months 15days 10hrs 18mins 41secs 820ms 792µs

Startup Time: 57ms 55µs 875ns

~>                                                                                                                     12/26/23 12:17:53 PM
```

## Default Shell

次に、Nushell を Default shell にする方法の紹介です。

[Default shell | Nushell](https://www.nushell.sh/book/default_shell.html)

今回は Nushell の検証なので、ここは飛ばしました。

# Quick Tour

ここからが本題です。

詳細は公式サイトに載っているので、ここでは重要なところを掻い摘んで紹介していこうと思います。

まず、Nushell には**様々なビルトインコマンドが用意されていて**、例えば `ls` コマンドの結果も、zsh などと異なるものとなっています。

また、コマンドの前に `^` をつけて `^ls` のようにすると、Nu の外部コマンドを実行できるようになっています。

```shell
> ls
╭────┬───────────────────────┬──────┬───────────┬─────────────╮
│ #  │         name          │ type │   size    │  modified   │
├────┼───────────────────────┼──────┼───────────┼─────────────┤
│  0 │ 404.html              │ file │     429 B │ 3 days ago  │
│  1 │ CONTRIBUTING.md       │ file │     955 B │ 8 mins ago  │
│  2 │ Gemfile               │ file │   1.1 KiB │ 3 days ago  │
│  3 │ Gemfile.lock          │ file │   6.9 KiB │ 3 days ago  │
│  4 │ LICENSE               │ file │   1.1 KiB │ 3 days ago  │
│  5 │ README.md             │ file │     213 B │ 3 days ago  │
...

```
```shell
~> ^ls                                                                                                                 12/26/23 12:39:00 PM
Applications		Desktop			Library			Pictures		repositories ...
```

そして、Nu はビルトインコマンドで出力されるような**テーブルの扱いを簡単にするコマンド**がいくつか用意されています。

これが Nu の一つの特徴でもあります。

sort-by, reverse, where などの使用例。

```shell
> ls | sort-by size | reverse
╭────┬───────────────────────┬──────┬───────────┬─────────────╮
│ #  │         name          │ type │   size    │  modified   │
├────┼───────────────────────┼──────┼───────────┼─────────────┤
│  0 │ Gemfile.lock          │ file │   6.9 KiB │ 3 days ago  │
│  1 │ SUMMARY.md            │ file │   3.7 KiB │ 3 days ago  │
│  2 │ Gemfile               │ file │   1.1 KiB │ 3 days ago  │
│  3 │ LICENSE               │ file │   1.1 KiB │ 3 days ago  │
│  4 │ CONTRIBUTING.md       │ file │     955 B │ 9 mins ago  │
│  5 │ books.md              │ file │     687 B │ 3 days ago  │
...
```

```shell
> ls | where size > 1kb
╭───┬───────────────────┬──────┬─────────┬────────────╮
│ # │       name        │ type │  size   │  modified  │
├───┼───────────────────┼──────┼─────────┼────────────┤
│ 0 │ Gemfile           │ file │ 1.1 KiB │ 3 days ago │
│ 1 │ Gemfile.lock      │ file │ 6.9 KiB │ 3 days ago │
│ 2 │ LICENSE           │ file │ 1.1 KiB │ 3 days ago │
│ 3 │ SUMMARY.md        │ file │ 3.7 KiB │ 3 days ago │
╰───┴───────────────────┴──────┴─────────┴────────────╯
```

また、`get` コマンドを使うことで、Column 内の Contents をさらに深く探索することも可能です。

```shell
> sys
╭───────┬───────────────────╮
│ host  │ {record 6 fields} │
│ cpu   │ [table 4 rows]    │
│ disks │ [table 3 rows]    │
│ mem   │ {record 4 fields} │
│ temp  │ [table 1 row]     │
│ net   │ [table 4 rows]    │
╰───────┴───────────────────╯
```
```shell
> sys | get host
╭────────────────┬────────────────────────╮
│ name           │ Debian GNU/Linux       │
│ os version     │ 11                     │
│ kernel version │ 5.10.92-v8+            │
│ hostname       │ lifeless               │
│ uptime         │ 19day 21hr 34min 45sec │
│ sessions       │ [table 1 row]          │
╰────────────────┴────────────────────────╯
```

`each` コマンドを使って、`xargs` のようなことも直観的にできるようになっています。

```shell
> sys | get host.sessions.name | each { |it| ^echo $it }
jt
```

また、ここまで出てきた Nushell のビルトインコマンドは、`help COMMANDS` の形でガイドを参照することができるようになっていました。

以上で Quick Tour は終わりです。

# おわりに

Quck Tour をやってみた感想としては、zsh などよりも**デフォルトで得られる情報量が多い**点、**出力されたテーブルを直観的に操作できる**点が特徴的だなと思いました。

また、データがテーブルとして綺麗に整形されて出力されるので、**実行結果が見やすい**点は非常に魅力的でした。

まだデフォルトシェルにするには心許ないので、引き続きドキュメントを見ながら色々と検証してみようと思います。

# 参考

[Quick Tour | Nushell](https://www.nushell.sh/book/quick_tour.html)
