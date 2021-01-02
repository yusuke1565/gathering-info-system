# 入力ファイル
　このディレクトリは、システムへの入力するデータを置いておく場所である。入力には2つの.tsvファイルを用いる。

### question.tsv
　このファイルには、ユーザに問いかける内容を記している。中身は、
```bash:question.tsv
<Phase1のquestion>\t<Phase2のquestion>\t<Phase3のquestion>\t<Phase4のquestion>\t<Phase5のquestion>\n
```
の一文となっている。

### prob.tsv
　このファイルには、ユーザに出題する問題を記している。グループによって問題を分ける為、少し名前の違ったファイルが3つ用意されている。それぞれの中身は、
```bash:problem.tsv
<問題ID>\t<英文>\t<解説文>\t<解説対象位置>\n
```
が複数文続いている。1行目の問題から順番に出題されるようになっている。<br>
　もし問題を追加したり、減らしたりした場合は、"app.py"の"Namespace"の"max_prob"の値を、問題数の最大値に変更する必要がある。
