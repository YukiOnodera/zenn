---
title: セキュリティを一歩先へ：Datadog Application Security Management による脆弱性管理と脅威対策
yaml_title: datadog-securities-services
created: 2024-03-08 10:51:48
updated: 2024-03-08 11:35:25
tags: 
aliases: 
emoji: 👏
published: true
topics:
  - Datadog
  - security
  - ASM
  - SCA
  - IAST
type: tech
---

# はじめに

今回は、Datadog が提供するセキュリティ機能の一つである、**Datadog Application Security Management**について調査しました。

すでに Datadog を導入していて、Application Security の導入を検討している方は参考にしてください。

# Datadog Application Security Management(Datadog ASM)

一言でまとめると、**コードレベルの脆弱性を利用しようとする攻撃に対する保護機能**を提供するものです。

主な機能は、下記の 3 つとなります。

- **脆弱性管理**
- **脅威検出**
- **脅威防御**

## WAF との違い

似たような Security 製品として WAF が挙げられますが、WAF との機能は大きく 2 つあります。

まず機能を配置する場所について違いがあります。

従来の WAF はインフラコンポーネントの境界に配置されますが、Datadog ASM は**アプリケーションとともに配置**されます。

どういうことかというと、Datadog ASM はサーバーの Agent やコンテナのサイドカーとして配置されるということです。これにより、**アプリケーショントレースに基づいた詳細な脅威管理ができる**ところがこの機能の特徴となります。

また、機能が得意とする役割にも違いがあります。

攻撃シグネチャなど**既存の情報に基づいて脅威をブロック**する WAF に対して、Datadog ASM は **IDS/IPS のようなサービス**としての意味合いが強く、アプリケーションのトレースを含めた様々な情報から**脅威を検出**することに優れています。

> WAF も IDS/IPS のような動きは可能だが、WAF はどちらかというと**脅威をブロック**する意味合いが強い。
> また、Datadog ASM はトレースなどを利用して検査を行うため、誤検知が少ない。

## 互換性

各言語と機能の対応状況については、[互換性要件](https://docs.datadoghq.com/ja/security/application_security/enabling/compatibility/) から確認ができるようになっています。

## 脆弱性管理

ここからは Datadog ASM が提供する機能について具体的に紹介していきます。

まず、脆弱性管理です。

これは、Datadog が提供する SCA となります。

[Getting Started with Software Composition Analysis](https://docs.datadoghq.com/ja/getting_started/application_security/software_composition_analysis/)

具体的には、Dependabot のような機能と IAST のような機能を有しています。

IAST は一般的には導入コストが高いものなので、Datadog Agent を利用して簡単にデプロイできることは特徴の一つですね。

## 脅威検出、脅威防御

次に、脅威検出と脅威防御についてです。

Datadog ASM は、**APM と同じトレーシングライブラリを使用**してトラフィックを監視します。

**既知の攻撃パターンであるシグネチャとトラフィックを比較し、脅威や攻撃を検出、サービスを防御**することが可能となっています。

WAF の代わりに使っても良さそうですが、その代わりトラフィックがコンテナまで到達する懸念があるので、基本的には併用するのがいいと思います。

実際にそのような [使い方](https://docs.datadoghq.com/ja/security/application_security/threats/protection/#%E6%94%BB%E6%92%83%E8%80%85%E3%82%92%E5%A2%83%E7%95%8C%E3%81%A7%E3%83%96%E3%83%AD%E3%83%83%E3%82%AF---asm-%E3%82%92%E6%97%A2%E5%AD%98%E3%81%AE-waf-%E3%83%87%E3%83%97%E3%83%AD%E3%82%A4%E3%81%A8%E3%82%A4%E3%83%B3%E3%83%86%E3%82%B0%E3%83%AC%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3) も紹介されています。

AWS WAF にあるような rate limit 機能などは使えなさそうですが、自動で Deny List に IP を追加したり、コンソールから簡単に IP のブロックをすることが可能になっています。

### OOTB Rules

脅威の検出には、Datadog が提供する OOTB Detection Rules に基づいて、**アプリケーション内での脅威を検出**することが可能となっています。

[OOTB Rules](https://docs.datadoghq.com/ja/security/default_rules/#cat-application-security) は、Datadog の Security Reserch Team により継続的に新しい Rules が追加されるので、常に最新の攻撃パターンに対応することができます。

### ユーザーモニタリングと保護

脅威防御の機能の一つとして、トレースからユーザーのアクティビティを追跡し、**アプリケーション上で不審な動きをするような悪質なユーザーを検出、ブロック**することが可能です。

これは、非認証ユーザーと認証済みユーザーどちらに対しても利用することができます。これはトレースなどアプリケーションの情報を利用しないといけないので、Datadog ASM の特徴に一つだと思います。

[ユーザーモニタリングと保護](https://docs.datadoghq.com/ja/security/application_security/threats/add-user-info/?tab=set_user)

### その他の機能

上記の機能に加えて、[保護](https://docs.datadoghq.com/ja/security/application_security/threats/protection/) による**脅威へのリアルタイムでの対応**や、[カスタム検出ルール](https://docs.datadoghq.com/ja/security/application_security/threats/custom_rules/) の作成、[アプリ内 WAF ルール](https://docs.datadoghq.com/ja/security/application_security/threats/inapp_waf_rules/) の追加などを可能で、ニーズに応じてカスタマイズできるようになっています。

### AWS WAF と併用する場合

**アプリケーション上の Datadog ASM により脅威を検出**した上で、**ネットワークの境界に配置された AWS WAF で脅威をブロック**するのがベストな構成かなと思います。

そうすることで、AWS WAF による**大まかな脅威対策**と、Datadog ASM による**アプリケーション毎のきめ細やかな脅威対策**が可能になります。

## コスト

それぞれの機能に関するコストは [料金 | Datadog](https://www.datadoghq.com/ja/pricing/?product=application-security-management#products) を確認してください。

AWS Fargate での利用であれば低コストでお試し利用も可能ですね。

# こちらもおすすめ

https://zenn.dev/yukionodera/articles/good-about-mise

https://zenn.dev/yukionodera/articles/easy-share-tab-with-google-meet

https://zenn.dev/yukionodera/articles/arc-2-released

# おわりに

ニーズがあれば他の https://docs.datadoghq.com/ja/security/ に記載されている Datadog Security 製品についても調査していこうと思います！
