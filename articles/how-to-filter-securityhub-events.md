---
title: Security Hub の Findings をEvent Bridge でフィルタリング
yaml_title: how-to-filter-securityhub-events
created: 2024-02-06 16:59:13
updated: 2024-02-06 17:52:06
tags: 
aliases: 
emoji: 📌
published: true
topics:
  - AWS
  - security
  - securityhub
  - Cloudwatch
type: tech
published_at: 2024-02-08 11:00
---

# はじめに

Security Hub の Findings を複数の通知先に振り分けるために、**EventBridge でフィルタリングする方法**を調べました。

# 問題

私が今回やろうとしていたことは、Security Hub に連携している Amazon Inspector の脆弱性の通知の中で、**Package Manager が OS のものだけ通知**する、ということでした。

# 解決方法

ASFF 構文に記載のある情報であれば、なんでも Filtering できます。[^page]

やり方は、EventBridge の Rule Pattern 設定にて、下記の `<finding content>` の部分に、ASFF 構文に従って Filtering したい属性を JSON 形式で挿入するだけです。
> ちなみに、`findings` がASFF構文の冒頭の`Findings`と対応しています。

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

私の設定はこんな感じになりました。

```json
{
...
   "detail":{
      "findings": [{
	        "Vulnerabilities" : [{
				"VulnerablePackages": [
					{
						"PackageManager": "OS"
					}
				]
			}]
       }]
   }
...
```

## ASFF 構文とは

**AWS Security Finding Format** の略で、Security Hub 上で、**さまざまな AWS サービスやサードパーティ製の製品からの結果を集約、整理する**ために使われている構文。

この構文により、データ変換作業などが不要となる。

# おわりに
ASFF 構文やらEventBridge やら、JSON読むのはめんどくさいですが、一度構造を理解すれば簡単です。

# Infra or SRE の方にはこちらもおすすめ

https://zenn.dev/yukionodera/articles/good-about-mise

https://zenn.dev/yukionodera/articles/how-to-check-cwl-cost

# 参考

https://docs.aws.amazon.com/ja_jp/securityhub/latest/userguide/asff-top-level-attributes.html#asff-vulnerabilities

https://docs.aws.amazon.com/ja_jp/securityhub/latest/userguide/securityhub-cwe-all-findings.html

[^page]: [AWS Security Finding 形式 - AWS Security Hub](https://docs.aws.amazon.com/ja_jp/securityhub/latest/userguide/securityhub-findings-format-syntax.html)
