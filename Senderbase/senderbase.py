#!/usr/bin/python
import urllib2, argparse
import json, sys

baseUrl = "http://api.statdns.com/"
helpMsg = """

SenderBase scores are assigned to IP addresses based on a combination of factors, including email volume and reputation.

Reputation scores in SenderBase may range from -10 to +10, reflecting the likelihood that a sending IP address is trying to send spam. Highly negative scores indicate senders who are very likely to be sending spam; highly positive scores indicate senders who are unlikely to be sending spam.

SenderBase is a designed to help email administrators better manage incoming email streams by providing objective data about the identity of senders. SenderBase is akin to a credit reporting service for email, providing data that ISPs and companies can use to differentiate legitimate senders from spam sources. SenderBase provides objective data that allows email administrators to reliably identify and block IP addresses originating unsolicited commercial email (UCE) or to verify the authenticity of legitimate incoming email from business partners, customers or any other important source. What makes SenderBase unique is that it provides a global view of email message volume and organizes the data in a way that it is easy to identify and group related sources of email. SenderBase combines multiple sources of information to determine a "reputation score" for any IP address. This information includes:

- Email volume information provided by tens of thousands of organizations that regularly receive Internet email
- Spam complaints received by the SpamCop service
- Information on other DNS-based blacklists

Reference: http://www.cisco.com/c/en/us/support/docs/security/email-security-appliance/118380-technote-esa-00.html
"""

def queryDNSmx(urlToParse):
    try:
        ipArr = []
        data = json.load(urllib2.urlopen(urlToParse))
        for eachEntry in range(len(data['answer'])):
            ipArr.append(str(data['answer'][eachEntry]['rdata'].split()[-1]).translate(None, '"'))
        return ipArr
    except Exception as e:
        return None

def queryDNSarec(urlToParse):
    try:
        data = json.load(urllib2.urlopen(urlToParse))
        for eachEntry in range(len(data['answer'])):
            return str(data['answer'][eachEntry]['rdata']).translate(None, '"')
    except Exception as e:
        return None

def returnDomain(simIP):
    ipaddrArrRev = '.'.join(reversed(simIP.split('.')))
    return ipaddrArrRev  + ".rf-adfe2ko9.senderbase.org"

def queryDNS(urlToParse):
    try:
        data = json.load(urllib2.urlopen(urlToParse))
        for eachEntry in range(len(data['answer'])):
            return str(data['answer'][eachEntry]['rdata']).translate(None, '"')
    except Exception as e:
        return None

def process_arguments(args):
    parser = argparse.ArgumentParser(description="Senderbase score query")
    parser.add_argument('-i',
                        '--ip',
                        #required=True,
                        help="IP address to query"
                        )
    parser.add_argument('-d',
                        '--domain',
                        #required=True,
                        help="Domain name to query"
                        )
    parser.add_argument('-w',
                        '--wiki',
                        #required=True,
                        help="Wiki for this tool"
                        )
    options = parser.parse_args(args)
    return vars(options)

if len(sys.argv) < 2:
    process_arguments(['-h'])
userOptions = process_arguments(sys.argv[1:])

if userOptions["ip"] != None:
    userIP = userOptions["ip"]
    sbrsScore = queryDNS(baseUrl + returnDomain(userIP) + "/txt")
    print "IP: %s\tScore: %s" %(userIP, sbrsScore)

if userOptions["domain"] != None:
    userDomain = userOptions["domain"]
    allMX = queryDNSmx(baseUrl + userDomain + "/mx")
    if allMX != None:
        for eachMx in allMX:
            currMxDomain = eachMx
            currMxIp = queryDNSarec(baseUrl + eachMx + "/a")
            currSbrs = queryDNS(baseUrl + returnDomain(currMxIp) + "/txt")
            print "MX: %s\tIP: %s\tScore: %s" %(currMxDomain, currMxIp, currSbrs)

if userOptions["wiki"] != None:
    print helpMsg
    sys.exit()
