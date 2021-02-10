# 出力ファイル
　このディレクトリは、システムの中でユーザが入力した情報などを記録し保管する場所である。出力ファイルには、2つの.tsvファイルを用いる。

### not_commentary.tsv
　このファイルには、ユーザが解説を**見る前**の解答情報が記されている。中身は、
```bash : not_commentary.tsv
<ID>\t<Nof_times>\t<prob_ID>\t<english>\t<answer>\t<extra>\n
```
となっている。<br>
　＜ID＞は、ユーザIDが入る。<br>
　＜Nof_times>は、何回目の実験かを表す。<br>
　＜prob_ID＞は、問題IDを記す。<br>
　＜english＞には、英文が正しいという意味の`right`。間違っているか分からないという意味の`n_know`（don't know)。間違っているという意味の`error`、のいずれかの値が入る。<br>
　＜answer＞は、ユーザが修正として入力した語句が、そのままここに記録される。入力が無かった場合は、`None`と記録される。<br>
　＜extra＞は、下線部を削除するという意味の`del`。答えが分からいという意味の`n_know`。どちらでもない場合は、`None`となる。<br>

### in_commentary.tsv
　このファイルには、ユーザが解説を**見た後**の解答情報が記されている。中身は、
```bash : in_commentary.tsv
<userID>\t<Nof_times>\t<prob_ID>\t<commentary>\t<english>\t<answer>\t<extra>\n
```
となっている。<br>
　＜commentary＞には、解説の内容が正しいという意味の`right`。内容が間違っているという意味の`error`がある。
