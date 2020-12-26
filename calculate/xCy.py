import sys
import math


def cal_custom(x, y, largeDataMode="OFF"):
    """
    Calculate xCy and return answer.
    If "largeDataMode" is ON, return "log_ans".
    $ xCy = answer = 10^(log_ans) $
    How to use "log_ans" -> 10^(log_ans/2) * (1.0*10^{-13}) * 10^(log_ans/2)
    Can prevent "Over float".
    """
    b = math.log10(int(x))
    c = math.log10(int(y))
    for n in range(1, int(y)):
        b += math.log10(int(x) - n)
        c += math.log10(int(y) - n)
    log_ans = b - c
    if largeDataMode == "ON":
        ans = log_ans
    else:
        ans = 10**(log_ans)
    return ans


if __name__ == "__main__":
    args = sys.argv
    x = args[1]
    y = args[2]
    largeMode = args[3]
    ans = cal_custom(x, y, largeDataMode=largeMode)
    print(x,"C",y,"=",ans)
