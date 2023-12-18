---
title: 私の Brewfile 管理方法
yaml_title: how-to-manage-brewfile
created: 2023-12-18 14:18:50
updated: 2023-12-18 14:44:03
tags: 
aliases: 
emoji: 🐥
published: true
published_at: 2023-12-19
topics:
  - Homebrew
  - config
  - dotfiles
  - chezmoi
type: tech
---
# はじめに

Brewfile の管理方法について、よく忘れるので、ここに記載してまとめます。

# Brewfile の管理方法

## ファイル作成
```
brew bundle dump
```
## 定期アップデート
```
brew bundle dump -f
```
## インストール
```
brew bundle
```
## Chezmoi で反映

chezmoi で Brewfile を管理している人は、変更を反映しておきましょう。

```
# 差分確認
chezmoi diff
# Chezmoi 反映
chezmoi re-add Brewfile
chezmoi cd
git add . && git commit -m "message" && git push
```

# おわりに

定期的なタスクは忘れがち。まとめられてよかった。

# 参考

[【Homebrew】Homebrewで入れたものをコード化して管理する方法 #homebrew - Qiita](https://qiita.com/terufumi1122/items/542da0faf947eeb258b6)
