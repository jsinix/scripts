#!/usr/bin/python
# encoding=utf8

import urllib2, xmltodict
import os, sys, signal

base = "/mnt/storage/media/podcast/"

urlmap = {'secweekly': 'http://podcast.securityweekly.com/rss', 'defsecurity': 
'http://www.defensivesecurity.org/feed/podcast', 'brakingsec': 
'http://www.brakeingsecurity.com/rss', 'datadrisec': 
'http://podcast.datadrivensecurity.info/feed/ddsec-feed.xml', 
'owaspsec': 'http://feeds.soundcloud.com/users/soundcloud:users:63303345/sounds.rss', 
'riskybus': 'http://risky.biz/feeds/risky-business', 'hacknaked': 
'http://hntvaudio.swsgtv.libsynpro.com/rss', 'eswaudio': 
'http://eswaudio.swsgtv.libsynpro.com/rss'}

pcastname = {'secweekly': 'Security Weekly', 'defsecurity': 'Defensive Security', 'brakingsec': 
'Braking Security', 'datadrisec': 'Data Driven Security', 'owaspsec': 'OWASP 24x7', 'riskybus': 
'Risky Business', 'hacknaked': 'Hack Naked', 'eswaudio': 'Enterprise Security Weekly'}

def dload(urlin, base):
    print "(+) CHDIR %s" %base
    os.chdir(base)
    filename = urlin.split('/')[-1]
    fullname = base+'/'+filename
    if os.path.exists(fullname) == False:
        print "(+) Downloading: %s" %filename
        print "(+) URL: %s" %urlin
        dlhandle = urllib2.urlopen(urlin)
        data = dlhandle.read()
        with open(fullname, "wb") as code:
            code.write(data)
    else:
        print "(-) %s already exist" %filename

def rssparser(pcast):
    linkarr = []
    file = urllib2.urlopen(urlmap.get(pcast))    
    data = file.read()
    file.close()
    data = xmltodict.parse(data)
    if pcast == 'secweekly':
	for i in xrange(0, len(data['rss']['channel']['item'])):
	    try:	
	        linkarr.append(data['rss']['channel']['item'][i]['link'])
	    except Exception as err:
		error = err
    else:
	for i in xrange(0, len(data['rss']['channel']['item'])):
	    try:
		linkarr.append(data['rss']['channel']['item'][i]['enclosure']['@url'])
	    except Exception as err:
		error = err	
    return linkarr

def controller():
    for eachpcast in urlmap.keys():
        print "(+) Podcast: %s" %pcastname.get(eachpcast)
        dir = base + eachpcast
        pcastlink = rssparser(eachpcast)

        if os.path.isdir(dir) == False:
	    try:
	        os.makedirs(dir)
	        print "(+) Directory created: %s" %dir
	    except Exception as err:
	        print "(-) %s" %err
 
        for each in pcastlink:
            try:
                dload(each, dir)
	    except Exception as err:
	        print err
        print "\n\n"

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
controller()
