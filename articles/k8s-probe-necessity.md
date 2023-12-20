---
title: Kubernetes Pod Probe の種類と必要性
yaml_title: k8s-probe-necessity
created: 2023-12-20 14:41:40
updated: 2023-12-20 15:12:56
tags: 
aliases: 
emoji: 💭
published: true
published_at: 2023-12-21
topics:
  - Kubernetes
  - Probe
  - ArgoCD
type: tech
---
# はじめに

Kubernetes の Pod Probe を導入するか迷ったので、改めてその種類や必要性について整理します。

> 元々導入済みだが、環境移行のタイミングで各種定義の棚卸しがしたかった
# 解説

Probe は全部で 3 種類。

- Startup Probe
- Liveness Probe
- Readiness Probe
コンテナ毎に設定が可能で、Probe に失敗した場合も再起動などもコンテナ単位 (Pod ではなく) で行われる。
## Startup Probe

他の Probe を開始しても問題がないか検知するための Probe.

アプリケーションの起動が完了するまでに、最大 5 分間までの猶予を与えることができる。

この間、他の Probe は実行されないため、起動時間が長く Liveness Probe だけではうまく調整が効かない場合に有用。

### 必要性

Liveness Probe, Readiness Probe など、他の Probe を設定する場合は、予期しない Probe の失敗を防ぐために、設定した方が良い。

### 設定例

基本的には、Liveness Probe と同じ設定で良い。

```yaml
startupProbe:
  httpGet:
    path: /healthz
    port: liveness-port
  failureThreshold: 30
  periodSeconds: 10
```

## Liveness Probe

コンテナを再起動するタイミングを検知するための Probe.

アプリケーションプロセス自体は上がっているが、デッドロックや何らかの要因により、処理が停止しているような状態のコンテナを検知することができる。

### 必要性

バグなどによる処理停止を検知できるため、基本的に入れた方が良い。

これがないと、応答しなくなったアプリケーションの再起動が走らないため、アプリケーションの可用性に影響が出てしまう。

### 設定例
```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: liveness-port
  failureThreshold: 1
  periodSeconds: 10
```
## Readiness Probe

コンテナにトラフィックを流すことができるか確認するための Probe.

この Probe に失敗している間は、Service などからのトラフィックが当該コンテナに振り分けられなくなる。

### 必要性

準備ができていないアプリケーションにトラフィックを流すことがなくなるため、基本的に入れた方が良い。

これを入れていない場合、アプリケーション起動時など、一時的にトラフィックを処理できないタイミングでトラフィックを送ってしまうと、正常に処理できず、全体のアプリケーションの信頼性に悪影響を及ぼしてしまう。

### 設定例
```yaml
readinessProbe:
  exec:
    command:
    - cat
    - /tmp/healthy
  initialDelaySeconds: 5
  periodSeconds: 5
```

# おわりに

Probe に関しては、基本的に全て入れておいた方が良さそうでした。

ArgoCD にもヘルスチェックのような機能があるのですが、そちらは Kubernetes リソースのステータス監視がメインとなっていて、コンテナの状態監視とは違った領域をカバーしていました。

# 参考

[Liveness Probe、Readiness ProbeおよびStartup Probeを使用する | Kubernetes](https://kubernetes.io/ja/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
