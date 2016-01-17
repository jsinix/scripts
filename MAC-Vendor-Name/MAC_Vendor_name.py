#!/usr/bin/python
import urllib

# Disclaimer: This script is only for educational purposes.
# Please use this at your own risk.
# Author: jsinix(jsinix.1337@gmail.com) 

#This tiny piece of code resolves the MAC address to its vendor. 
def Get_Vendor(macaddr):
    connection = urllib.urlopen("http://api.macvendors.com/"+macaddr)
    output = connection.read()
    connection.close()
    return output

my_mac = "xx:xx:xx:xx:xx:xx"
print Get_Vendor(my_mac)
