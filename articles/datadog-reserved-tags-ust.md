---
title: Datadogのタグには予約語がある ─ Reserved TagsとUnified Service Taggingを理解する
emoji: 🏷️
type: tech
topics:
  - Datadog
  - monitoring
  - observability
published: false
---

## はじめに

今回は、Datadog の **Reserved Tags** と **Unified Service Tagging（UST）** についてまとめます。

ふと「Datadog のタグって自由に名前をつけていいの？」と思って調べたら、あらかじめ用途が決まっている予約タグが存在することを知りました。知らずに使っていると意図しない挙動になることもあるので、整理しておきます。

## Reserved Tags とは

**Reserved Tags** とは、Datadog があらかじめ用途を定めたタグのことです。プログラミング言語の予約語と同じイメージで、「この名前は特定の意味を持つ」と決められています。

定められた用途以外に使うことは推奨されておらず、現在は以下の7種類が Reserved Tags として定義されています。

| タグ | 用途 |
|------|------|
| `host` | メトリクス・トレース・プロセス・ログをホスト単位で紐づける |
| `device` | メトリクス・トレース・プロセス・ログをデバイス・ディスク単位で分離する |
| `source` | ログ管理におけるスパンフィルタリングとパイプラインの自動生成 |
| `service` | メトリクス・トレース・ログをサービス単位でスコープする |
| `env` | メトリクス・トレース・ログを環境単位でスコープする |
| `version` | メトリクス・トレース・ログをバージョン単位でスコープする |
| `team` | リソースのオーナーシップをチーム単位で割り当てる |

[Getting Started with Tags | Datadog](https://docs.datadoghq.com/getting_started/tagging/)

## Unified Service Tagging（UST）とは

**Unified Service Tagging（UST）** は、Reserved Tags の中でも特に重要な3つ ─ `service`・`env`・`version` ─ を使った運用ベストプラクティスです。

:::message
UST は Reserved Tags の**部分集合**です。「この3つのタグを統一した形で全テレメトリに付与しましょう」という運用の考え方を指します。
:::

なぜこの3つなのかというと、サービスの観測において「**どのサービスの**（service）」「**どの環境の**（env）」「**どのバージョンの**（version）」データかを特定できれば、問題の切り分けに必要な軸がほぼ揃うからです。

この3つは環境変数（`DD_SERVICE`・`DD_ENV`・`DD_VERSION`）で一元設定でき、設定した値がトレース・ログ・メトリクス・RUM など**すべてのテレメトリに自動的に付与**されます。

[Unified Service Tagging | Datadog](https://docs.datadoghq.com/getting_started/tagging/unified_service_tagging/)

## UST があると何が変わるのか

UST が設定されていると、Datadog の UI でトレース・ログ・メトリクスが**自動でワンクリックでつながります。**

具体的には、以下のような操作がシームレスにできるようになります。

- メトリクスのグラフから、異常が発生した時間帯の**トレースに直接ジャンプ**する
- トレースの詳細画面から、そのリクエストに紐づく**ログをインラインで確認**する
- ログから**関連する APM サービスやインフラメトリクス**へ移動する

:::message
UST がないと「探せばたどり着ける」レベルになります。タイムスタンプを手がかりに手動でログを検索したり、サービス名を自分でフィルタして絞り込んだりする必要があり、インシデント対応時の速度に差が出ます。
:::

また、`version` タグを付与しておくと、デプロイ前後でエラーレートやレイテンシを自動で比較できるため、リリースの影響確認にも役立ちます。

## おわりに

「タグは自由につけていい」と思っていたのですが、Reserved Tags という概念を知ってからは、タグ設計に一定のルールがあることがわかりました。

UST の3つのタグを最初からきちんと設定しておくと、後から観測性を高めようとしたときの手戻りが少なくなりそうです。

## 参考

[Getting Started with Tags | Datadog](https://docs.datadoghq.com/getting_started/tagging/)

[Unified Service Tagging | Datadog](https://docs.datadoghq.com/getting_started/tagging/unified_service_tagging/)

[Correlate Logs and Traces | Datadog](https://docs.datadoghq.com/tracing/other_telemetry/connect_logs_and_traces/)
