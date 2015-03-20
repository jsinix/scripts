# The series, 11 + 22 + 33 + ... + 1010 = 10405071317.
# Find the last ten digits of the series, 11 + 22 + 33 + ... + 10001000.
# Answer: 9110846700

#!/usr/bin/python
sqareCollector = []
total = 0

def squareOf(numbr1):
    return numbr1**numbr1
for each1 in range(1,1001):
    sqr1 = squareOf(each1)
    sqareCollector.append(sqr1)
for each2 in sqareCollector:
    total = total + each2

print str(total)[-10:]
