Question: The following iterative sequence is defined for the set of positive integers:
n → n/2 (n is even)
n → 3n + 1 (n is odd)
Using the rule above and starting with 13, we generate the following sequence:
13 → 40 → 20 → 10 → 5 → 16 → 8 → 4 → 2 → 1
It can be seen that this sequence (starting at 13 and finishing at 1) contains 10 terms. Although it has not been proved yet (Collatz Problem), it is thought that all starting numbers finish at 1.
Which starting number, under one million, produces the longest chain?
NOTE: Once the chain starts the terms are allowed to go above one million.

Answer: found 837799 at length 525

#!/usr/bin/python

def calculate(start):
    count = 1
    while (start != 1):
        if (start%2 == 0):
            start = start/2
        elif (start%2 != 0):
            start = (3*start)+1
        count = count+1
    return count

collector = []
for i in range(13,1000000):
    result = calculate(i)
    collector.append(result)

max_len = max(collector)

for i in range(13,1000000):
        result = calculate(i)
        if result == max_len:
            print "found %s at length %s" %(i, result)
