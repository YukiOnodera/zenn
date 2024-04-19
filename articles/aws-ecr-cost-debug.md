---
title: 知らぬ間に ECR の料金が10倍以上になっていた
yaml_title: aws-ecr-cost-debug
created: 2024-04-19 15:39:18
updated: 2024-04-19 16:00:40
tags: 
aliases: 
emoji: 💭
published: true
published_at: 2024-04-22 10:00
topics:
  - ecr
  - AWS
  - Cost
  - CostExplorer
type: tech
---

# はじめに

先日 Cost Explorer を眺めていたら、ECR の料金が**数ヶ月前から 10 倍以上**に膨れ上がっているのを発見しました。

# 調査開始

これはまずいと思い、**即座に原因調査**を開始しました。

## ECR の料金体系確認

まず、**ECR の料金体系を確認**するところから始めました。

https://aws.amazon.com/jp/ecr/pricing/

ECR の料金は、**イメージ保存量に応じたストレージ料金と、外部へのデータ転送量**で決まるそうです。

## 請求書確認

次に、**先月の請求書の確認**を行いました。

**ストレージとデータ転送量のどちらの料金が増えているのかを確認**するためです。

このとき、ECR の請求欄を確認しても、ECR のストレージの料金しか参照できません。

データ転送量に関しては、別途データ転送量の項目が設けられているので、そちらを確認しましょう。自分はこれに気づかずに、料金違うのなんで？？？という状況に陥りました。

自分の場合は、**データ転送量の料金が圧倒的に増加**していました。

## AWS アカウントの確認

AWS Organizations を使っていたので、**どのメンバーアカウントの ECR 料金が上がっているのかを確認**しました。

幸いなことに、料金が増加しているアカウントがひとつだけだったので、すぐに原因となっているアカウントを絞ることができました。

## ECR Repository の確認

ただ、AWS アカウントがわかっただけでは問題を解決できません。

とりあえず ECR Repository の一覧をざっと開いて確認してみました。

すると、**料金が増加する時期に作成された Repository がちらほら**。

## コスト増加の原因

メンバーなどにも確認しつつ調べていると、ci に利用する Repository を Docker Hub から移行してきたものであるということがわかりました。

ci はコミット時に Github Actions 上で実行されるようにしており、Image size がそこそこ大きいものを複数 pull していたので、**転送料金が高騰**していたようです。

# こちらもおすすめ

https://zenn.dev/yukionodera/articles/good-about-mise

https://zenn.dev/yukionodera/articles/datadog-asm-protection

https://zenn.dev/yukionodera/articles/how-to-manage-images-with-obsidiann

# おわりに

原因わかってよかったです。というより、Cost Explorer で気づけたことが**ラッキー**でした。

クラウドは思わぬところで料金が上がっていることがあるので、気をつけないとですね。

# 参考

https://docs.docker.com/docker-hub/download-rate-limit/
