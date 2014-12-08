#!/usr/bin/python

def sumofsq(n):
    sumofsqs = 0
    for i in range(1,n+1):
	sumofsqs = sumofsqs + (i*i) 
    return sumofsqs
	    	

def sqofsum(n):
    sqofsums = 0
    for j in range(1,n+1):
	sqofsums = sqofsums + j
    return sqofsums*sqofsums

#diff = sumofsq(10) - sqofsum(10)
#print diff   
#print sumofsq(10)
print sqofsum(100) - sumofsq(100)    
