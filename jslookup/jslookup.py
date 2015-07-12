# Permission to use, copy, modify and distribute this 
# software and its documentation for any purpose and 
# without fee is hereby granted, provided that the above 
# copyright notice appear in all copies that both 
# copyright notice and this permission notice appear in 
# supporting documentation. jsinix makes no representations 
# about the suitability of this software for any purpose. 
# It is provided "as is" without express or implied warranty.

# jsinix DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, 
# INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. 
# IN NO EVENT SHALL jsinix BE LIABLE FOR ANY SPECIAL, INDIRECT 
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM 
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, 
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN 
# CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

#!/usr/bin/python
import urllib2, json
import sys, argparse

baseUrl = "http://api.statdns.com/"
swichDict = {'aarec': 'aaaa', 'arec': 'a', 'certrec': 'cert', 'dnskeyrec': 'dnskey', 'mxrec': 'mx', 'nsrec': 'ns', 'ptrec': 'ptr', 'soarec': 'soa', 'spfrec': 'spf', 'txtrec': 'txt'}

def queryDNS(domainLocal):
    urlToParse = domainLocal
    try:
        jsonObj = urllib2.urlopen(urlToParse)
        data = json.load(jsonObj)
        for eachEntry in range(len(data['answer'])):
            ttl = data['answer'][eachEntry]['ttl']
            ipRes = data['answer'][eachEntry]['rdata']
            type = data['answer'][eachEntry]['type']
            print "TYPE#~ %s\tDATA#~ %s\tTTL#~ %s" %(type, ipRes, ttl)
    except Exception as e:
        print "(+) %s\n" % e
    print "\n"

def urlGenerator(switchType, domainLocal):
    aUrl = baseUrl + domainLocal + '/a'                         # Get Host Address (A records)
    aaaaUrl = baseUrl + domainLocal + '/aaaa'                   # Get IPv6 Host Address (AAAA records)
    certUrl = baseUrl + domainLocal + '/cert'                   # Get Certificate (CERT records)
    nsUrl = baseUrl + domainLocal + '/ns'                       # Get Name Servers (NS records)
    mxUrl = baseUrl + domainLocal + '/mx'                       # Get Mail Exchange record (MX records)
    dnskeyUrl = baseUrl + domainLocal + '/dnskey'               # Get DNS Key record (DNSKEY records)
    ptrUrl = baseUrl + domainLocal + '.in-addr.arpa' + '/ptr'   # Get Pointer record (PTR records)
    soaUrl = baseUrl + domainLocal + '/soa'                     # Get Start of Authority (SOA record)
    spfUrl = baseUrl + domainLocal + '/spf'                     # Get Sender Policy Framework (SPF records)
    txtUrl = baseUrl + domainLocal + '/txt'                     # Get Text record (TXT records)
    urlArray = {'a': aUrl, 'aaaa': aaaaUrl, 'cert': certUrl, 'ns': nsUrl, 'mx': mxUrl, 'dnskey': dnskeyUrl, 'ptr': ptrUrl, 'soa': soaUrl, 'spf': spfUrl, 'txt': txtUrl}
    if switchType in urlArray:
        return True, urlArray[switchType]
    else:
        return False, None

parser = argparse.ArgumentParser(description='jslookup is a tool similar to nslookup which works over http using an API')
parser.add_argument("-a", help="Get Host Address (A records)")
parser.add_argument("-aa", help="Get IPv6 Host Address (AAAA records)")
parser.add_argument("-crt", help="Get Certificate (CERT records)")
parser.add_argument("-ns", help="Get Name Servers (NS records)")
parser.add_argument("-mx", help="Get Mail Exchange record (MX records)")
parser.add_argument("-dns", help="Get DNS Key record (DNSKEY records)")
parser.add_argument("-ptr", help="Get Pointer record (PTR records)")
parser.add_argument("-soa", help="Get Start of Authority (SOA record)")
parser.add_argument("-spf", help="Get Sender Policy Framework (SPF records)")
parser.add_argument("-txt", help="Get Text record (TXT records)")

if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)
args=parser.parse_args()

def controller(bitX, valueX):
    if bitX == True:
        queryDNS(valueX)
    else:
        print "(+) Unknown record type"

if args.a != None:
    bit, value = urlGenerator('a', args.a)
    controller(bit, value)
if args.aa != None:
    bit, value = urlGenerator('aaaa', args.aa)
    controller(bit, value)
if args.crt != None:
    bit, value = urlGenerator('cert', args.crt)
    controller(bit, value)
if args.dns != None:
    bit, value = urlGenerator('dnskey', args.dns)
    controller(bit, value)
if args.mx != None:
    bit, value = urlGenerator('mx', args.mx)
    controller(bit, value)
if args.ns != None:
    bit, value = urlGenerator('ns', args.ns)
    controller(bit, value)
if args.ptr != None:
    bit, value = urlGenerator('ptr', args.ptr)
    controller(bit, value)
if args.soa != None:
    bit, value = urlGenerator('soa', args.soa)
    controller(bit, value)
if args.spf != None:
    bit, value = urlGenerator('spf', args.spf)
    controller(bit, value)
if args.txt != None:
    bit, value = urlGenerator('txt', args.txt)
    controller(bit, value)
