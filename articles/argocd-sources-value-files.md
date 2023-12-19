---
title: ArgoCD で Multiple Sources を利用してHelm のvalueFiles を指定する方法
emoji: 🌟
type: tech
topics:
  - ArgoCD
  - Kubernetes
  - Helm
published: true
published_at: 2023-12-20
---
# はじめに
ArgoCD のApplication をマニフェストファイルで定義しているときに、source としてhelm を使いながら、values をファイルで定義する方法が分かりずらかったので、まとめます。

# 問題
下記のように、helm の定義でvalueFiles を使ってValueを定義したかったのですが、これだとうまくいきませんでした。
この設定だと、repoURL で指定しているリポジトリのファイル階層を辿ってしまいます。
```yaml
# ...
  sources:
  - repoURL: https://argoproj.github.io/argo-helm
    targetRevision: 0.9.1
    chart: argocd-image-updater
    helm:
      releaseName: argocd-image-updater
      valueFiles:
      - ./path/to/file/values.yaml
```

# 解決方法
下記のように、source を複数定義して、ref を使って`$repo`で参照してあげると、うまくいきます。
```yaml
# ...
  sources:
  - repoURL: https://argoproj.github.io/argo-helm
    targetRevision: 0.9.1
    chart: argocd-image-updater
    helm:
      releaseName: argocd-image-updater
      valueFiles:
      - $repo/path/to/file/values.yaml
  - repoURL: https://github.com/ORG/REPOSITORY.git
    targetRevision: main
    ref: repo
```
# おわりに
ちょっと手こずったので、誰かの参考になればと思い、まとめておきました。
valueObject で定義してもいいのですが、数が多い場合はvalueFiles を使うと便利だと思います。

# 参考
[Multiple Sources for an Application - Argo CD - Declarative GitOps CD for Kubernetes](https://argo-cd.readthedocs.io/en/stable/user-guide/multiple_sources/#helm-value-files-from-external-git-repository)