---
title: AWS の発表した SOCI とは何か
yaml_title: what-is-soci
created: 2024-01-09 17:49:36
updated: 2024-01-09 17:59:50
tags: 
aliases: 
emoji: ✨
published: true
topics: 
type: tech
---
# はじめに

SOCI がわからなかったので、改めて調べました。

# SOCI とは

AWS によって OSS 化されたテクノロジーであり、Seekable OCI の略。

> OCI が何かは明示されていませんでしたが、おそらく Open Container Initiative の略？

# 何ができるのか

SOCI という技術を利用して、SOCI インデックスを作成することでコンテナイメージの遅延読み込みを可能にし、結果としてコンテナを高速に起動することができる。

具体的には、イメージのダウンロード時に、コンテナの立ち上げに必要なレイヤーのみを先に抽出し、残りの部分はコンテナの立ち上げと並列で実行することで、起動時間を短縮している。

# おわりに

実際に使っていますが、起動時間がかなり省略できるので導入してよかったです。

> 250MB 以下のイメージにはあまり効果がないとのこと
# 参考

[詳解 : Seekable OCI を使用した AWS Fargate におけるコンテナイメージの遅延読み込み | Amazon Web Services ブログ](https://aws.amazon.com/jp/blogs/news/under-the-hood-lazy-loading-container-images-with-seekable-oci-and-aws-fargate/)

[コンテナイメージを遅延読み込みする Seekable OCI の紹介](https://aws.amazon.com/jp/about-aws/whats-new/2022/09/introducing-seekable-oci-lazy-loading-container-images/)

[Seekable OCI (SOCI) をちょっと調べた - フラミナル](https://blog.framinal.life/entry/2022/09/20/020818)

[ECS起動を高速化するSeekable OCI(SOCI)インデックスをGitHub Actionsでも作る - KAKEHASHI Tech Blog](https://kakehashi-dev.hatenablog.com/entry/2023/09/25/100000)
