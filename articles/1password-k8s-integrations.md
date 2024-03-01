---
title: Kubernetes 環境で 1Password を活用する方法
yaml_title: 1password-k8s-integrations
created: 2024-03-01 15:09:44
updated: 2024-03-01 15:21:04
tags: 
aliases: 
emoji: 📌
published: true
topics:
  - Kubernetes
  - 1password
type: tech
---

# はじめに

今回は、1Password が提供する **Kubernetes Integrations** について調査します。

[Kubernetes integrations | 1Password Developer](https://developer.1password.com/docs/k8s/k8s-integrations)

これを使うことにより、**Kubernetes 環境から 1Password の情報を参照**することができるようになります。

# 1Password Kubernetes Integrations

はじめに、1Password Kubernetes Integrations を利用するにあたって、重要な Component が 3 つあります。

- Connect Server
- Operator
- Injector

まずはこれらの Component が果たす役割について紹介します。

## Connect Server

Connect Server は、1Password のセキュアな情報管理機能を Kubernetes クラスター内のアプリケーションやサービスで利用できるようにする**API サーバー**です。

これにより、Kubernetes のリソースが 1Password に保存されている秘密情報や資格情報にアクセスできるようになります。

Connect サーバーは、**1Password のアカウントと Kubernetes クラスター間の橋渡し役**として機能し、セキュリティを維持しながら秘密情報の管理とアクセスを容易にします。

## Operator

Operator は、特定のアプリケーションを Kubernetes 上で実行し、管理するための方法を提供するための Component です。

Kubernetes クラスター内で Connect Server を使用して秘密情報を安全に管理し、アプリケーションがそれらの情報にアクセスできるようにするための**カスタムリソース定義（CRD）とロジックを提供**します。

これにより、開発者は Kubernetes の**マニフェストファイル内で直接 1Password の秘密情報を参照できる**ようになり、セキュリティと利便性が向上します。

## Injector

Injector は、**Kubernetes のポッドが起動する際に、自動的に 1Password から秘密情報を取得して、それらを環境変数としてポッド内に注入する機能**を提供します。

これにより、アプリケーションは起動時に必要な秘密情報を安全に取得でき、開発者は秘密情報のハードコーディングや不適切な管理方法を避けることができます。

インジェクターは、セキュリティのベストプラクティスを容易に実装しながら、アプリケーションの設定を簡素化します。

# 1Password Helm Charts

1Password では、**上記の Connect Server, Operator, Injector を簡単にデプロイ**するために、Helm charts を提供しています。

[1Password Helm charts | 1Password Developer](https://developer.1password.com/docs/k8s/k8s-helm/)

[Helm chart configuration | 1Password Developer](https://developer.1password.com/docs/connect/helm/) で **Helm chart configuration** も確認可能になっているので、設定からデプロイまで簡単に完結します。

# おわりに

1Password で認証情報を一元管理できるのはすごく便利です。

ぜひ使ってみてください。

# こちらもおすすめ

https://zenn.dev/yukionodera/articles/good-about-mise

https://zenn.dev/yukionodera/articles/easy-share-tab-with-google-meet

https://zenn.dev/yukionodera/articles/how-to-manage-images-with-obsidiann
