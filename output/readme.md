# 出力ファイル
　このディレクトリは、システムの中でユーザが入力した情報などを記録し保管する場所である。出力ファイルには、2つの.tsvファイルを用いる。

### not_commentary.tsv
　このファイルには、ユーザが解説を<font color="RED">見る前</font>の解答情報が記されている。中身は、
```bash : not_commentary.tsv
<userID>\t<実験回数>\t<問題ID>\t<英文の正誤>\t<解答(修正)>\t<削除またはわからない>\n
となっている。
```

### in_commentary.tsv
　このファイルには、ユーザが解説を<font color="RED">見た後</font>の解答情報が記されている。中身は、
```bash : in_commentary.tsv
<userID>\t<実験回数>\t<問題ID>\t<解説文の正誤>\t<英文の正誤>\t<解答(修正)>\t<削除またはわからない>\n
```
となっている。
