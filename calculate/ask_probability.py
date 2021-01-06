# python3 ask_probability.py
# Calculate probability using 
# accuracy, Number of data and Number of correct answer.
import sys
from xCy import cal_custom

args = sys.argv

acc = args[1]
data = int(args[2])
ask_w_answer = data - int(args[3])
lDM = args[4]
ans = 0
for w_answer in range(0, data+1):
    if w_answer == 0:  # if Nof_wrong_answer is 0.  
        log_cus = 0
    else:
        log_cus = cal_custom(data, w_answer, largeDataMode=lDM)

    if lDM == "ON":
        ans += 10**(log_cus/2) * ((1-float(acc)) ** w_answer) * \
              (float(acc) ** (data - w_answer)) * 10**(log_cus/2)
    else:
        ans += log_cus * ((1-float(acc)) ** w_answer) * \
               (float(acc) ** (data - w_answer))

    if w_answer == ask_w_answer:
        print("number of correct answer ->", data-w_answer, "  probability -> ", ans, "\n")
        break
