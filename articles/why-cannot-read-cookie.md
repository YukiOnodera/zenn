---
title: document.cookie で cookie が読み込めない原因
yaml_title: why-cannot-read-cookie
created: 2024-01-12 17:59:35
updated: 2024-01-12 18:14:09
tags: 
aliases: 
emoji: 🙌
published: true
published_at: 2024-01-15 11:00
topics:
  - JavaScript
  - Cookie
type: tech
---
# はじめに

JavaScript で、`document.cookie` を使って一部の cookie は取得できるが、session_id など一部の cookie は 取得できないという現象が発生しました。

# 原因

**HttpOnly**属性が cookie に設定されている場合、`document.cookie` を使っても取得することはできません。

なぜなら、HttpOnly 属性が設定された cookie は、ウェブサーバーとブラウザ間での HTTP リクエストとレスポンスでのみ利用が可能になり、 クライアントサイドのスクリプトからは、読み取ったり変更することができなくなるからです。

# 解決方法

**HttpOnly** 属性をなくすことで解決します.

しかし、一般的には session_id などのクッキーには**HttpOnly**属性を付与することが推奨されています.

なぜなら、セッションハイジャック等の危険性があるからです.

# おわりに

**HttpOnly**属性は、ほとんどの場合で設定しておいた方が堅牢な構成になります。

別の手段で代替できないか検討しましょう。

# 参考

[Document.cookie - Web API | MDN](https://developer.mozilla.org/ja/docs/Web/API/Document/cookie)

[HTTP Cookie の使用 - HTTP | MDN](https://developer.mozilla.org/ja/docs/Web/HTTP/Cookies)
