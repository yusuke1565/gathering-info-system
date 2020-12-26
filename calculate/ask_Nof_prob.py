import sys
from xCy import cal_custom

args = sys.argv

t = args[1]
acc = args[2]
data = int(args[3])
ans = 0
a = 0
for n in range(1, data):
    log_cus = cal_custom(data, n, largeDataMode="ON")
    ans += 10**(log_cus/2) * ((1-float(acc)) ** n) * \
           (float(acc) ** (data - n)) * 10**(log_cus/2)
    if ans >= float(t):
    # if n == 200:
        print("n ->", data-(n-1), "ans -> ", a, "\n")
        print("n ->", data-n, "ans -> ", ans, "\n")
        break
    a = ans
