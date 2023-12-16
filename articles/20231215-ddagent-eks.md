---
title: Datadog on EKS がややこしい
yaml_title: 20231215-ddagent-eks
created: 2023-12-15 15:16:44
updated: 2023-12-15 15:39:51
tags: 
aliases: 
emoji: ⛳
published: true
topics:
  - Kubernetes
  - Datadog
  - SRE
  - EKS
  - AWS
type: tech
---
# はじめに

EKS 上に Datadog を導入しようとしたら、思いの外手こずったので整理してまとめます。

# 概要

まず、EKS に Datadog を導入する場合、EKS on EC2 と EKS on Fargate でそれぞれ異なる Datadog Agent の導入が必要になります。

EC2 と Fargate を使い分けるような混合ワークロードの場合は、それぞれのワークロードに合わせた Agent の導入が必要になります。

## Datadog Agent in EKS on EC2

この構成の場合、一般的な EC2 と同じように、各ノードに対して一つの Agent が必要になります。

EKS の導入に関しても、基本的に [Kubernetes](https://docs.datadoghq.com/ja/containers/kubernetes/) ドキュメントの指示に従い導入を進めていきます。

> おすすめの導入方法は、Operator を利用したものです。

## Datadog Agent in EKS on Fargate

この構成の場合は、ECS タスクと似たような構成になり、Pod のサイドカーとして Agent をデプロイする必要があります。

公式ドキュメント [Amazon EKS on AWS Fargate](https://docs.datadoghq.com/ja/integrations/eks_fargate/#%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB) が提供されているので、こちらに従って進めるのが良いでしょう。

また、混合ワークロードを利用していて、Datadog Cluster Agent を利用する場合は、別途追加の設定が必要になります。

こちらも [Amazon EKS on AWS Fargate](https://docs.datadoghq.com/ja/integrations/eks_fargate/#cluster-agent-%E3%81%BE%E3%81%9F%E3%81%AF-cluster-checks-runner-%E3%81%AE%E5%AE%9F%E8%A1%8C) に設定方法が記載されています。

# 注意点
1. Datadog Cluster Agent を利用する場合、Fargate 上ではなく、EC2 ノード上でデプロイされているかどうかをしっかりと確認しましょう。私はこれに気づかず、結構時間持ってかれました。
2. タグを含めた環境変数周りの設定は、Agent 毎に都度設定しないといけません。IaC 化していると冗長的に感じることもありますが、頑張りましょう。
3. Fargate を利用している場合、Pods の数が多ければ多いほど、料金は増えていきます。事前にコストの試算を行いましょう。

# おわりに

 EKS における Datadog Agent の導入は、ワークロードによってかなり複雑化します。

 

 公式ドキュメントにも体系的にまとめてくれているところがなかったので、整理できてよかったです。

# 参考

[Kubernetes](https://docs.datadoghq.com/ja/containers/kubernetes/)

[Amazon EKS on AWS Fargate](https://docs.datadoghq.com/ja/integrations/eks_fargate/#%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB)
