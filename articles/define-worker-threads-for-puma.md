---
title: Rails における DB_POOL や WORKER 数の最適解
yaml_title: define-worker-threads-for-puma
created: 2023-12-21 11:39:01
updated: 2023-12-21 17:47:12
tags: 
aliases: 
emoji: 🐥
published: true
published_at: 2023-12-22
topics:
  - Rails
  - Nginx
  - MySQL
  - Puma
  - Unicorn
type: tech
---
# はじめに

Nginx, Puma or Unicorn, Rails, Sidekiq 環境における DB_POOL, WORKER 数などについて、迷子になることが多いので、整理します。

# 前提知識

本題に入る前に、WORKER 数を設定するためには、CPU コア数について知っておかなければなりません。

答えのみを求める人は、すっ飛ばしてもらって OK.

## 物理コアと論理コア

CPU には、物理コアと論理コアという概念があります。

物理コアとは文字通り、物理的に存在する CPU のコア数です。

論理コアとは、ハイパースレッディング技術などを利用して、物理コアが複数のコアとして動作しているかのように見せる技術により、論理的に利用できるコア数です。

> CPU の世界で出てくるスレッドと、プロセスにおけるスレッドの概念は全く別のものです。
## コア数とプロセスの並列処理

プロセスの最大並列処理数は、物理コア数か論理コア数に依存します。

## コア数と WORKER 数の関係

WORKER 数とは、一般的にミドルウェアの WORKER として動作するプロセス数を表しており、コア数に合わせることが推奨されています。

それ以上の WORKER 数を設定しても、並列処理できず、プロセスの切り替えによるコンテキストスイッチの影響で、システムに悪影響を及ぼす可能性もあります。

しかし、I/O Wait の時間などが非常に多いシステムなどでは、CPU の空き時間が増えるので、その分 WORKER 数をコア数より多くするなどの例外もあります。

また、WORKER 数をコア数に合わせた結果メモリ使用量が逼迫してしまう場合は、WORKER 数を減らすことも検討すると良さそうです。

これらを前提として、冒頭で紹介したミドルウェアの設定値について検討してみます。

# Nginx

まず、Nginx において `worker_processes auto;` が最適解です。

auto 設定だと、コア数に合わせて自動でいい感じに調節してくれます。

# Unicorn

次に Unicorn ですが、こちらも例に漏れず、WORKER_NUM はコア数に合わせましょう。

# Puma

次に Puma ですが、こちらも例に漏れず、WEB_CONCURRENCY はコア数に合わせましょう。

また、Puma はマルチスレッドプロセスなので、スレッド数 `RAILS_MAX_THREADS` の設定も必要になります。

メモリ使用量などと相談しながら、無理のない値を設定しましょう。

> Puma がマルチスレッドマルチプロセスであるのに対して、Unicorn がシングルスレッドマルチプロセスであることは覚えておくと良さそう。
# Rails

Rails では、DB_POOL サイズを設定することができます。

ここで設定した DB_POOL サイズが、プロセス毎に保持する DB 接続数となります。

例えば、WORKER 数が 3 で、DB_POOL が 10 の場合、システム全体では、30 の DB 接続が作成されることとなります。

Puma などのマルチスレッドプロセスを利用している場合は、スレッド数に少し余裕を持たせた値を設定しておくといいでしょう。

また、あまり大きくしすぎると、DB 側の接続数のリミットに引っかかるので注意です。

# Sidekiq

最後に Sidekiq です。

Sidekiq はマルチスレッドシングルプロセス構成を想定します。

> 確か構成によってはマルチプロセスにもできたような気もしますが

この場合に考慮することは、スレッド数と DB_POOL サイズです。

こちらも無理のない値を設定すれば OK。

# おわりに

これで各ミドルウェアの設定をするときに、どのくらいの値が適切かわからず焦ることもなくなりそう。

>ちなみに、プロセスとスレッドの主な違いですが、プロセスは独立したメモリ空間を持つ実行ユニットで、スレッドはプロセスのメモリ空間を共有し軽量な実行パスを提供するユニットであるところにあります。

# 参考
- [Pumaについて深掘りしてみた #Rails - Qiita](https://qiita.com/yusuke2310/items/1695cd702cdf25d34fbc)
- [Sidekiq Enterpriseの同時実行数制御を理解する - Studyplus Engineering Blog](https://tech.studyplus.co.jp/entry/2021/10/25/100000)
