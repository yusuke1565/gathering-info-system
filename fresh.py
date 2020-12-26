with open("_num_file/start_position_prob.txt",
          "w", encoding="utf-8") as f:
    f.write("")

with open("_num_file/of_times.txt",
          "w", encoding="utf-8") as f:
    f.write("")

with open("_num_file/IDnum.txt", "w",
          encoding="utf-8") as f:
    f.write("0")

with open("ex_output/outputA.tsv", "w",
          encoding="utf-8") as f:
    f.write("ID\tNof_times\tprob_num\tenglish\tanswer\textra\n")

with open("ex_output/outputB.tsv", "w",
          encoding="utf-8") as f:
    f.write("ID\tNof_times\tprob_num\tcommentary\tenglish\tanswer\textra\n")

with open("output/not_commentary.tsv", "w",
          encoding="utf-8") as f:
    f.write("ID\tNof_times\tprob_num\tenglish\tanswer\textra\n")

with open("output/in_commentary.tsv", "w",
          encoding="utf-8") as f:
    f.write("ID\tNof_times\tprob_num\tcommentary\tenglish\tanswer\textra\n")
