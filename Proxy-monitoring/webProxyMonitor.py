#!/usr/bin/python

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

import urllib2, socket
import smtplib, logging
import logging.handlers
import sys, os
from datetime import datetime
from dateutil import tz

from datetime import datetime
from pytz import timezone
fmt = "%Y-%m-%d %H:%M:%S %Z%z"
now_time = datetime.now(timezone('US/Eastern'))
centralTime = str(now_time.strftime(fmt))

proxyMap = {'$IP': '$Name'}
proxyMapPublic = {'$Name': '$IP'}

urlToHit = "http://www.google.com"
#urlToHit = "http://some-random-domain-name-that-does-not-work-to-test.com"
proxyList = []
badProxy = []
errorOrNotBit = 0
emailBody = """
"""

for key in proxyMap:
    proxyList.append(key)

my_logger = logging.getLogger('wsaLogger')
my_logger.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address = '/dev/log')
my_logger.addHandler(handler)

def is_bad_proxy(pip):
    global emailBody
    try:
        proxy_handler = urllib2.ProxyHandler({'http': pip})
        opener = urllib2.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib2.install_opener(opener)
        req=urllib2.Request(urlToHit)
        sock=urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        text8 = '\tError code: %s' % e.code
        emailBody = emailBody + text8 +'\n'
        return e.code
    except Exception, detail:
        text9 = "\tERROR: %s" % detail
        emailBody = emailBody + text9+'\n'
        return True
    return False

def main():
    global emailBody
    my_logger.critical("The script was run")
    emailBody = emailBody + 'Time Stamp: '+  str(centralTime) + '\n\n'
    text1 = "(+) URL: %s" % urlToHit
    emailBody = emailBody + text1+'\n'
    text2 = ""
    emailBody = emailBody + text2+'\n'
    socket.setdefaulttimeout(120)
    for currentProxy in proxyList:
        currentProxyName = proxyMap[currentProxy]
        text3 = "    (-) Connecting via %s(%s)" %(currentProxyName, currentProxy)
        emailBody = emailBody + text3+'\n'
        currentProxy = currentProxy+':8080'
        if is_bad_proxy(currentProxy):
            text4 = "\t%s is BAD" % (currentProxyName)
            #print text4
            emailBody = emailBody + text4+'\n'
            badProxy.append(currentProxyName)
            text4 = "Proxy - " + currentProxyName +' - '+ text4
            my_logger.critical(text4)
        else:
            text5 = "\t%s is OK" % (currentProxy)
            emailBody = emailBody + text5+'\n'
        text6 = ""
        emailBody = emailBody + text6+'\n'
    print emailBody

if __name__ == '__main__':
    main()
if len(badProxy) == 0:
    sys.exit()

SERVER = '$emailRelayServer' # replace the IP address here of the email relay 
FROM = 'jsinix@jsinix.com'
TO = ['jsinix@jsinix.com']
SUBJECT = 'Proxy Health Check'
TEXT = '\n'+emailBody
message = """\
From: %s
To: %s
Subject: %s

%s
""" % (FROM, ", ".join(TO), SUBJECT, TEXT)

try:
    server = smtplib.SMTP(SERVER)
    server.sendmail(FROM, TO, message)
    server.quit()
except Exception as e:
    print "Error: %s" % e
