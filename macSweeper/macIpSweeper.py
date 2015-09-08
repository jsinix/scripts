#!/usr/bin/python
from subprocess import check_output
from netaddr import *
import logging, getpass
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
conf.verb=0

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
        return None

def intDetails(ifaceIn):
    try:
        ifconfig = check_output(['ifconfig', ifaceIn])
        iface, ip, mac, bcast, nmask, ipv6 = (ifconfig.split()[i] for i in (0, 6, 4, 7, 8, 11))
        ip = ip.split(':')
        bcast = bcast.split(':')
        nmask = nmask.split(':')
        return iface, ip[1], mac, bcast[1], nmask[1], ipv6
    except Exception as e:
        return None

def ipAddGen(ipAddIn, netMaskIn):
    allHosts = []
    for ip in IPSet([ipAddIn+'/'+netMaskIn]):
        allHosts.append(ip)
    return allHosts

def mainFunc(eachIntIn):
    allHostsGen = []
    eachIntDetail = intDetails(eachIntIn)
    if eachIntDetail != None:
        allHostsGen = ipAddGen(eachIntDetail[1], eachIntDetail[4])
    return allHostsGen, eachIntDetail[0]

def arpRequester(returnedHostsIn, currIntIn):
    for eachHost in returnedHostsIn:
        eachHost = str(eachHost)
        # You can increase or decrease the timeout value in the below line
        # FYI if you keep the timeout value high, it will take a lot of
        # time to scan your network depending on your network size.
        try:
            ans, unans = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=eachHost, hwdst='ff:ff:ff:ff:ff:ff'), iface=currIntIn, timeout=0.50, inter=0.1)
            for send, rcv in ans:
                print rcv.sprintf(r"    %Ether.src% is at %ARP.psrc%")
        except Exception as e:
            print "",

my_user = getpass.getuser()
if(my_user != 'root'):
    print "(-) Please run this script as ROOT"
    sys.exit()

def controller():
    allNixInterfacesX = getNixInterfaces()
    if allNixInterfacesX == None:
        print "(-) Cannot obtain interfaces"
    try:
        allNixInterfacesX.remove('lo')
    except Exception as e:
        print '(-) No loopback address to ignore'

    for eachInt in allNixInterfacesX:
        print "(+) Interface: %s" %eachInt
        returnedHosts, currInt = mainFunc(eachInt)
        arpRequester(returnedHosts, eachInt)
        print "\n\n"

controller()
