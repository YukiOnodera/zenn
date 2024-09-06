---
title: IaC環境の安全性向上：Checkovを用いたセキュリティチェックの導入方法
yaml_title: feat-checkov
created: 2024-09-04 15:45:44
updated: 2024-09-06 11:00:17
tags: 
aliases: 
emoji: 🌟
published: true
published_at: 2024-09-09 09:00
topics:
  - Security
  - IaC
  - Terraform
type: tech
---
# はじめに

IaC (Infrastructure as Code) のセキュリティ強化を目的として、新たに Checkov という静的解析ツールを導入しました。Checkov は、IaC のセキュリティ脆弱性を検出してくれます。

[https://www.checkov.io/](https://www.checkov.io/)

Checkov が対応しているプラットフォームは以下の通りです。

- **Terraform**
- **CloudFormation**
- **Kubernetes**
- **Helm**
- **ARM Templates**
- **Serverless framework**
- etc.
# 技術選定

IaC のセキュリティ系 CI ツールを選択する際に、いくつかの候補を比較検討した結果、以下の理由から Checkov を選定しました。

- **更新頻度が高いこと**
- **IaC のセキュリティ強化を目的としていること**

Checkov は他のツールと比べて頻繁に更新されており、最新のセキュリティ基準に対応している点がいいなと思いました。

## 選定候補

- CloudSploit
    [https://github.com/aquasecurity/cloudsploit](https://github.com/aquasecurity/cloudsploit)
    Status: Last Updated on Jun. 6
    
- Accurics(Terrascan)
    [https://runterrascan.io/](https://runterrascan.io/)
    [https://github.com/tenable/terrascan](https://github.com/tenable/terrascan)
    Status: Last Updated on Mar. 7
    
- Terrafirma
    [https://github.com/wayfair-archive/terrafirma](https://github.com/wayfair-archive/terrafirma)
    Status: Archived
    
- Checkov
    [https://www.checkov.io/](https://www.checkov.io/)
    Status: Frequently Updated
- Trivy (TFSec)
    [https://github.com/aquasecurity/trivy](https://github.com/aquasecurity/trivy)
    Status: Frequently Updated

# 仕組み

Checkov の実行方法としては、GitHub Actions のような CI/CD ツールの利用も検討しましたが、最終的に https://pre-commit.com/ の仕組みを利用することにしました。

コミット前にコードをチェックすることで、無駄なコミットを防ぎ、ローカル環境での即時修正を可能にするためです。

# 利用方法

コミットを実行すると、pre-commit が作動し、その中で Checkov が実行されます。

チェックが成功すればそのままコミットが実行されますが、問題がある場合はコミットが失敗します。

![](/images/feat-checkov-20240906103628.png)

失敗時には、以下の情報が表示されます。

- 実行されたチェック数
- 成功と失敗の数
- 失敗したチェックの詳細

これに基づいて、問題を修正しましょう。

また、各チェックには詳細なガイド URL も表示されるので、そこから修正方法を確認することができます。

## やむを得ず Check に失敗しているとき

もし、設定が正しく、それでもチェックが失敗している場合は、リソース内に特定のコメントを追加することで、そのリソースの対象チェックをスキップすることが可能です。

```hcl

#checkov:skip=CKV_AWS_000: **スキップする理由(必須)**
```

![](/images/e3f86fd577d09be88b9d62eb6e4e16e7_MD5.jpeg)

## 導入時に Skip したもの

Checkov 導入に伴い、既存のリソースが複数のチェックに引っかかってしまっていたので、理由がわからないものは一時的に全てスキップして、**これらに関しては、今後理由の確認と修正を行なっていく予定です。**

## 設定ファイルによるスキップ管理

すべてのリソースに対して特定のチェックをスキップしたい場合は、Checkov の設定ファイル（`.checkov.yaml`）を利用することをおすすめします。このファイルで、スキップするチェックを指定できます。

- pre-commit 設定例
	```yaml
	...
	- id: tofu_checkov
	args:
	- --args=--config-file __GIT_WORKING_DIR__/.checkov.yaml
	...
	```

- Checkov 設定例
	```.checkov.yaml
	branch: develop
	check:
	  - CKV_DOCKER_1
	compact: true
	directory:
	  - test-dir
	docker-image: sample-image
	dockerfile-path: Dockerfile
	download-external-modules: true
	evaluate-variables: true
	external-checks-dir:
	  - sample-dir
	external-modules-download-path: .external_modules
	framework:
	  - all 
	output: cli 
	quiet: true 
	repo-id: prisma-cloud/sample-repo 
	skip-check: 
	  - CKV_DOCKER_3 
	  - CKV_DOCKER_2 
	skip-framework:
	  - dockerfile
	  - secrets
	soft-fail: true
	```

	https://github.com/bridgecrewio/checkov?tab=readme-ov-file#configuration-using-a-config-file

# こちらもおすすめ

https://zenn.dev/yukionodera/articles/good-about-mise

https://zenn.dev/yukionodera/articles/datadog-asm-protection

https://zenn.dev/yukionodera/articles/how-to-manage-images-with-obsidiann

# おわりに

 IaC にも CI の流れがきているように感じます。

pre-commit や Checkov を利用して、 IaC に関するセキュリティリスクを最小限に抑えましょう。
