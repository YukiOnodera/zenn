---
title: 超簡単! 遂にGAとなった OpenTofu への移行方法
yaml_title: migrate-to-opentofu
created: 2024-01-18 15:54:34
updated: 2024-01-18 16:12:24
tags: 
aliases: 
emoji: 🤖
published: true
published_at: 2024-01-19 11:00
topics:
  - Terraform
  - OpenTofu
type: tech
---
# はじめに

遂に **OpenTofu が GA** となりました。

**Terraform から OpenTofu に移行する方法**をサクッと紹介します。

# 移行手順
1. **OpenTofu を Install**
[Installing OpenTofu | OpenTofu](https://opentofu.org/docs/intro/install/)
環境に合わせて Install 方法がいくつか提供されていますが、自分は Homebrew で Install しました。
```sh
brew update
brew install opentofu
tofu --version
```
2. **Terraform の Version を更新**
OpenTofu は Terraform の Version1.6 系と互換性があるため、Terraform の Version を上げる必要があります。
```providers.tf
terraform {
required_version = "~> 1.6.0"
required_providers {
...
```
3. **Execute OpenTofu**
```sh
tofu init
tofu plan
```

以上で移行が完了です。

# おわりに

移行作業というと重い作業にも思えますが、**OpenTofu への移行は非常に簡単**でした。

既存の Terraform との互換性もきっちり整備されていて、設定やファイル追加なしでも移行できたのがありがたかったです。

Terraform を v1.6 に上げたいけど、ライセンスの問題などでまだ v1.5.5 を使っているという方は、ぜひこのタイミングで移行しちゃいましょう。

# 参考

[OpenTofu](https://opentofu.org/docs/intro/migration)
