---
title: IAM Identity Store で外部IdP を利用しつつグループを作成する方法
yaml_title: how-to-manage-identitystore-group
created: 2024-01-09 18:01:37
updated: 2024-01-09 18:21:44
tags: 
aliases: 
emoji: 👌
published: true
published_at: 2024-01-10 11:00
topics:
  - AWS
  - SSO
  - IAM
type: tech
---
# はじめに

Google Workspace と IAM Identity Store を連携させた環境で、グループの作成がうまくできなかったので、作成方法を調べました。

# 問題

AWS のマネジメントコンソールからグループを作成しようとした際、下記のようなメッセージが出ており、グループが作成できませんでした。

> ID ソースは現在「外部 ID プロバイダー」として設定されています。新しいグループを追加したり、メンバーシップを編集したりするには、外部 ID プロバイダーを使用してこれを行う必要があります。

確かに ID source は Google Workspace を利用しているので、外部 ID プロバイダーを利用していることになります。

しかし、Google Workspace 側の権限は持っていないので、新しいグループの追加などは難しい状況です。

いろいろ調べていたら、解決法が見つかりました。

# 解決方法

実は、外部 ID プロバイダー側でグループを整備しなくても、AWS CLI や API を使えばグループの作成が可能となっていました。

こちら [Google Workspace - AWS IAM Identity Center](https://docs.aws.amazon.com/ja_jp/singlesignon/latest/userguide/google-idp.html) に記載があります。

> SCIM による Google Workspace グループの自動プロビジョニングは利用できません。グループは次のように手動で作成できます。

コンソールで表示された日本語の文言を勘違いしており、公式ドキュメント読み漁るまで気づきませんでした。

# おわりに

AWS って日本語訳怪しいことよくありますよね。ドキュメント大事。

Terraform でもリソースが用意されていたので、自分は IaC で作っていく予定です。

# 参考

[Google Workspace - AWS IAM Identity Center](https://docs.aws.amazon.com/ja_jp/singlesignon/latest/userguide/google-idp.html)

[Terraform Registry](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/identitystore_group)
