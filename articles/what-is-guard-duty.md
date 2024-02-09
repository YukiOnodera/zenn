---
title: 検知対策サービス Amazon GuardDuty が現在提供する機能を調査
yaml_title: what-is-guard-duty
created: 2024-02-08 16:05:19
updated: 2024-02-09 09:25:22
tags: 
aliases: 
emoji: 🐷
published: true
published_at: 2024-02-12 10:00
topics:
  - AWS
  - guardduty
  - security
type: tech
---

# はじめに

Amazon GuardDuty の機能が以前調べた時よりも拡充されていたので、どういったサービスなのか改めて調査しました。

# Amazon GuardDuty とは

簡単に表現すると、AWS アカウントとワークロードに対して、脅威検知を行うことのできるサービス。

> 脅威とは、セキュリティインシデントの可能性があるアクティビティのことです。

公式サイトによると、

> Amazon GuardDuty は、AWS アカウントとワークロードを継続的にモニタリングして悪意のあるアクティビティがないかを確認し、可視化と修復のための詳細なセキュリティ検出結果を提供する脅威検出サービスです。
https://aws.amazon.com/jp/guardduty/

だそうです。

では具体的に、どういった脅威を検知することができるのか？

# GuardDuty の機能一覧

ざっとリストにすると、こんな感じになっています。

- **Default Protection**
	- **AWS** 環境での脅威検知
	- **VPC, DNS** での脅威検知
- **S3 Protection**
	- **S3**に対するアクセスとアクティビティの脅威検知
- **EKS Protection**
	- **EKS Cluster**に対する脅威検知
- **ランタイムモニタリング**
	- **ECS, EKS, EC2**リソース内での脅威検知
	- Agent 型
- **マルウェアからの保護**
	- **EBS**上でのマルウェアに対する脅威検知
	- EC2 や ECS on EC2 にアタッチされた EBS が対象
- **RDS 保護**
	- **Aurora**に対するログインアクティビティの脅威検知
- **Lambda 保護**
	- **Lambda 関数**の不正利用に対する脅威検知

## Default Protection

基本的な機能としては、下記 3 つのリソースを分析し、脅威を検知することができる機能が用意されています。

- **AWS CloudTrail 管理イベント**
    - 管理イベント (コントロールプレーンとも呼ばれる) とは、AWS アカウント内のリソースに対して実行される管理オペレーションに関する情報を提供
- **Amazon Virtual Private Cloud (Amazon VPC) フローログ**
- **DNS クエリログ**

つまりデフォルトでは、**AWS アカウント内での不審な動きの検知、VPC, DNS 関連のログを元にしたネットワーク関連の不審な動きの検知**などができるようになっています。

これらの機能に加えて他の脅威検知機能を任意で追加することができるようになっています。

![](/images/what-is-guard-duty-20240208041229.png)

これらについて、もう少し詳しく調査していきます。

## S3 プロテクション

**CloudTrail 管理イベント**と**CloudTrail S3 データイベント**を分析することにより、Amazon Simple Storage Service (Amazon S3) リソースに対する脅威を監視することが可能です。

具体的には、**S3 バケットに対するアクセスとアクティビティから、脅威を検知**することが可能となっています。

## EKS プロテクション

**EKS 監査ログ**を継続的に分析し、**セキュリティ分析に使用されるイベントのみを処理**することで、コストを削減しながら EKS Cluster に対する脅威を検知することが可能です。

> 公式サイトより
> Kubernetes 監査ログは、ユーザー、Kubernetes API を使用するアプリケーション、コントロールプレーンからのアクティビティなど、Amazon EKS クラスター内のシーケンシャルアクションをキャプチャします。
https://docs.aws.amazon.com/ja_jp/guardduty/latest/ug/features-kubernetes-protection.html#guardduty_k8s-audit-logs

## ランタイムモニタリング

監視したいリソースに対して、**GuardDuty Security Agent をデプロイし、ファイルアクセス、プロセス実行、ネットワークアクセスなどを可視化**することで、潜在的な脅威を検知可能です。

> https://docs.aws.amazon.com/ja_jp/guardduty/latest/ug/runtime-monitoring.html

対象のリソースはこちら。

- **EKS**
- **Amazon Elastic Container Service** (Amazon ECS) (AWS Fargate 上で実行されるデプロイメントを含む)
- **Amazon EC2** (プレビュー) 

## マルウェアから保護

EC2, ECS(on EC2) などにアタッチされた**EBS をスキャン**することで、**マルウェアの潜在的な存在の可能性**を検知可能です。

また、マルウェアを示す動作が検出された EC2 インスタンスまたはコンテナワークロードは、アタッチされている Amazon Elastic Block Store (Amazon EBS) ボリュームのレプリカをスキャンし、**マルウェアの可能性があるかどうかを確認**することができます。

> 
> https://docs.aws.amazon.com/ja_jp/guardduty/latest/ug/malware-protection.html

## RDS 保護

**RDS ログインアクティビティを分析してプロファイリング**し、**Amazon Aurora データベース** (Amazon Aurora MySQL 互換エディションおよび Aurora PostgreSQL 互換エディション) への潜在的なアクセス脅威がないかどうかを調べます。

この機能により、**潜在的に疑わしいログイン動作**を特定することも可能です。

RDS Protection は追加のインフラストラクチャが不要で、データベースインスタンスのパフォーマンスに影響を与えないように設計されているそうです。

## Lambda 保護

AWS Lambda 関数の実行によって生成される**ネットワークアクティビティログ**を継続的にモニタリングし、不正な暗号通貨マイニングのために悪意を持って転用された関数や、既知の脅威アクターサーバーと通信している侵害された Lambda 関数など、**Lambda に対する脅威**を検出可能にします。

# おわりに

可能であれば全部有効化したほうが良いでしょう。

一方でコストもそれなりにかかりますので、無料利用期間中にコストを試算して利用可否を判断するのが良さそうです。

https://aws.amazon.com/jp/guardduty/pricing/

# こちらもおすすめ

https://zenn.dev/yukionodera/articles/what-is-cybersecurity

https://zenn.dev/yukionodera/articles/good-about-mise

https://zenn.dev/yukionodera/articles/how-to-manage-dotfiles
