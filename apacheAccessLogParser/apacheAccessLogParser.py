#!/usr/bin/python

# Disclaimer: This script is only for educational purposes.
# Please use this at your own risk.
# Author: jsinix(jsinix.1337@gmail.com) 

import urlparse
import sys, argparse

def logParser(ipAddressX, countBitX):
    occurCount = 0
    with open('/var/log/access.log') as f:
        for line in f:
            data = line.split()
            if len(data) > 10:
                if ipAddressX in data[0]:
                    if countBitX == 1:
                        occurCount+=1
                    else:
                        print line
    if countBitX == 1:
        print "Total hits: %s" %occurCount

# Just parsing CLI input
def process_arguments(args):
    parser = argparse.ArgumentParser(description="HTTP Access Log Parser")
    parser.add_argument('-i',
                        '--ip-address',
                        #action='store_true',
                        help="The IP address that access the webpage"
                        )
    parser.add_argument('-c',
                        '--hit-count',
                        action='store_true',
                        help="Total number of hits from the specified IP"
                        )
    options = parser.parse_args(args)
    return vars(options)

if len(sys.argv) < 2:
    process_arguments(['-h'])

userOptions = process_arguments(sys.argv[1:])
ipAddress = userOptions['ip_address']
countOrNot = userOptions['hit_count']
if countOrNot == True:
    countBit = 1
else:
    countBit = 0
logParser(ipAddress, countBit)
