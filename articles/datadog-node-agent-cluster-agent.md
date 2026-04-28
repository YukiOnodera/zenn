---
title: DatadogのKubernetesモニタリングを支える2層構成：Node AgentとCluster Agent
emoji: 🐶
type: tech
topics:
  - Datadog
  - Kubernetes
  - monitoring
published: true
published_at: 2026-04-29 19:00
---

## はじめに

今回は、Datadog の Kubernetes モニタリングを支える **Node Agent** と **Cluster Agent** の2層構成についてまとめます。

最初は「なぜ Agent が2種類あるのか」がよくわからなかったのですが、設計の意図を理解したら構成がシンプルに見えてきました。同じく疑問に思った方の参考になれば幸いです。

## 全体構成

Datadog の Kubernetes モニタリングは、以下の2つのコンポーネントで成り立っています。

```
┌─────────────────────────────────────────┐
│               Kubernetes Cluster        │
│                                         │
│  ┌──────────┐  ┌──────────┐             │
│  │Node Agent│  │Node Agent│  ...        │  ← DaemonSet（各ノードに1つ）
│  └────┬─────┘  └────┬─────┘             │
│       │              │                  │
│       └──────┬───────┘                  │
│              ↓                          │
│      ┌───────────────┐                  │
│      │ Cluster Agent │                  │  ← Deployment（クラスタに1つ）
│      └───────┬───────┘                  │
│              ↓                          │
│       Kubernetes API Server             │
└─────────────────────────────────────────┘
```

Node Agent が各ノードのデータを収集し、Cluster Agent がクラスタ全体の情報を一手に管理する構成です。

## Node Agent の役割

**Node Agent** は、`DaemonSet` としてクラスタの各ノードに1つずつ常駐します。担当範囲は「そのノード」に限定されており、収集するのは以下のデータです。

- そのノード上のコンテナのメトリクス
- アプリケーションのログ・トレース

収集したデータには、Cluster Agent から受け取ったクラスタ全体のメタデータ（Pod 名・サービス名・ラベルなど）をタグとして付与したうえで、Datadog に送信します。

ポイントは、**Node Agent は Kubernetes API Server に直接アクセスしない**という点です。クラスタ全体の情報の取得は、すべて Cluster Agent に委ねています。

## Cluster Agent の役割

**Cluster Agent** は、`Deployment` としてクラスタに1つだけ（または少数）動きます。Node Agent とは異なり、クラスタ全体を俯瞰する役割を担います。

主な責務は以下の通りです。

- **Kubernetes API Server への代表アクセス**：クラスタ全体のメタデータ（Pod・Service・Deployment 情報など）を 30 秒おきに取得してキャッシュする
- **Node Agent へのメタデータ配布**：各 Node Agent からの問い合わせに対して、キャッシュ済みのメタデータを返す
- **Kubernetes イベントの収集**：Pod のライフサイクルやノードの状態変化などのイベントを収集して Datadog に転送する

## なぜ2層構成なのか

ここが今回の一番の気づきでした。

**もし Node Agent が全員で直接 API Server を叩いたら**、どうなるでしょうか。たとえば 200 ノードのクラスタがあれば、200 個の Node Agent がそれぞれ定期的に API Server へリクエストを投げることになります。これは API Server への大きな負荷になり、クラスタの安定性にも影響しかねません。

Cluster Agent はこの問題を解決するために存在します。

```
Before（Node Agent が直接アクセス）:
Node Agent × 200 → API Server  ← 負荷が爆発する

After（Cluster Agent 経由）:
Node Agent × 200 → Cluster Agent → API Server  ← API Server へのアクセスは1本
                         ↑
                    キャッシュを配布
```

Cluster Agent が「代表」として API Server からデータを取得・キャッシュし、各 Node Agent にはそのキャッシュを返す設計にすることで、**クラスタが大きくなっても API Server への負荷が増えない**構成を実現しています。

セキュリティ面でも利点があります。Node Agent は API Server への直接アクセス権限が不要になるため、RBAC 設定をシンプルに保てます。

## おわりに

「なぜ2種類あるのか」という疑問も、設計の意図から逆引きすると一気に腑に落ちました。

スケールしても安定するモニタリング基盤のために、こういう設計になっているんだと理解できると、構成図を見たときの解像度が上がります。

## 参考

[Cluster Agent for Kubernetes | Datadog](https://docs.datadoghq.com/containers/cluster_agent/)

[Set Up the Datadog Cluster Agent | Datadog](https://docs.datadoghq.com/containers/cluster_agent/setup/)

[Introducing the Datadog Cluster Agent | Datadog Blog](https://www.datadoghq.com/blog/datadog-cluster-agent/)
