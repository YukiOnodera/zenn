---
title: Spaceliftで実現するIaC自動化のためのポリシー設定ガイド
yaml_title: spacelift-policies-recommended-settings
created: 2024-03-22 15:59:34
updated: 2024-03-22 16:45:19
tags: 
aliases: 
emoji: 🌊
published: true
published_at: 2024-03-25 10:00
topics:
  - Spacelift
  - IaC
  - ChatOps
  - cicd
  - Terraform
type: tech
---

# はじめに

今回は、Spacelift での IaC 自動化を実現するための、おすすめ設定を紹介します。

IaC の自動化を検討している方は、参考にしてみてください。

> Spacelift とは、IaC に特化した CI/CD プラットフォームで、OpenTofu, Terraform, Terragrunt, CloudFormation, Pulumi, Kubernetes, Ansible などのツールに対応しています。

https://spacelift.io/

Terragrunt にも対応してるのは珍しいですよね。

Spacelift では、**Github と連携しながら IaC のプロビジョニングを柔軟に自動化**していくことができます。

# 今回紹介する設定

Spacelift で柔軟な設定をしていくにあたって必要になるのが、**Policy** の設定です。

Spacelift では、Policy の記述に **Rego** という **Policy as Code** の言語が使用されています。

https://www.openpolicyagent.org/docs/latest/policy-language/

今回は Rego で記載された Policy のおすすめ設定を紹介します。

この設定をすることで、**下記のような環境を構築することができる**ようになります。

- main 以外のブランチでは毎回 `plan` 実行
- `plan` の結果は PR のメッセージに投稿
- Github の main ブランチにマージしたら自動で `apply`
- 変更内容に Delete, Update が含まれている場合は手動での承認フェーズに移動
- 承認フェーズに移動した場合は、Slack に通知

**IaC の CI/CD を自動化しつつ、ChatOps も交えた運用しやすい環境に変わる**ので、IaC を導入している環境におすすめです。

# 2 つの Run について

早速本題に入る前に、Policy を作る上で最低限必要な Spacelift での概念があるので、先に紹介しておきます。

それがこちらです。

- Proposed Run
- Tracked Run

Proposed Run は、Terraform でいう `terraform plan` のようなもので、プロビジョニング前にリソースの状態を確認できるコマンドです。

Tracked Run は、Terraform でいう `terraform apply` で、実際にリソースをプロビジョニングします。

> Terraform 以外のツールを使っている場合は、それに準じたコマンドになります。

# Policy の設定

では、早速本題に入っていきます。

まず、今回作成する Policy は 4 つです。

- Plan Policy
- Push Policy
- Notification Policy for Pull Request
- Notification Policy for Slack

## Plan Policy

Plan Policy は、**Plan フェーズで実行される `terraform plan` コマンドなどの後に評価される Policy** です。

下記の設定にすると、`terraform plan` 実行後、変更内容に Delete, Update が含まれているかどうかを評価し、True の場合は手動での承認フェーズに移動するようになります。

```
package spacelift

warn[sprintf(message, [action, resource.address])] {
  message := "action '%s' requires human review (%s)"
  review  := {"update", "delete"}

  resource := input.terraform.resource_changes[_]
  action   := resource.change.actions[_]

  review[action]
}

sample { true }
```

ちなみに、Plan フェーズは Proposed Run, Tracked Run どちらにも含まれるフェーズとなります。

## Push Policy

Push Policy は、**Github から Push や PR 作成の通知が来た時に評価される Policy** となります。

> Github からの通知は、Github App を利用して Spacelift とシームレスに連携できるようになっています。
> ここでの説明は割愛します。

下記の設定にすると、Stack の Project Root に設定したファイルパス配下で変更が発生した場合のみ、Run を実行させることができます。

メインブランチの場合は、Tracked Run, それ以外では Proposed Run が走るような設定にしています。

また、複数のコミットにより QUEUE に Run が溜まっている場合は、不要な Run をキャンセルする記述も入れています。

```
package spacelift

track {
  affected
  input.push.branch == input.stack.branch
}

propose { affected }
propose { affected_pr }

ignore  {
    not affected
    not affected_pr
}
ignore  { input.push.tag != "" }

affected {
    filepath := input.push.affected_files[_]
    startswith(filepath, input.stack.project_root)
}

affected {
    filepath := input.push.affected_files[_]
    glob_pattern := input.stack.additional_project_globs[_]
    glob.match(glob_pattern, ["/"], filepath)
}

affected_pr {
    filepath := input.pull_request.diff[_]
    startswith(filepath, input.stack.project_root)
}

affected_pr {
    filepath := input.pull_request.diff[_]
    glob_pattern := input.stack.additional_project_globs[_]
    glob.match(glob_pattern, ["/"], filepath)
}

# 同じブランチで QUEUE に入っている PROPOSED RUN がある場合、キャンセルして最新のコミットの RUN を優先する
cancel[run.id] {
  run := input.in_progress[_]
  run.type == "PROPOSED"
  run.state == "QUEUED"
  run.branch == input.pull_request.head.branch
}

sample { true }
```

## Notification Policy for Pull Request

Notification Policy は、**Spacelift 上で何らかの通知が発生した場合に、その通知を他のプラットフォームにも通知するように設定できる Policy** です。

こちらの設定にすると、Pull Request のメッセージに `terraform plan` で検知した変更内容を投稿してくれるようになります。

- メッセージ例
![](/images/spacelift-policies-recommended-settings-20240322043555.png)
```
package spacelift

import future.keywords.contains
import future.keywords.if
import future.keywords.in

header := sprintf("### Resource changes ([link](https://%s.app.spacelift.io/stack/%s/run/%s))\n\n![add](https://img.shields.io/badge/add-%d-brightgreen) ![change](https://img.shields.io/badge/change-%d-yellow) ![destroy](https://img.shields.io/badge/destroy-%d-red)\n\n| Action | Resource | Changes |\n| --- | --- | --- |", [input.account.name, input.run_updated.stack.id, input.run_updated.run.id, count(added), count(changed), count(deleted)])

addedresources := concat("\n", added)
changedresources := concat("\n", changed)
deletedresources := concat("\n", deleted)

added contains row if {
  some x in input.run_updated.run.changes

  row := sprintf("| Added | `%s` | <details><summary>Value</summary>`%s`</details> |", [x.entity.address, x.entity.data.values])
  x.action == "added"
  x.entity.entity_type == "resource"
}

changed contains row if {
  some x in input.run_updated.run.changes

  row := sprintf("| Changed | `%s` | <details><summary>New value</summary>`%s`</details> |", [x.entity.address, x.entity.data.values])
  x.entity.entity_type == "resource"

  any([x.action == "changed", x.action == "destroy-Before-create-replaced", x.action == "create-Before-destroy-replaced"])
}

deleted contains row if {
  some x in input.run_updated.run.changes
  row := sprintf("| Deleted | `%s` | :x: |", [x.entity.address])
  x.entity.entity_type == "resource"
  x.action == "deleted"
}

pull_request contains {"commit": input.run_updated.run.commit.hash, "body": replace(replace(concat("\n", [header, addedresources, changedresources, deletedresources]), "\n\n\n", "\n"), "\n\n", "\n")} if {
  input.run_updated.run.state == "FINISHED"
  input.run_updated.run.type == "PROPOSED"
}

sample { true }
```

## Notification Policy for Slack

次に、Slack への通知用 Policy です。

**Stack で承認フェーズ (UNCONFIRMED) が発生した場合のみ、チャンネルに通知を投げてくれます。**

> チャンネル ID は各自必要なものに入れ替えてください。
```
package spacelift
  
slack[{
  "channel_id": "xxxxxx",
  "message": sprintf("http://example.app.spacelift.io/stack/%s/run/%s needs your approval!", [stack.id, run.id]),
}] {
  stack := input.run_updated.stack
  run := input.run_updated.run
  run.type == "TRACKED"
  run.state == "UNCONFIRMED"
}
sample { true }
```

# こちらもおすすめ

https://zenn.dev/yukionodera/articles/good-about-mise

https://zenn.dev/yukionodera/articles/arc-2-released

https://zenn.dev/yukionodera/articles/how-to-manage-images-with-obsidiann

# おわりに

Spacelift を導入すると、ローカルでのコマンド実行や S3 での State ファイル管理、それに伴う権限管理などの運用が不要となり、**IaC での開発が向上**します。

ぜひ参考にしてみてください。
