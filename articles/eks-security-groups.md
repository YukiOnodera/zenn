---
title: EKS 関連の Security Group についてまとめました
yaml_title: eks-security-groups
created: 2023-12-22 18:30:47
updated: 2024-02-09 08:53:18
tags: 
aliases: 
emoji: 📝
published: true
published_at: 2023-12-25
topics:
  - AWS
  - EKS
  - Kubernetes
type: tech
---

# はじめに

EKS 関連の Security Group は複数存在しており、しっかりと理解していないと運用にも苦戦するなと思ったので、まとめました。

# EKS 関連の Security Group

まず、EKS 関連の Security Group (以下 SG) は 3 種類あります。

- クラスター SG
- コントロールプレーン SG
- ノード SG

## クラスターSG

EKS クラスターを作成した時に EKS 側で自動作成される SG.

デフォルトでは、クラスターSG 自身からの通信を全て許可するルールが付与されている。

注意点としては、CFn でルールをカスタマイズしてデプロイ等ができず、カスタマイズが必要な場合はクラスター作成後に**手動変更が必要になる**ところ。

> IaC 化を行っている場合だとここが残念

### アタッチされるリソース

- EKS コントロールプレーン通信用 ENI（EKS-managed ENI）
- Fargate ノード: EKS on Fargate 利用時
- マネージドノードグループ内の EC2 ノード: EKS on EC2 利用時

> ※ただし, 後述するノード SG が EC2 ノードに付与されている場合、クラスターSG は付与されない。

## コントロールプレーン SG

Optional で作成可能な SG.

クラスターSG とは別に、コントロープレーン ENI に追加ルールを設けたい時に作成する。

> こちらは IaC 化が可能なので、こちらで追加ルールの管理をするのがおすすめ。

AWS マネジメントコンソールの EKS クラスター設定で「追加のセキュリティグループ」と表示される。

### アタッチされるリソース

- EKS コントロールプレーン通信用 ENI（EKS-managed ENI）
> クラスターSG と違い、Fargate ノード、マネージドノードグループ 内の EC2 ノードには付与されない。

## ノード SG

Optional で、EKS on EC2 限定で使える SG.

マネージドノードグループ内の EC2 ノードに付与される。

コントロールプレーンや、ノード EC2 との通信が必要なリソース（他ノード、ALB など）からのアクセスを許可するために使用することが多い。

> こちらも IaC 化対応。クラスターSG 以外は基本的に対応している。

作成は必須ではなく、ノード SG の指定がなければクラスターSG がマネージドノードグループに自動適用される。

### アタッチされるリソース

- マネージドノードグループ内の EC2 ノード

# おわりに

AWS 側で制御ができる EKS 関連の SG については、以上となります。

ですが、これだけだと Fargate 上の Pod の制御がクラスターSG でしかできず、不便です。

そのための対応策として、Fargate 上の Pod に対しては、**Security Group Policy リソースを駆使する**必要があります。

> これを含めると実質 4 種類ありますね。書きながら思い出しました。

学習には、公式から出ている [チュートリアル: Pods のセキュリティグループ - Amazon EKS](https://docs.aws.amazon.com/ja_jp/eks/latest/userguide/security-groups-for-pods.html) などを参考にするのがおすすめです。

# 参考

- [EKSのセキュリティグループについて理解する #AWS - Qiita](https://qiita.com/MAKOTO1995/items/4e70998e50aaea5e9882)
- [チュートリアル: Pods のセキュリティグループ - Amazon EKS](https://docs.aws.amazon.com/ja_jp/eks/latest/userguide/security-groups-for-pods.html)
