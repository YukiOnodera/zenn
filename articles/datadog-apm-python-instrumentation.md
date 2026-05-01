---
title: Datadog APM で Python アプリを計装するために必要なこと【Docker 編】
emoji: 🔭
type: tech
topics:
  - Datadog
  - APM
  - Python
  - Docker
  - observability
published: true
---

# はじめに

今回は、Datadog APM を使って Python アプリケーションを計装するために必要なコンポーネントと、Docker 環境での設定方法についてまとめます。

「Datadog Agent とライブラリを入れればなんとかなる」という認識は正しいのですが、それぞれの内部でどのコンポーネントが何をしているのかを理解しておくと、トラブル時の原因切り分けが格段にしやすくなります。

# Datadog APM の構成要素

Datadog APM でアプリを計装するには、大きく **Agent 側** と **ライブラリ側** の 2 つの準備が必要です。

## Agent 側：Trace Agent

Datadog Agent で APM を有効化すると、内部で **Trace Agent** というコンポーネントが起動します。

Trace Agent はアプリケーションから送られてくるトレースデータを受け取り、Datadog のバックエンドへ転送する役割を担います。デフォルトでは **8126/tcp** ポートでトレースを受け付けます。

Docker 環境では以下の環境変数で APM を有効化します。

| 環境変数 | 説明 |
| --- | --- |
| `DD_APM_ENABLED` | APM（Trace Agent）を有効化する |
| `DD_APM_NON_LOCAL_TRAFFIC` | 別コンテナからのトレース送信を許可する |

:::message
`DD_APM_NON_LOCAL_TRAFFIC=true` を設定しないと、同じ Docker ネットワーク内の別コンテナからのトレースが受け付けられないため注意が必要です。
:::

## ライブラリ側：ddtrace

Python アプリ側には **ddtrace** というライブラリを使います。Datadog 公式の Python APM クライアントで、Flask・Django・SQLAlchemy など 80 以上のライブラリに対応した自動計装を提供しています。

```sh
pip install ddtrace
```

# Auto Instrumentation の仕組み：Monkey Patching

ddtrace の Auto Instrumentation は **Monkey Patching** という仕組みで動作します。

**Monkey Patching** とは、プログラムの実行時に既存のクラスや関数を動的に差し替える手法です。ddtrace はこれを利用して、アプリのコードを変更せずに対応ライブラリへのトレース計装を差し込みます。

実装方法は 2 つあります。

## ddtrace-run コマンド（推奨）

アプリの起動コマンドの先頭に `ddtrace-run` を付けるだけです。

```sh
ddtrace-run python app.py
```

Dockerfile では CMD を以下のように変更します。

```dockerfile:Dockerfile
CMD ["ddtrace-run", "python", "app.py"]
```

## import ddtrace.auto

エントリーポイントの先頭でインポートする方法もあります。

```python
import ddtrace.auto

from flask import Flask
# ...
```

:::message alert
`ddtrace-run` と `import ddtrace.auto` を同時に使うと二重に Monkey Patching が適用されるため、どちらか一方のみ使用してください。
:::

# Docker 環境での設定

## Agent コンテナ

```yaml:docker-compose.yml
services:
  datadog-agent:
    image: gcr.io/datadoghq/agent:latest
    environment:
      DD_API_KEY: ${DD_API_KEY}
      DD_SITE: datadoghq.com
      DD_APM_ENABLED: "true"
      DD_APM_NON_LOCAL_TRAFFIC: "true"
    ports:
      - "8126:8126/tcp"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
```

## アプリコンテナ

アプリコンテナ側では、Agent コンテナへの接続先を環境変数で指定します。

```yaml:docker-compose.yml
services:
  myapp:
    build: .
    environment:
      DD_AGENT_HOST: datadog-agent
      DD_TRACE_AGENT_PORT: "8126"
      DD_SERVICE: my-python-app
      DD_ENV: production
      DD_VERSION: 1.0.0
    depends_on:
      - datadog-agent
```

`DD_AGENT_HOST` には Docker Compose のサービス名をそのまま指定できます。

# Unified Service Tagging

`DD_SERVICE` / `DD_ENV` / `DD_VERSION` の 3 つは **Unified Service Tagging** と呼ばれる仕組みで、Datadog 全体のテレメトリを横断的に紐づけるための標準タグです。

| 環境変数 | 説明 | 例 |
| --- | --- | --- |
| `DD_SERVICE` | サービス名 | `my-python-app` |
| `DD_ENV` | 環境名 | `production`, `staging` |
| `DD_VERSION` | バージョン | `1.0.0` |

この 3 つを設定しておくことで、APM のトレース画面から関連するログやメトリクスへワンクリックで移動できるようになります。設定しておくことを強くおすすめします。

# おわりに

Datadog APM の計装は、Agent 側の Trace Agent とライブラリ側の ddtrace（Monkey Patching）の 2 つが連携することで成り立っています。Docker 環境では `DD_APM_NON_LOCAL_TRAFFIC=true` と `DD_AGENT_HOST` の設定が特にハマりやすいポイントなので、セットアップ時に意識してみてください。

# 参考

[Tracing Docker Applications | Datadog](https://docs.datadoghq.com/containers/docker/apm/)

[Tracing Python Applications | Datadog](https://docs.datadoghq.com/tracing/trace_collection/automatic_instrumentation/dd_libraries/python/)

[Unified Service Tagging | Datadog](https://docs.datadoghq.com/getting_started/tagging/unified_service_tagging/)
