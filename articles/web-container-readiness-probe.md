---
title: web コンテナのReadiness Probe はどこを見ればいいのか
yaml_title: web-container-readiness-probe
created: 2023-12-22 17:32:34
updated: 2023-12-22 17:47:20
tags: 
aliases: 
emoji: 👌
published: true
published_at: 2023-12-24
topics:
  - Apache
  - Nginx
  - Probe
  - Kubernetes
type: tech
---
# はじめに

Nginx や Apache などの web コンテナの ReadinessProbe を設定するときに、どこを監視すれば良いのか迷ったので、まとめます。

# 問題

Kubernetes の Pod Probe でコンテナ監視ができるのですが、web コンテナの Readiness Probe の Health Check 先はどこが適切なのか迷いました。

web コンテナの Health Check 用エンドポイントを見ればいいのか、backend にあるアプリケーションのページを見ればいいのか、など。

# 解決方法

**backend アプリケーションの TOP ページ**などを指定しましょう。

こうすることで、backend のコンテナが障害で落ちた場合に、ReadinessProbe に失敗して web コンテナにトラフィックが流れなくなります。

web コンテナの Health Check 用エンドポイントを ReadinessProbe で監視してしまうと、backend コンテナが落ちた場合でもそれを検知できず、web コンテナまでトラフィックが流れてきてしまいます。

# おわりに

いろんなところに Health Check の設定が存在していて忘れがちだから、整理できてよかった。

# 参考

https://kubernetes.io/ja/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/

https://cstoku.dev/posts/2018/k8sdojo-10/

https://zenn.dev/nekoshita/articles/4e838ae224ed56
