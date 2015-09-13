#!/usr/bin/python

from subprocess import check_output
from netaddr import *
import logging, getpass
import argparse, sys, nmap
from multiprocessing import Pool
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
conf.verb=0
globalInt = ''
vBit = True

def scanUsingNmap(ipAddrIn):
    thisIpAllPortDict = {}
    nm = nmap.PortScanner()
    nm.scan(ipAddrIn, '1-1024')
    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            lport = nm[host][proto].keys()
            lport.sort()
            for port in lport:
                thisPort = port
                thisProduct = nm[host][proto][port]['product']
                thisProto = nm[host][proto][port]['name']
                thisStatus = nm[host][proto][port]['state']
                thisPortArr = [thisProto, thisStatus, thisProduct]
                thisIpAllPortDict[thisPort] = thisPortArr
    return thisIpAllPortDict
    # Returns a dictionary with a list of ports and some details 
    # regarding that port. Here is the structure of the output:
    # {993: ['imap', 'open', 'Dovecot imapd'], 995: ['pop3', 'open', 'Dovecot pop3d'], 
    # 587: ['smtp', 'open', 'Postfix smtpd'], 110: ['pop3', 'closed', ''], 143: ['imap', 
    # 'closed', ''], 80: ['http', 'open', 'Apache httpd'], 465: ['smtp', 'open', 'Postfix smtpd']}

def scanMiddleman(ipArrIn):
    allKeys = ''
    for eachIpInArr in ipArrIn:
        resultOfScan = scanUsingNmap(eachIpInArr)
        for key in resultOfScan:
            allKeys = allKeys + str(key) + ' '
        print "      (*) %s:\t%s" %(eachIpInArr, allKeys)

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
            # Returns all the interfaces the system has
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
        # Returns details like IP address, subnet mask
        # broadcast address, and IPv6 address for the interface
    except Exception as e:
        return None

def ipAddGen(ipAddIn, netMaskIn):
    allHosts = []
    for ip in IPSet([ipAddIn+'/'+netMaskIn]):
        allHosts.append(ip)
    return allHosts
    # Returns a list of all hosts in a particular subnet

def mainFunc(eachIntIn):
    allHostsGen = []
    eachIntDetail = intDetails(eachIntIn)
    if eachIntDetail != None:
        allHostsGen = ipAddGen(eachIntDetail[1], eachIntDetail[4])
    return allHostsGen, eachIntDetail[0]

def arpRequester(returnedHostsIn, currIntIn):
    print "   (-) Sniffing MAC address"
    ansrdHosts = {}
    for eachHost in returnedHostsIn:
        eachHost = str(eachHost)
        # You can increase or decrease the timeout value in the below line
        # FYI if you keep the timeout value high, it will take a lot of
        # time to scan your network depending on your network size.
        try:
            ans, unans = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=eachHost, hwdst='ff:ff:ff:ff:ff:ff'), \ 
            iface=currIntIn, timeout=0.25, inter=0.1)
            for send, rcv in ans:
                if vBit == True:
                    print rcv.sprintf(r"      (*) %Ether.src% is at %ARP.psrc%")
                ansrdHosts[eachHost] = rcv.hwsrc
        except Exception as e:
            print "",
    return ansrdHosts
    # Returns a dictionary with mapping of IP address with corrosponding MAC address

my_user = getpass.getuser()
if(my_user != 'root'):
    print "(-) Run this script as ROOT\n"
    sys.exit()

def controller(userIntInpIn):
    allNixInterfacesX = getNixInterfaces()
    if allNixInterfacesX == None:
        print "   (-) Cannot obtain interfaces"
    try:
        allNixInterfacesX.remove('lo')
    except Exception as e:
        print '   (-) No loopback address to ignore'

    if userIntInpIn not in allNixInterfacesX:
        print "   (-) Interface not found"
        sys.exit()

    globalInt = userIntInpIn
    allNixInterfacesX = [userIntInpIn]
    for eachInt in allNixInterfacesX:
        print "(+) Interface: %s\n" %eachInt
        try:
            returnedHosts, currInt = mainFunc(eachInt)
        except Exception as rHost:
            print "   (-) Exception: %s" %rHost
        try:
            arpRepliedBy = arpRequester(returnedHosts, eachInt)
        except Exception as aReq:
            print "   (-) Exception: %s" %aReq
        print "\n"

    print "   (-) Scanning hosts"
    scanMiddleman(arpRepliedBy)

def process_arguments(args):
    parser = argparse.ArgumentParser(description="Silent network scanner for local subnet. Use it wisely !")

    parser.add_argument('-i',
                        '--interface',
                        required=True,
                        help="Interface name to circle around"
                        )
    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        help="Verbose mode"
                        )
    options = parser.parse_args(args)
    return vars(options)

if len(sys.argv) < 2:
    process_arguments(['-h'])
userOptions = process_arguments(sys.argv[1:])
if userOptions["interface"] != None:
    userIntInp = userOptions["interface"]
if userOptions["verbose"] != True:
    debug = True

controller(userIntInp)
