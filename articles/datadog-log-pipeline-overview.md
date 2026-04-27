---
title: DatadogのログパイプラインとLogging without Limitsの仕組み
emoji: 🪵
type: tech
topics:
  - Datadog
  - observability
  - logging
published: true
---

# はじめに

今回は、Datadogのログ管理における処理フローについてまとめます。

Datadogのログ管理画面を触っていると、生のログがパイプラインを通じてどんどんリッチになっていく過程が見えて、面白いなと感じました。その仕組みを整理しておきたいと思います。

:::message
この記事では自分が今回学んだ主要なステップに絞って紹介しています。実際にはセンシティブデータスキャンやError Tracking、Live Tailなど、さらに詳細なプロセスが存在します。全体像は[公式ドキュメント | Datadog](https://docs.datadoghq.com/logs/)を参照してください。
:::

# ログ処理の全体フロー

Datadogのログ管理は **Logging without Limits™** という設計思想のもと動いており、「取り込み」「保存」「分析」をそれぞれ独立して制御できるようになっています。

処理の大まかな流れは以下の通りです。

```
Ingest（取り込み）
  ↓
Pipelines（パース・エンリッチ）
  ↓
Generate Metrics（メトリクス生成）
  ↓
Exclusion Filters（除外フィルタ）
  ↓
Index（インデックス保存）
```

# 各ステップの解説

## Ingest（取り込み）

まず、様々なソースからログをDatadogに取り込みます。

Datadogには **500以上のログインテグレーション** が用意されており、AWS・GCP・Kubernetes・各種ミドルウェアなど、幅広いソースに対応しています。これだけの数があるのかと最初は驚きました。

## Pipelines（パース・エンリッチ）

取り込んだ生のログを、**パイプライン**を通じて構造化・エンリッチ（情報付加）します。

**Grokパーサー**などのプロセッサーを使って、非構造化テキストのログをフィールドに分解したり、属性を追加したりします。

```
# パース前（生ログ）
2024-04-27 12:00:00 ERROR [app] Connection timeout: host=db01 duration=5002ms

# パース後（構造化）
{
  "timestamp": "2024-04-27T12:00:00Z",
  "level": "ERROR",
  "service": "app",
  "message": "Connection timeout",
  "host": "db01",
  "duration_ms": 5002
}
```

未成形のログが整形されてリッチになっていくこの過程が、眺めていて一番面白いポイントでした。

## Generate Metrics（メトリクス生成）

ここが Logging without Limits の設計で最も興味深いポイントです。

**ログベースメトリクスの生成は、除外フィルタよりも前**に実行されます。

つまり、後のステップでインデックスから捨てることになるログからでも、メトリクスとして統計情報を残しておくことができます。

:::message
コストを抑えるためにログを大量に捨てていても、傾向やエラー率などのメトリクスはきちんと取れる、というのがこの設計のメリットです。
:::

## Exclusion Filters（除外フィルタ）

メトリクス生成の後、**除外フィルタ**でインデックスに保存しないログを選別します。

デバッグログや大量の定型ログなど、常時検索には不要なものをここで弾くことで、インデックスのコストを抑えられます。

## Index（インデックス保存）

最終的にフィルタを通過したログが **Index** に保存されます。インデックスに入ったログは、Datadogの画面でファセット検索や分析が可能になります。

# なぜこの順序が重要なのか

この処理順序のポイントは、**「捨てる前にメトリクスを取る」** という設計にあります。

ログの保存コストは膨大になりがちなので、全部のログをインデックスに入れることは現実的ではありません。しかしそれでは、捨てたログの傾向が見えなくなってしまいます。

Logging without Limits はメトリクス生成を除外フィルタの前に置くことで、この問題を解決しています。保存コストを下げながら、可観測性は最大化できる設計です。

# おわりに

Datadogのログパイプラインは、取り込み・パース・メトリクス生成・除外・インデックス保存と、各ステップが明確に分離されています。特にメトリクス生成が除外フィルタの前に走るという設計は、コストと可観測性を両立するうえで重要なポイントだと感じました。

# こちらもおすすめ

https://zenn.dev/yukionodera/articles/datadog-asm-protection

https://zenn.dev/yukionodera/articles/datadog-reserved-tags-ust

https://zenn.dev/yukionodera/articles/datadog-node-agent-cluster-agent
