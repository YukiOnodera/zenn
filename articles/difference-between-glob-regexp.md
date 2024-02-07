---
title: Glob と正規表現の違い
yaml_title: difference-between-glob-regexp
created: 2023-12-26 18:53:20
updated: 2024-02-07 15:39:43
tags: 
aliases: 
emoji: 😎
published: true
published_at: 2023-12-26
topics:
  - regexp
  - glob
  - Unix
type: tech
---

# はじめに

ドキュメントを読んでいるとよく出てくる、Glob と正規表現の違いがわからなくなったので、ここで簡単に整理する。

# Glob

ファイルシステムにおいて、ファイル名を**ワイルドカード**を利用して指定するときなどに使われるパターン。

よく聞くワイルドカード (\*, ?, \[0-9\] など) とは、Glob から出てきた表現。

ワイルドカードを利用して、パターン指定ができる.

# 正規表現

Glob よりも複雑な表現ができるのが正規表現。

英語だと regular expression と呼ばれ、省略した `regexp` という表現はよく見かける。

# おわりに

この辺りはよく混同しやすいため、覚えておきたい。

# 参考

[グロブ - Wikipedia](https://ja.wikipedia.org/wiki/%E3%82%B0%E3%83%AD%E3%83%96)

[正規表現 - Wikipedia](https://ja.wikipedia.org/wiki/%E6%AD%A3%E8%A6%8F%E8%A1%A8%E7%8F%BE)
