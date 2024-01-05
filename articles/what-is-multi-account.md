---
title: AWS のマルチアカウント構成とそのベストプラクティス
yaml_title: what-is-multi-account
created: 2024-01-05 17:22:24
updated: 2024-01-05 17:33:36
tags: 
aliases: 
emoji: 📝
published: true
topics:
  - AWS
  - ControlTower
  - LandingZone
type: tech
---
# はじめに

AWS のアカウント構成を整備するために、AWS のマルチアカウント構成とベストプラクティスについて調べました。

> マルチアカウント構成とは、AWS のアカウントを複数にわけて運用する構成のこと

# マルチアカウント構成によるメリット

AWS アカウントを分割することで、一般的には下記のようなメリットがある。

- 本番や開発など、環境毎に分けることで**セキュリティ、ガバナンス、規制**などを分けることができる
- **課金**体系を明確に分けることができる
- 組織のガバナンスに合わせて、アカウントに対する**権限**を明確に分けることができる
- サービスやデータに応じて、**ワークロード**を分けることができる

# マルチアカウント構成により生じる課題

一方で、ただアカウントを分けただけだと、下記のような課題が浮き彫りになってきてしまいます。

- アカウント間での**共通設定に関する整合性**が取れない
- 各アカウントに行う**設定や構築作業の複雑化**
- 継続的な**コンプライアンス管理の負荷**

# 課題を解消するためには

マルチアカウント構成を取り入れつつ、課題を解決するための最適な構成はどういったものなのか？

それを解決してくれる資料の一つが、AWS が提供するベストプラクティス集である、[AWS Well-Architected](https://aws.amazon.com/jp/architecture/well-architected/?wa-lens-whitepapers.sort-by=item.additionalFields.sortDate&wa-lens-whitepapers.sort-order=desc&wa-guidance-whitepapers.sort-by=item.additionalFields.sortDate&wa-guidance-whitepapers.sort-order=desc)。

そして、[AWS Well-Architected](https://aws.amazon.com/jp/architecture/well-architected/?wa-lens-whitepapers.sort-by=item.additionalFields.sortDate&wa-lens-whitepapers.sort-order=desc&wa-guidance-whitepapers.sort-by=item.additionalFields.sortDate&wa-guidance-whitepapers.sort-order=desc) などを参考に、マルチアカウント構成を展開することを可能にした仕組みの総称であり、概念となるのが、**Landing Zone**。

さらに、Landing Zone を実現するためのマネージドサービスが、**AWS Control Tower**。

つまり、**AWS Control Tower を利用してマルチアカウント構成を作成することで、マルチアカウント構成による課題を極力発生させずに、運用していくことが可能**となります。

### Landing Zone

Landing Zone は、主に 5 つの機能から構成される。

- 必要な初期設定の済んだアカウント発行
- 対象アカウントを管理するための権限発行
- AD, ファイルサーバなどの共有環境へのアクセスの実装
- 監査用ログの集約
- ガードレールの設置

### AWS Control Tower

Control Tower では、主に 5 つの機能が提供されている。

- AWS Organizations を利用したマルチアカウント環境の作成
- AWS SSO を利用した ID 管理の提供
- AWS SSO を使用したアカウントへの Federated Access の提供
- CloudTrail, AWS Config など、監査関連ログの集中管理
- IAM, SSO などを利用したクロスアカウントセキュリティ監査

これらをマネージドで構成し、機能として提供しているのが、Control Tower である。

> Landing Zone で必要とされる機能を、より具体的に実現しているサービスとなる。

# おわりに

どのようにマルチアカウント構成を作成していけば良いのかを知ることができてよかったです。

# 参考

[AWS マルチアカウント管理を実現するベストプラクティスとは ?](https://aws.amazon.com/jp/builders-flash/202007/multi-accounts-best-practice/?awsf.filter-name=*all)

[AWS Organizations における組織単位のベストプラクティス | Amazon Web Services ブログ](https://aws.amazon.com/jp/blogs/news/best-practices-for-organizational-units-with-aws-organizations/)

[AWS Well-Architected](https://aws.amazon.com/jp/architecture/well-architected/?wa-lens-whitepapers.sort-by=item.additionalFields.sortDate&wa-lens-whitepapers.sort-order=desc&wa-guidance-whitepapers.sort-by=item.additionalFields.sortDate&wa-guidance-whitepapers.sort-order=desc)

[AWS 規範ガイダンス](https://aws.amazon.com/jp/prescriptive-guidance/?apg-all-cards.sort-by=item.additionalFields.sortDate&apg-all-cards.sort-order=desc&awsf.apg-new-filter=*all&awsf.apg-content-type-filter=*all&awsf.apg-code-filter=*all&awsf.apg-category-filter=*all&awsf.apg-rtype-filter=*all&awsf.apg-isv-filter=*all&awsf.apg-product-filter=*all&awsf.apg-env-filter=*all)
