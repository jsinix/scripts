#!/usr/bin/python
from subprocess import check_output

def getNixInterfaces():
    try:
        with open('/proc/net/dev') as f:
            allInterfaces = []
            for line in f:
                rawIface = line.split()[0]
                if 'Inter' not in rawIface:
                    if 'face' not in rawIface:
                        if ':' in rawIface:
                            allInterfaces.append(rawIface[:-1])
                        else:
                            allInterfaces.append(rawIface)
            return allInterfaces
    except Exception as e:
        print "%s" %e

def intDetails(ifaceIn):
    try:
        ifconfig = check_output(['ifconfig', ifaceIn])
        iface, ip, mac, bcast, nmask, ipv6 = (ifconfig.split()[i] for i in (0, 6, 4, 7, 8, 11))
        ip = ip.split(':')
        bcast = bcast.split(':')
        nmask = nmask.split(':')
        return iface, ip[1], mac, bcast[1], nmask[1], ipv6
    except Exception as e:
        #print "Interface %s: %s" %(ifaceIn, e)
        return None

allNixInterfaces = getNixInterfaces()
for eachInt in allNixInterfaces:
    eachIntDetail = intDetails(eachInt)
    if eachIntDetail != None:
        print "Interface:\t%s\nIP Address:\t%s\nMAC Address:\t%s\nBroadcast:\t%s\nNetmask:\t%s\nIPv6 Address:\t%s\n" \
        %(eachIntDetail[0], eachIntDetail[1],eachIntDetail[2], eachIntDetail[3], eachIntDetail[4], eachIntDetail[5])
