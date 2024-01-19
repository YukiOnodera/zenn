---
title: OpenTofu が GA に！新機能や今後の方針まとめ
yaml_title: opentofu-ga-v1-6
created: 2024-01-18 17:41:01
updated: 2024-01-19 13:47:02
tags: 
aliases: 
emoji: 👻
published: true
published_at: 2024-01-19 11:00
topics:
  - Terraform
  - OpenTofu
  - IaC
type: tech
---
# はじめに

[OpenTofu がGA](https://opentofu.org/blog/opentofu-is-going-ga/) となりましたので、ざっくりとその内容について紹介します。

# そもそも OpenTofu とは

端的にいえば、Terraform の OSS Version です。

経緯としては、2023 年の 8 月ごろに、Terraform のライセンスが v1.5.5 以降から BSL に変わることが発表されました。[^1] つまり、**Terraform の商用利用に制限**がつくようになったのです。

その影響で、Spacelift, Terragrunt など Terraform を利用したエコシステム群は Terraform v1.5.5 以降のバージョンに対応できなくなったため、新たに OSS の **OpenTofu Project が発足**されました。

# 新機能

OpenTofu 1.6.0 で実装された主な新機能は、以下の **3 つ**となります。

- test 機能
- s3 state backend で指定できるオプションの拡充
- OpenTofu のための Registry

**基本は Terraform 1.6.0 を追っていく形**となるので、Registry 以外は Terraform と差分ないですね。他にももちろんいくつか細かい修正はあると思うんですが、今回は割愛します。

# OpenTofu の今後について

最も重要で基本的な方針として、**今後も Terraform との互換性を保ち、相互での Migration Paths を維持しながら開発**を行なっていくとのことです。

# OpenTofu 1.7 で予定しているもの

1.7 では、下記の実装を進めているとのことです。

- Client Side State encryption
	- Local の State File, plan File などの暗号化
- modules, providers, backends などの Instance 化
- adding new state backends
	- OSS であることを生かし、ThirdParty ツールとの連携拡充

# おわりに

新しく GA したサービスの記事は読んでいて面白いですね。

v1.7 で実装が予定されている機能もどれも有用性がありそうで、楽しみです。

詳細は [こちら](https://opentofu.org/blog/opentofu-is-going-ga/) にあるので、気になった方は読んでみてください！

# 参考

[OpenTofu is going GA | OpenTofu](https://opentofu.org/blog/opentofu-is-going-ga/)

[https://spacelift.io/blog/why-should-you-switch-to-opentofu](https://spacelift.io/blog/why-should-you-switch-to-opentofu)  
[https://opentofu.org/](https://opentofu.org/)  
[https://arc.net/l/quote/ktlhqmid](https://arc.net/l/quote/ktlhqmid)

[^1]: [OpenTofu Release Candidate Is Out, GA Set for Jan 10th | OpenTofu](https://opentofu.org/blog/opentofu-release-candidate-is-out/)
