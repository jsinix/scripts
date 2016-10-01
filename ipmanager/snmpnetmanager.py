#!/usr/local/bin/python

from socket import inet_aton
import socket, struct
from netaddr import *
import os, sys, time

devices = {'device1': '192.168.0.1'}
ignore = ['0.0.0.0', '127.0.0.1']
database_base = '/tmp/'
dbfile = 'interface.db'
community = 'public'

def get_net_size(netmask):
    binary_str = ''
    for octet in netmask:
        binary_str += bin(int(octet))[2:].zfill(8)
    return str(len(binary_str.rstrip('0')))

def updatedb(idata):
    try:
        with open(database_base+dbfile, "a") as handler:
            handler.write(ientry)
    except Exception as err:
        print "Error: %s" %err

def getnetdetail(ipadr, community):
    command = "snmpwalk -v2c -c " +community + " " + ipadr + " .1.3.6.1.2.1.4.20.1.3"
    netarray = []
    rawres = os.popen(command, 'r')
    while 1:
        line = rawres.readline()
        if not line: break
        if 'ipAdEntNetMask' in line:
            ip = line.split()[0].split('::')[1].replace('ipAdEntNetMask.', '')
            mask = line.split()[-1]
            maskarr = mask.split('.')
            try:
                inet_aton(ip)
                inet_aton(mask)
                cidr = get_net_size(maskarr)
                if not any(x in ip for x in ignore):
                    resip = ip
                    rescidr = cidr
                    resmask = mask
                    netarray.append([resip, resmask, rescidr])
                    #print "%s/%s" %(ip, cidr)
            except Exception as err:
                print "IP Address Or Netmask Invalid\n"
    return netarray

try:
    oldfile = database_base+dbfile
    newfie = oldfile+'-'+str(time.time()).split('.')[0]
    if os.path.isfile(oldfile):
        os.rename(oldfile, newfie)
        print "Old database renamed to %s" %newfie
except Exception as err:
    print err

for device in devices:
    print "Hostname: %s" %device
    inetarray = getnetdetail(devices.get(device), community)
    for each in inetarray:
        ipaddress, subnetmask, cidrmask  = each
        inetaddr = IPNetwork(ipaddress+'/'+str(cidrmask)).network
        print "IP %s in network %s/%s" %(ipaddress, inetaddr, cidrmask)
        ientry = "%s:%s:%s:%s\n" %(device, ipaddress, inetaddr, cidrmask)
        try:
            updatedb(ientry)
        except Exception as err:
            print err
    print "\n"
