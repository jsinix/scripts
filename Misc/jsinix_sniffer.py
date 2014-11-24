#!/usr/bin/python
#This is sniffer that captures all the possible network traffic 
#including TCP, UDP, ICMP etc. The data field has been commented 
#i.e it will not be printed. Most of the code for this has been 
#referenced from http://www.binarytides.com/python-packet-sniffer-code-linux/
#and https://docs.python.org/2/library/socket.html
import socket, sys
from struct import *

def sniff_tcp():
    t = iph_length + eth_length
    tcp_header = packet[t:t+20]

    #now unpack them :)
    tcph = unpack('!HHLLBBHHH' , tcp_header)

    source_port = tcph[0]
    dest_port = tcph[1]
    sequence = tcph[2]
    acknowledgement = tcph[3]
    doff_reserved = tcph[4]
    tcph_length = doff_reserved >> 4

    print 'SPort: ' + str(source_port) + ' DPort: ' + str(dest_port) + ' Seq Number: ' + str(sequence)  + ' Ack: ' + str(acknowledgement) + ' TCP header length : ' + str(tcph_length)

    h_size = eth_length + iph_length + tcph_length * 4
    data_size = len(packet) - h_size

    #get data from the packet
    data = packet[h_size:]

    #print 'Data : ' + data

def sniff_udp():
    u = iph_length + eth_length
    udph_length = 8
    udp_header = packet[u:u+8]

    #now unpack them :)
    udph = unpack('!HHHH' , udp_header)

    source_port = udph[0]
    dest_port = udph[1]
    length = udph[2]
    checksum = udph[3]

    print 'SPort: ' + str(source_port) + ' DPort: ' + str(dest_port) + ' Length: ' + str(length) + ' Checksum: ' + str(checksum)

    h_size = eth_length + iph_length + udph_length
    data_size = len(packet) - h_size

    #get data from the packet
    data = packet[h_size:]

    #print 'Data : ' + data

def sniff_icmp():
    u = iph_length + eth_length
    icmph_length = 4
    icmp_header = packet[u:u+4]

    #now unpack them :)
    icmph = unpack('!BBH' , icmp_header)

    icmp_type = icmph[0]
    code = icmph[1]
    checksum = icmph[2]

    print 'Type: ' + str(icmp_type) + ' Code: ' + str(code) + ' Checksum: ' + str(checksum)

    h_size = eth_length + iph_length + icmph_length
    data_size = len(packet) - h_size

    #get data from the packet
    data = packet[h_size:]

    #print 'Data : ' + data

def usage():
    print "Usage: .jsinix_sniffer.py -tcp/udp/icmp"

def eth_addr (a) :
    b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(a[0]) , ord(a[1]) , ord(a[2]), ord(a[3]), ord(a[4]) , ord(a[5]))
    return b

try:
    s = socket.socket( socket.AF_PACKET , socket.SOCK_RAW , socket.ntohs(0x0003))
except socket.error , msg:
    print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()


while True:
    argno = len(sys.argv)
    if(argno == 2):
        active_proto = sys.argv[1]
    else:
        active_proto = None

    packet = s.recvfrom(65565)

    packet = packet[0]

    eth_length = 14

    eth_header = packet[:eth_length]
    eth = unpack('!6s6sH' , eth_header)
    eth_protocol = socket.ntohs(eth[2])
    print 'Dst MAC: ' + eth_addr(packet[0:6]) + ' Src MAC: ' + eth_addr(packet[6:12]) + ' Proto: ' + str(eth_protocol)

    if eth_protocol == 8 :
        ip_header = packet[eth_length:20+eth_length]

        iph = unpack('!BBHHHBBH4s4s' , ip_header)

        version_ihl = iph[0]
        version = version_ihl >> 4
        ihl = version_ihl & 0xF

        iph_length = ihl * 4

        ttl = iph[5]
        protocol = iph[6]
        s_addr = socket.inet_ntoa(iph[8]);
        d_addr = socket.inet_ntoa(iph[9]);

        print 'Version: ' + str(version) + ' IP Header Length: ' + str(ihl) + ' TTL: ' + str(ttl) + ' Proto: ' + str(protocol) + ' Src: ' + str(s_addr) + ' Dst: ' + str(d_addr)

        if(active_proto == '-tcp'):
            protocol = 6
        elif(active_proto == '-udp'):
            protocol = 17
        elif(active_proto == '-icmp'):
            protocol = 1

        #TCP protocol
        if protocol == 6 :
            sniff_tcp()

        #ICMP Packets
        elif protocol == 1 :
            sniff_icmp()

        #UDP packets
        elif protocol == 17 :
            sniff_udp()

        #Other IP packet like IGMP
        else :
            print 'Protocol other than TCP/UDP/ICMP'

        print
