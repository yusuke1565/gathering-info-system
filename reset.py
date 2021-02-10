with open("num_file/problem_start_position.txt",
          "w", encoding="utf-8") as f:
    f.write("")

with open("num_file/of_times.txt",
          "w", encoding="utf-8") as f:
    f.write("")

with open("num_file/IDnum.txt", "w",
          encoding="utf-8") as f:
    f.write("0")

with open("ex_output/outputA.tsv", "w",
          encoding="utf-8") as f:
    f.write("ID\tNof_times\tprob_ID\tenglish\tanswer\textra\n")

with open("ex_output/outputB.tsv", "w",
          encoding="utf-8") as f:
    f.write("ID\tNof_times\tprob_ID\tcommentary\tenglish\tanswer\textra\n")

with open("output/not_commentary.tsv", "w",
          encoding="utf-8") as f:
    f.write("ID\tNof_times\tprob_ID\tenglish\tanswer\textra\n")

with open("output/in_commentary.tsv", "w",
          encoding="utf-8") as f:
    f.write("ID\tNof_times\tprob_ID\tcommentary\tenglish\tanswer\textra\n")
