---
title: 痒い所に手が届く。開発環境構築ツール mise (旧rtx) の何がいいのか？
yaml_title: good-about-mise
created: 2024-01-25 15:33:58
updated: 2024-01-25 17:16:00
tags: 
aliases: 
emoji: 🕌
published: true
topics:
  - mise
  - asdf
  - rtx
  - development
  - SRE
type: tech
---
# はじめに

年明けに、バージョン管理ツールを asdf から **mise** に乗り換えました。

[Home | mise-en-place](https://mise.jdx.dev/)

ここまで使ってみて、ここが**いいなと思った点**と、**今後使ってみたい機能**などを書いていこうと思います。

> 今後 asdf, direnv の代替ツールとして広がっていく可能性もありそうなツールです。
> 個人的には、ツールの性質からもフロントからインフラまで、様々な人におすすめできます。
# Mise の何がいいのか？

ざっと思い浮かぶところは、こんな感じです。

- asdf と比べて
	- **操作が簡単**
	- **CLI が直感的**
- direnv と比べて
	- `direnv allow` する**手間が省けて楽**
- 既存の設定ファイル群にも**互換性があり導入しやすい**

詳しく書いていきます。

### Asdf と比べて

例えば、asdf で新しいツールを導入するときは、下記のようなコマンドの実行が必要になります。

```sh
asdf plugin add node
asdf install node latest:20
asdf local node latest:20
```

ツールを導入するだけなのに、Plugin 追加して、install して、それを適用して、、、というように、いくつかの工程を踏む必要があります。

mise ではこうです。

```sh
mise use node@20
```

これだけで、Plugin の追加、バージョン Install、config ファイルの更新 (.tool-versions/.mise.toml) まで行ってくれます。

グローバルに適用したい場合は、

```sh
mise use -g node@20
```

オプションをつけるだけ。

**非常に直感的で、扱いやすい**ですよね。

[Dev Tools | mise-en-place](https://mise.jdx.dev/dev-tools/)

### Direnv と比べて

`direnv` だと、値を新しく追加したり更新した時に、

```sh
direnv allow
```

で許可をする必要がありますよね。

mise はわざわざ許可しなくても**自動で環境変数を設定**してくれます。

> ここは好みにもよるかもしれませんが

mise で環境変数を設定するときは、下記のコマンドで追加可能です。

```sh
mise set NODE_ENV=development
```

mise の設定は `.mise.toml` に集約されてるので、そこから一括でツールや環境変数の設定をしても問題ないです。

私は設定ファイルをリポジトリ管理してるので、基本的にコマンドよりもファイルを直接編集することのほうが多かったりします。

[Environments | mise-en-place](https://mise.jdx.dev/environments.html#environments)

### 既存の設定ファイル群にも互換性がある

例えばツールのインストールであれば `.tool-versions` を利用できたり、環境変数の設定も `.mise.toml` から指定すれば `.env` などのファイルが読み込めたりできるようになっています。

なので、**気軽に導入してみて試験的に使ってみることができる**のが mise のいいところだと思います。

[Dev Tools | mise-en-place](https://mise.jdx.dev/dev-tools/)

[Environments | mise-en-place](https://mise.jdx.dev/environments.html#env-directives)

# 今後使ってみたい機能

今気になっている機能は、下記の 3 つです。

- **CI Integration**
- **Tasks**
- **Using env vars in other env vars**

### CI Integration

mise には Github Actions の Workflow である [GitHub - jdx/mise-action](https://github.com/jdx/mise-action) が用意されています。

私は Github Actions を利用することが多いのですが、バージョン管理含めた煩雑な環境構築を、**mise 1 つで解消できる**のはすごくいいなと思いました。

```yaml:Example.yaml
...
- uses: jdx/mise-action@v2
  with:
  version: 2023.12.0 # [default: latest] mise version to install
  install: true # [default: true] run `mise install`
  cache: true # [default: true] cache mise using GitHub's cache
  # automatically write this .tool-versions file
  experimental: true # [default: false] enable experimental features
  tool_versions: |
	shellcheck 0.9.0
  # or, if you prefer .mise.toml format:
  mise_toml: |
	[tools]
	shellcheck = "0.9.0"
- run: shellcheck scripts/*.sh
...
```

[Continuous integration | mise-en-place](https://mise.jdx.dev/continuous-integration.html#github-actions)

### Tasks

まだ Experimental Status ではありますが、mise には Task を定義することのできる機能があります。

`package.json` で定義できるような、コマンドのラッパー的な機能です。

また、ファイルの変更を検知して、**自動で Task を実行**するような機能もあるようです。

この辺りの機能も、今後どこかのタイミングで利用してみたいです。

[Running Tasks | mise-en-place](https://mise.jdx.dev/tasks/running-tasks.html#running-tasks)

### Using Env Vars in other Env Vars

**環境変数の定義に、別の環境変数を利用できる機能**も提供予定となっているそうです。

痒いところに手が届きそうな機能でこちらも今後リリースされたら使ってみたい機能です。

[Environments | mise-en-place](https://mise.jdx.dev/environments.html#using-env-vars-in-other-env-vars)

# おわりに

ここに書いた内容だけでも、十分 mise の恩恵を受けられると思います。

他ツール群との互換性があり導入も簡単なので、**とりあえず入れてみることをおすすめします！**

# 参考

[Home | mise-en-place](https://mise.jdx.dev/)
