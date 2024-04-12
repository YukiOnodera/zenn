---
title: Datadog が提供するコスパ最強のアプリケーションセキュリティをご紹介します
yaml_title: datadog-asm-protection
created: 2024-04-12 15:33:16
updated: 2024-04-12 16:22:03
tags: 
aliases: 
emoji: 🍣
published: true
published_at: 2024-04-15 10:00
topics:
  - security
  - Datadog
  - application
  - waf
type: tech
---

# はじめに

今回は、Datadog ASM が提供する **Protection** 機能ついて紹介します。

Datadog ASM には、Protection 以外にも Traces, Signals, など Protection と連携した機能が複数ありますが、今回は Protection に絞って紹介しました。

Datadog ASM の概要についてはこちらを読んでみてください。

https://zenn.dev/yukionodera/articles/datadog-securities-services

# Datadog ASM の Protection 機能とは

Datadog Application Security Monitoring (ASM) では、脅威と判断されるリクエストやユーザーに対してブロック機能を提供しており、**Protection** 機能とは、これらの総称となります。

以下は、Protection 機能の中でも特筆すべき情報を整理し、よりわかりやすくまとめたものとなります。

## Deny List and Pass List

Datadog ASM では、IP アドレス or Path を元にした **Deny, Pass List** が作成できるようになっています。

まず、**Deny List** では、IP アドレスや User ID を基にリクエストをブロックすることが可能です。

15 分などの一時的なアクセス制限も可能で、特定の脅威からの保護に役立ちます。

主に Detection Rules や Signals と連携して使用されます。

次に、**Pass List** では、リクエストをブロックしたくない通信を IP, パスなどを指定してリストとして作成することができます。

特定のルールのみブロックしない、リクエストは監視だけしてブロックはしない、といったこともできます。

## IP Block

Datadog ASM では、GUI コンソールから**簡単に IP アドレスをブロック**できる機能が提供されています。この機能は、先ほど紹介した Deny List とシームレスに連携しているので、後からブロックした IP アドレスの一覧を確認することも可能です。

**15 分などの時間制限付き**でアドレスをブロックすることなども可能となっており、この機能がかなり重宝しています。

IP アドレスをブロックするときに、メモを残すことができるのも、**地味に便利な機能**です。

![](/images/datadog-asm-protection-20240412034522.png)

## In-App WAF

Datadog ASM の **In-App WAF** は、アプリケーションレベルで**不審なリクエスト**を識別、ブロックする強力なセキュリティ機能です。

不審なリクエストの検査は Datadog ライブラリによって行われ、認識されたリクエストはトレースエクスプローラー(Traces) に表示されます。

また、トレースエクスプローラーのリクエスト情報は Detection Rules での Signal 発行基準としても利用することができます。

**基本的には Datadog が定義した Rule を利用すれば十分機能を発揮してくれます**が、必要に応じてカスタムルールを追加することもできます。

AWS WAF と役割が被りますが、両者を比較した場合、設置位置、利用されるルールの種類、そして運用の容易さにおいて違いがあるかなと思います。

個人的には、AWS WAF でカバーできなかった不審なリクエストを検出するといったような補完的役割がいいのかなと思います。AWS WAF にない強みとして、Detection Rules やトレースとの連携、GUI を通じた直感的な操作による利便性などが挙げられます。

## Detection Rules

**Detection Rules** では、特定の脅威パターンを検出するルールを定義することで、潜在的な攻撃を検知することが可能になります。

これを利用することで、例えば、不特定多数の IP アドレスから攻撃が仕掛けられた場合でも、トレースの情報から攻撃元を割り出し、**攻撃元の User をブロック**するということが可能になっています。

これは、Datadog APM の導入が前提となっている Datadog ASM 特有の機能で、これがアプリケーションセキュリティの保護として**今後活躍しそう**だなと感じました。

デフォルトでは、Datadog が提供している OOTB Rules が有効化されており、これにより、トレースの情報から攻撃元を割り出して Signals としてアラートを出すことができるようになっています。

もちろん、自分でカスタムルールを追加することもできます。

また、アラートを出すことに加えて、自動で攻撃元を Block するような設定もできるようになっています。

これにより、**攻撃の検知からブロックまでが自動で完了**します。素晴らしい。

# こちらもおすすめ

https://zenn.dev/yukionodera/articles/good-about-mise

https://zenn.dev/yukionodera/articles/arc-2-released

https://zenn.dev/yukionodera/articles/how-to-manage-images-with-obsidiann

# おわりに

アプリケーションセキュリティの対策ツールに迷ったらとりあえずこれを入れておけば間違い無いんじゃないかと思いました。

今回、画像をあまり入れてないので伝わりづらかったと思いますが、GUI の利便性や情報提供量などもかなり充実していて、本当に使いやすいです。

今回は紹介していませんが、Datadog ASM では言語によって脆弱性管理なども提供されているので、気になっている方はぜひ。

# 参考

https://docs.datadoghq.com/security/application_security/threats/protection/
