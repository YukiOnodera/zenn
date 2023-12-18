---
title: chezmoi を使った dotfiles の管理方法
yaml_title: how-to-manage-dotfiles
created: 2023-12-16 12:56:52
updated: 2023-12-18 14:44:45
tags: 
aliases: 
emoji: 🌊
published: true
topics:
  - dotfiles
  - chezmoi
  - config
  - git
  - github
type: tech
---
# はじめに

私は、chezmoi を使って PC 内の dotfiles を Github で一括管理しています。

[Quick start - chezmoi](https://www.chezmoi.io/quick-start/)

しかし、日々の業務で dotfiles を更新した時に、chezmoi での運用フローを忘れがちなので、ここにまとめます。

# 運用フロー

## Dotfiles を更新したい

まずは差分を確認

```
chezmoi diff
```

問題なければ 更新

```
chezmoi re-add
```

## Dotfiles を Git Push したい

ディレクトリを移動

```
chezmoi cd
```

いつも通り Push する

```
git add . && git commit -m "message" && git push
```

## Dotfiles を新しく追加したい

対象のファイルを追加

```
chezmoi add ~/path/to/file
```

## Dotfiles を削除する

```
chezmoi remove target
```
# おわりに

これで普段の運用が楽になりそう。

chezmoi で dotfiles を管理しておくと、PC の入れ替え時などにかなり役立つので、おすすめです。

# 参考

[Quick start - chezmoi](https://www.chezmoi.io/quick-start/#using-chezmoi-across-multiple-machines)
