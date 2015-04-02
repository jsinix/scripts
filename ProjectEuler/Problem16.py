# 215 = 32768 and the sum of its digits is 3 + 2 + 7 + 6 + 8 = 26.
# What is the sum of the digits of the number 21000?
# Answer: 1366

#!/usr/bin/python
import math

def getPwr(base, power):
    return int(math.pow(base, power))

def summer(num):
    summ = 0
    for i in str(num):
        summ = summ + int(i)
    return summ

print summer(getPwr(2, 1000))
