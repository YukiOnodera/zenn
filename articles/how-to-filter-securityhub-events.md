---
title: Security Hub の Findings をEvent Bridge でフィルタリングして通知
yaml_title: how-to-filter-securityhub-events
created: 2024-02-06 16:59:13
updated: 2024-02-08 08:09:07
tags: 
aliases: 
emoji: 📌
published: true
published_at: 2024-02-08 11:00
topics:
  - AWS
  - security
  - securityhub
  - Cloudwatch
type: tech
---

# はじめに

Security Hub の Findings を複数の通知先に振り分けるために、**EventBridge Rule のイベントパターンでフィルタリングする方法**を調べました。

# 問題

私が今回やろうとしていたことは、Security Hub に連携している Amazon Inspector の脆弱性の通知の中で、**Package Manager が OS のものだけ通知**する、ということでした。

# 解決方法

そもそもそこまで細かいフィルタリングができるのか不安だったのですが、可能でした。

ASFF 構文に記載のある情報であれば、なんでも フィルタリング可能です。[^page]

方法としては、**EventBridge Rule のイベントパターン**を利用します。

下記は一例ですが、このようなイベントパターンの定義内で、 `<finding content>` の部分に、**Filtering したい属性を JSON 形式で挿入**することでフィルタリング可能になります。

```json
{
   "version":"0",
   "id":"CWE-event-id",
   "detail-type":"Security Hub Findings - Imported",
   "source":"aws.securityhub",
   "account":"111122223333",
   "time":"2019-04-11T21:52:17Z",
   "region":"us-west-2",
   "resources":[
      "arn:aws:securityhub:us-west-2::product/aws/macie/arn:aws:macie:us-west-2:111122223333:integtest/trigger/6294d71b927c41cbab915159a8f326a3/alert/f2893b211841"
   ],
   "detail":{
      "findings": [{
         <finding content>
       }]
   }
}
```
> 上記は一例なので、必要に応じて値を修正してください。
> [Security Hub の EventBridge イベント形式 - AWS Security Hub](https://docs.aws.amazon.com/ja_jp/securityhub/latest/userguide/securityhub-cwe-event-formats.html)

> ちなみに、`findings` が ASFF 構文の冒頭の `Findings` と対応しています。

また、属性の記載方法ですが、**ASFF 構文と同じ構造で記載が必要**になります。

注意点としては、ASSF 構文のままだとエラーになるので、**JSON 形式への変換が必要**になります。

例えば、ASFF 構文のままだと `[{ contents }]` のようにリストの中にオブジェクトを入れているような構造になっているので、`[]` を取ってあげることが必要です。

私の設定はこんな感じになりました。

```json
{
...
	"detail":{
		"findings": {
			"Vulnerabilities" : {
				"VulnerablePackages": {
					"PackageManager": ["OS"]
				}
			}
		}
	}
...
```

## ASFF 構文とは

**AWS Security Finding Format** の略で、Security Hub 上で、**さまざまな AWS サービスやサードパーティ製の製品からの結果を集約、整理する**ために使われている構文。

この構文により、データ変換作業などが不要となる。

## ちなみに

EventBridge のイベントパターンでは、さまざまな比較演算子が利用できるようになっています。

ワイルドカードや `anything-but` などは便利なので、状況によって使い分けると捗ります！

![](/images/how-to-filter-securityhub-events-20240207045237.png)[^1]

# おわりに

ASFF 構文やら EventBridge やら、JSON 読むのはめんどくさいですが、一度構造を理解すれば簡単です。

# こちらもおすすめ

https://zenn.dev/yukionodera/articles/good-about-mise

https://zenn.dev/yukionodera/articles/how-to-manage-dotfiles

https://zenn.dev/yukionodera/articles/how-to-check-cwl-cost

# 参考

https://docs.aws.amazon.com/ja_jp/securityhub/latest/userguide/asff-top-level-attributes.html#asff-vulnerabilities

https://docs.aws.amazon.com/ja_jp/securityhub/latest/userguide/securityhub-cwe-all-findings.html

[^page]: [AWS Security Finding 形式 - AWS Security Hub](https://docs.aws.amazon.com/ja_jp/securityhub/latest/userguide/securityhub-findings-format-syntax.html)
[^1]: https://docs.aws.amazon.com/ja_jp/eventbridge/latest/userguide/eb-event-patterns.html
