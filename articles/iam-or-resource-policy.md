---
title: アクセス制御にはIAM Policy とResource Based Policy どちらを使うべきか
yaml_title: iam-or-resource-policy
created: 2024-01-17 17:17:23
updated: 2024-01-17 17:34:17
tags: 
aliases: 
emoji: 📝
published: true
topics:
  - AWS
  - IAM
  - S3
  - Policy
type: tech
---
# はじめに

AWS アカウント内で、一部のユーザーにのみ特定の S3 バケットに対して許可を与えたい！

S3 バケットへのアクセスを一部ユーザーにのみ制限したい！

そんな時、代表的な制御方法は 2 つあります。

それが、IAM Policy を利用する方法と Resource Based Policy (今回は S3 バケットポリシー）を利用する方法です。

どちらを使うのがいいのでしょうか？

# 結論

**迷ったら IAM Policy を利用しましょう。**

# なぜか

IAM Policy を利用することで、**Principal が持つアクセス権限を一元管理できる**ことに加えて、Resource Based Policy を使うより**ロジックがシンプルでわかりやすい**からです。

例えば、Resource Based Policy を使う場合、ユーザー毎のアクセス制御には Principal の指定、Condition の設定、Deny の利用などが必要になると思います。

普段から Principal や Condition の設定を頻繁に行っていて精通している場合は良いですが、それ以外の場合は設定の都度 Key や ARN などを調べるのが割と負担になります。

Deny を用いた制御に関しても、慎重に扱わなければなりません。

また、xxx の Condition に該当しない場合は Deny という Statement を Policy に付与した場合、その後のアクセス制御の幅が狭くなります。

なぜなら、Condition の条件として、他の Key を使った OR 条件の追加ができなくなるからです。

> AND 条件であれば問題なく可能です。また、同一 Key による値の OR も可能です。

# おわりに

ということで、基本的にアクセス制御は IAM Policy を利用するのがいいと思います。

Resource Based Policy については、全く使用しないというわけではなく、利用するタイミングとしては、その AWS サービスの**リソース固有の設定や外部アクセスの制御など**が考えられそうです。

組織の AWS ログイン方式を SSO に移行している最中なのですが、バケット周りのアクセス権限が原因で terraform apply が妨げられ、苦戦しました。

これでなんとかなりそうです。

# 参考
