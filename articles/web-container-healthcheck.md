---
title: apache, nginx のヘルスチェック用エンドポイント設定
emoji: 🎃
type: tech
topics:
  - Nginx
  - Apache
  - Kubernetes
published: true
published_at: 2023-12-23
---
# はじめに
PodのProbe時に適切なパスがなくて困ったので、まとめます。
Nginx やApacheのヘルスチェック用エンドポイントをとりあえず作っておくための設定です。

# 問題
Pod のProbeを改めて設定しようと思った時に、StartupProbe やLivenessProbeの本来の目的を考慮し、HealthCheck用のエンドポイントがあった方がいいという結論に至りました。

しかし、既存環境にはエンドポイントがなかったので、修正しました。
# 解決方法
Apache, Nginx それぞれの設定ファイルに、数行追記するだけです。
記載する場所によって処理順序が異なると思うので、そこだけ注意です。

## Apache 
```apache
RewriteRule "/healthz" - [R=200]
```
## Nginx
```nginx
location /healthz {
  access_log off;
  return 204;
  break;
}
```
# おわりに
これを追加しておけば、Probe でweb コンテナの状態を簡単に監視できます。

# 参考
[AWS ALBでnginxのヘルスチェックを設定する #AWS - Qiita](https://qiita.com/7CIT/items/363e69806de54438f561)
[mod\_rewrite - Apache HTTP Server Version 2.4](https://httpd.apache.org/docs/2.4/mod/mod_rewrite.html#page-header)