#!/usr/bin/python
from urllib2 import urlopen
import time

def get_last_line(fname):
    try:
        with open(fname, 'rb') as fh:
            for line in fh:
                pass
            last = line.strip('\n')
	    return last
    except Exception as err:
        return None

filename = '/var/log/wanip.log' # This is tracking/db file
timestamp = str(int(time.time()))
lastline = str(get_last_line(filename))
print "\n(+) Database IP: %s" %lastline.split()[0] 
my_ip = str(urlopen('http://ip.42.pl/raw').read().strip('\n'))
print "(+) Current IP: %s" %my_ip

if lastline.split()[0] != my_ip:
    print "(+) New IP detected"	
    try:
        fh = open(filename, 'a')
        fh.write(my_ip + ' ' + timestamp)
	print '  IP written: %s\n' %my_ip
    except Exception as err:
	print "  Error: " %err
	print "  Cannot write: %s\n" %my_ip	
else:
    print "(+) IP unchanged\n"
