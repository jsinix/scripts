#!/usr/bin/python

sum = 2
z = 0
x = 1
y = 2
#print x
#print y


while z <= 4000000:
    z = x+y
    x = y 
    y = z
    
    if(z%2 == 0):
	#print z
	sum = sum+z
print sum
