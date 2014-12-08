#!/usr/bin/python

result = []

for i in range(999, 100, -1):
    for j in range(999, 100, -1):
	res = i*j
	if str(res) == str(res)[::-1]:
		result.append(res)

print max(result) 
