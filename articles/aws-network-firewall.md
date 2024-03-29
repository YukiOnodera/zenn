---
title: AWSの盾、Network Firewall の仕組みとコストを解説！
yaml_title: aws-network-firewall
created: 2024-03-29 16:10:58
updated: 2024-03-29 16:43:33
tags: 
aliases: 
emoji: 🔥
published: true
published_at: 2024-04-01 10:00
topics:
  - AWS
  - security
  - network
  - firewall
type: tech
---

# はじめに

今回は AWS が提供する AWS Network Firewall について調査をしました。

ここでは、その**仕組みとコスト**についてまとめています。

会社で AWS Network Firewall の導入を検討している方は参考にしてみてください。

# AWS Network Firewall とは

AWS が提供する **Network レイヤーでの Firewall** です。

DMZ のような形で、Public Subnet と IGW の間に Network Firewall 専用の Subnet を設けて、きめ細やかなルール設定を行うことで、VPC 全体の Firewall として働きます。

![](/images/aws-network-firewall-20240329041203.png)

> https://aws.amazon.com/jp/network-firewall/

## 特徴

AWS Network Firewall のざっくりとした特徴を知りたい方は [AWS Network Firewall の特徴](https://aws.amazon.com/jp/network-firewall/features/) を参照してください。

日本語でざっくりとした説明が書いてあります。

# AWS Network Firewall の仕組み

 [こちらの資料](https://docs.aws.amazon.com/ja_jp/network-firewall/latest/developerguide/what-is-aws-network-firewall.html) を読みながら、内容をまとめていきます。

## How AWS Network Firewall Works

まず、AWS Network Firewall は、下記の図のように Internet Gateway と Customer subnet (Public subnet など) の**境界線で動作**します。

Firewall 専用の Subnet を作成するのですが、Firewall Subnet 内の Traffic は検査しないので、基本的に他の用途と併用するのは NG となります。

また、Firewall Subnet 内には、Firewall Endpoint が配置されるようになっております。

Multi-AZ 構成の場合、この Firewall Subnet は AZ 毎に必要となります。

![](/images/aws-network-firewall-20240329041439.png)

### Firewall Components in AWS Network Firewall

続いて、Firewall を作成する際の主なコンポーネントの紹介になります。

主なコンポーネントは下記の 3 つです。

- **Rule Group**
	- 使い回し可能なルールの集合体
	- 種類は stateful, stateless のどちらか
	- ここに追加するルールにより、通信を検査
- **Firewall Policy**
	- 使い回し可能な、複数の Rule Group と Policy level の設定をまとめたもの
- **Firewall**
	- Firewall Policy と VPC を紐づけるもの
	- この時、ログの設定なども決定

### High-level Steps for Implementing a Firewall

実際に**AWS Network Firewall を既存環境に導入する際に必要となるステップ**は下記の通りです。

1. Firewall Endpoint を配置するための専用 Subnet の作成
2. Firewall Policy, Firewall の作成
3. VPC ルートテーブルの修正

### Firewall Behavior

下記の図は、Firewall がパケットを処理する際の流れを表しています。

基本的には、 こんな感じ。

1. Stateless Rules の評価
2. Stateful Rules の評価

![](/images/aws-network-firewall-20240329041449.png)

### Considerations for Asymmetric Routing

AWS Network Firewall は、**非対称のルーティングをサポートしておりません。**

どう言うことかというと、インバウンドのトラフィックと、そのレスポンスとなるアウトバウンドトラフィックは、同じ Firewall Endpoint を経由しなければならないと言うことです。

下記のリソースが環境内にある場合は、非対称のルーティングが発生する可能性があるので、注意しましょう。

- Nat Gateway
- Stateless rules
- Centralized deployment model
- decentralized deployment model

詳しく知りたい方は、 [こちら](https://docs.aws.amazon.com/ja_jp/network-firewall/latest/developerguide/asymmetric-routing.html) を参照してください。

### Architecture and Routing Examples

AWS Network Firewall を導入した際の構成とルーティングに関する例がいくつか提供されています。

https://docs.aws.amazon.com/ja_jp/network-firewall/latest/developerguide/architectures.html

Multi-AZ 構成の方は下記の構成になると思います。

[Multi zone architecture with an internet gateway - AWS Network Firewall](https://docs.aws.amazon.com/ja_jp/network-firewall/latest/developerguide/arch-two-zone-igw.html)

### AWS Managed Rule Groups

Rule Group に関しては、自分で一から作成することも可能ですが、基本的には AWS が提供する Managed rule Groups 取り入れるのがいいと思います。

 [こちら](https://docs.aws.amazon.com/ja_jp/network-firewall/latest/developerguide/aws-managed-rule-groups-list.html) にその一覧と説明が書いてありますので、参考にしてください。

# AWS Network Firewall のコスト

続いてコストについてです。

基本的には、**Endpoint の設置に対する時間あたりの料金と、Data の処理に対する量あたりの料金**の**2 種類**が発生します。

また、今回は調査しておりませんが、Advanced Inspection というオプション機能を有効化している場合、さらに 2 項目料金が追加され、合計 4 項目の料金が発生するとのことです。

さらに特典として、**NAT GW の料金が利用料に応じて免除**されるようになっています。

![](/images/aws-network-firewall-20240329041416.png)

目安として、トラフィックが１か月あたり 5,000GB であり、機能をフルで利用した場合、約 $1,166 ほどかかるそうです。

![](/images/aws-network-firewall-20240329041430.png)

# こちらもおすすめ

https://zenn.dev/yukionodera/articles/good-about-mise

https://zenn.dev/yukionodera/articles/arc-2-released

https://zenn.dev/yukionodera/articles/how-to-manage-images-with-obsidiann

# おわりに

以上です！

AWS Network Firewall は、**セキュリティ対策を始める最初のツールとしてベストかも**しれないです。

# 参考

[AWS Network Firewall](https://aws.amazon.com/jp/network-firewall/)
