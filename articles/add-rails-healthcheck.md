---
title: Rails に Health Check 用エンドポイントを追加
yaml_title: add-rails-healthcheck
created: 2023-12-28 11:11:34
updated: 2023-12-28 11:30:30
tags: 
aliases: 
emoji: 📝
published: true
published_at: 2023-12-29
topics:
  - Rails
  - Healthcheck
  - Gem
type: tech
---
# はじめに

Rails コンテナの監視用に、Health Check Endpoint が欲しくなったので、追加しました。

候補としては、

- [Rails ver.7.1で導入されたDefaultの機能](https://blog.saeloun.com/2023/02/27/rails-introduces-default-health-check-controller/) を使う
- [okcomputer gem](https://blog.saeloun.com/2023/02/27/rails-introduces-default-health-check-controller/) を導入する

の 2 つが挙がりましたが、今回は okcomputer gem を導入します。

なぜ okcomputer にしたかというと、

- 今回導入予定のアプリケーションは Version が足りていないこと
- okcomputer の方が高機能であること
- Health Check 機能であれば将来的に何か問題が発生しても移行が簡単であること

などの理由があります。

# Okcomputer を導入する

実施した作業手順は下記となります。

1. Gemfile に追記
	```rb
	gem 'okcomputer'
	```
2. bundle install を実行
3. `config/initializers/okcomputer.rb` を追加
	```rb
	OkComputer.mount_at = 'healthz' # Path 変更
	OkComputer.logger = Rails.logger # logger 設定
	```
4. 日本語対応のため、`config/locales/okcomputer_ja.yml` を追加
locale の設定は、[okcomputer.en.yml](https://github.com/sportngin/okcomputer/blob/master/config/locales/okcomputer.en.yml) を参考にしました。

	```rb
	ja:
	  okcomputer:
	    check:
	      passed: "%{registrant_name}: PASSED %{message} (%{time})"
	      failed: "%{registrant_name}: FAILED %{message} (%{time})"
	```

1. 動作確認
`/healthz`,` /healthz/all`, `/healthz/default`, `/healthz/database` などに接続し、正常に動作していることを確認しました。

# おわりに

導入から設定まで、非常に簡単でした。

# 参考

[Rails で利用できる Health Check API 系の Gem である okcomputer について #Rails - Qiita](https://qiita.com/dany1468/items/3b2f9c38d859d0fcd9b2)

[GitHub - sportngin/okcomputer: Provides a health-check endpoint to your Ruby on Rails apps.](https://github.com/sportngin/okcomputer?tab=readme-ov-file#performing-checks)

[rails okcomputer를 이용한 healthcheck url만들기 - Negabaro\`s Blog](https://negabaro.github.io/archive/rails-healthcheck-using-okcomputer)
