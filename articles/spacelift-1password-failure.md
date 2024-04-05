---
title: IaCで利用する認証情報を1Password で一元管理しようとしたら失敗した話
yaml_title: spacelift-1password-failure
created: 2024-04-05 10:10:37
updated: 2024-04-05 10:40:07
tags: 
aliases: 
emoji: 👌
published: true
published_at: 2024-04-08 10:00
topics:
  - 1password
  - Spacelift
  - sops
  - Terraform
  - IaC
type: tech
---

# はじめに

先日、認証情報を 1Password から Spacelift に引っ張ってこようとしたら失敗しました。

やりたかったことは、**1Password での認証情報の一元管理**です。

そのために、こんなことを行いました。

- 1Password で service account token を発行
- sops で service account token を暗号化し、Github で管理
- Spacelift 上で、sops から service account token を復号して、1Password の認証情報を参照できるように data sources を作成
- Spacelift 上で作成する Resources から data sources を利用して 1Password の認証情報を参照

https://developer.1password.com/docs/service-accounts/

# 問題

では、なぜこれがうまくいかなかったのでしょうか？

原因は**主に 2 つ**ありました。

## 原因 1

1 つ目は、**1Password 側で IP 制限をかけていた**ことです。

これにより、接続できる IP アドレスが限られていました。

Spacelift では、Enterprize Plan に入ることで Private 環境で Worker を動作させることも可能ですが、コストが高いため今回は断念しました。

https://spacelift.io/pricing

## 原因 2

2 つ目は、**Spacelift の Public Worker に op cli が入っていない**ことです。

https://developer.1password.com/docs/cli/get-started/

1Password の data sources を利用するために、1Password provider の設定が必要になるのですが、この provider を利用するには、動作ホストに op cli が入っていなければなりません。

しかし、Spacelift の Public Worker にはそれがありませんでした。自前で Docker Image を作成しそれを運用することも可能ですが、今回はそもそも IP 制限の壁があったので、こちらも断念しました。

> 仮に IP 制限の壁を突破できたとしても、ここで Docker Image を運用していくかどうかはまた考慮が必要になりそうです。

https://docs.spacelift.io/concepts/configuration/runtime-configuration/#runner_image-setting

# 解決方法

1Password に IP 制限がかかっておらず、Docker Image の運用も手間でなければ、冒頭でやりたかったこととして提示した、**1Password での認証情報の一元管理**も捗ると思います。

# こちらもおすすめ

https://zenn.dev/yukionodera/articles/good-about-mise

https://zenn.dev/yukionodera/articles/arc-2-released

https://zenn.dev/yukionodera/articles/how-to-manage-images-with-obsidiann

# おわりに

多数のサービスを抱える立場としては、**いろいろな面で可能な限り一元管理を推進していきたい**んですが、現実はそううまくいくとも限らず。あるあるですね。

似たような仕組みを検討している方の参考になってたら嬉しいです。

# 参考

https://1password.com/jp

https://github.com/getsops/sops

https://spacelift.io/
