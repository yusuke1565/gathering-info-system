# static
　このディレクトリには、[templatesディレクトリ](../templates)にある、HTMLのstyleシートを置く場所である。

### style.css
　このファイルの中身について、一部紹介する。<br>
　`.hide`は、文字列などを、穴あきボックスにすることができる。<br>
　`.display-none`は、文字列などを、完全に消すことができる。空いた空白は詰められる。<br>
　`.under`は、文字列などに、赤の下線を引くことが出来る。<br>
　`.radio`や`.botton`は、ラジオボックスとボタンのスタイルを統一するものである。<br>
　これらは、
```HTML:
I have <span class="hide">a</span> pen.
```
という風に使用する。＜span＞で囲い、classに、"hide"や"under"と記述することで、適用される。
