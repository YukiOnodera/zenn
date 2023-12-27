---
title: bundle install で発生する mysql2 のインストールエラー対処法
yaml_title: how-to-fix-error-mysql2
created: 2023-12-27 16:24:24
updated: 2023-12-27 16:42:29
tags: 
aliases: 
emoji: 👋
published: true
published_at: 2023-12-28
topics:
  - Rails
  - mysql2
  - bundle
type: tech
---
# はじめに

`bundle install` 実行時に、mysql2 のインストールに失敗しました。

# 問題

色々な例があると思いますが、自分の場合は zstd の Path がうまく通っておらず、下記のエラーが出ていました。

```sh
...
ld: library 'zstd' not found
...
```

# 解決方法

下記を実行することで、成功しました。

```sh
export LIBRARY_PATH=$LIBRARY_PATH:$(brew --prefix zstd)/lib/
```

今後同様のエラーが発生しないように、`~/.zshrc` に追記しておくのがおすすめです。

## LIBRARY_PATH とは

Unix 系のオペレーティングシステム（Linux や macOS など）において、コンパイラが共有ライブラリを探すために参照する環境変数のこと。

## Zstd とは

可逆式圧縮を可能とするライブラリ。

# おわりに

`mysql2` 関連エラーはデバッグに時間がかかって大変です。

# 参考

[bundle install fails with Gem::Ext::BuildError · Issue #1175 · brianmario/mysql2 · GitHub](https://github.com/brianmario/mysql2/issues/1175)

[【Rails】mysql2のインストールができない場合の対処法【MySQL】 #Rails - Qiita](https://qiita.com/P-man_Brown/items/bb525958f361af39a472)

[[Rails]初のbundle installでmysql2のエラーが出た時の解決策をまとめてみた #Rails - Qiita](https://qiita.com/Hiron0120/items/1a381d7845e208d35f61)

[Zstandard - Wikipedia](https://ja.wikipedia.org/wiki/Zstandard)
