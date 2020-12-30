# 入力ファイル
　このディレクトリは、システムへの入力するデータを置いておく場所である。入力には2つの.tsvファイルを用いる。

### question.tsv
　このファイルには、ユーザに問いかける内容を記している。中身は、
```bash:question.tsv
<Phase1のquestion>\t<Phase2のquestion>\t<Phase3のquestion>\t<Phase4のquestion>\t<Phase5のquestion>\n
```
の一文となっている。

### problem.tsv
　このファイルには、ユーザに出題する問題を記している。中身は、
```bash:problem.tsv
<問題ID>\t<英文>\t<解説文>\t<解説対象位置>\n
```
が複数文続いている。<br>
 いま現在のデータについては、datasetにあるexcelファイルの一部である。
