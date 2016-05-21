#!/usr/bin/python2.7

#from __future__ import unicode_literals
import requests, datetime, os, youtube_dl
import time, argparse, sys, signal, ssl, re
from BeautifulSoup import BeautifulSoup
now = datetime.datetime.now()

# Change this to where ever you want to 
# store videos. 
base_dir = '/mnt/jsinixcollector/Drama/'

if os.path.isdir(base_dir) == False:
    print "(+) Share not mounted"
    sys.exit()
else:
    bit = 0    

def debuglog(messge):
    logfname = str(time.strftime('%Y-%m-%d-%H-%M-%S'))
    with open("/tmp/drama.log", "a") as myfile:
        myfile.write(logfname+messge)

debuglog(" Script started(drama)\n")

signature = """________       _____       _____        
______(_)_________(_)_________(_)___  __
_____  /__  ___/_  /__  __ \_  /__  |/_/
____  / _(__  )_  / _  / / /  / __>  <  
___  /  /____/ /_/  /_/ /_//_/  /_/|_|  
/___/           jsinix.1337@gmail.com """

# This defines the quality of video to download
ydl_opts = {
    'format': '1',
	'nocheckcertificate': '1',
}

# All the serials that have to be downloaded
alser = ['mereangnemein', 'diyaaurbaatihum', 'saathnibhanasaathiya', 'silsilapyaarka', 'dehleez', 'yehhaimohabbatein', 'kapilsharma', 'comedynightslive', 'yehrishtakyakehlatahai', 'swaragini', 'suhanisiekladki']

alserdict = {'mereangnemein': 'http://www.desiserials.tv/watch-online/star-plus/mere-angne-mein/', 'diyaaurbaatihum': 'http://www.desiserials.tv/watch-online/star-plus/diya-aur-baati-hum-star-plus/', 'saathnibhanasaathiya': 'http://www.desiserials.tv/watch-online/star-plus/saath-nibhana-saathiya-star-plus/', 'silsilapyaarka': 'http://www.desiserials.tv/watch-online/star-plus/silsila-pyaar-ka-star/', 'dehleez': 'http://www.desiserials.tv/watch-online/star-plus/dehleez/', 'yehhaimohabbatein': 'http://www.desiserials.tv/watch-online/star-plus/yeh-hai-mohabbatein-star-plus/', 'kapilsharma': 'http://www.desiserials.tv/watch-online/sony-tv/the-kapil-sharma-show/', 'comedynightslive': 'http://www.desiserials.tv/watch-online/colors/comedy-nights-live/', 'yehrishtakyakehlatahai': 'http://www.desiserials.tv/watch-online/star-plus/yeh-rishta-kya-kehlata-hai-plus/', 'swaragini': 'http://www.desiserials.tv/watch-online/colors/swaragini-tv/', 'suhanisiekladki': 'http://www.desiserials.tv/watch-online/star-plus/suhani-si-ek-ladki-plus/'}

alserdictrev = {'http://www.desiserials.tv/watch-online/star-plus/mere-angne-mein/': 'mereangnemein', 'http://www.desiserials.tv/watch-online/star-plus/diya-aur-baati-hum-star-plus/': 'diyaaurbaatihum', 'http://www.desiserials.tv/watch-online/star-plus/saath-nibhana-saathiya-star-plus/': 'saathnibhanasaathiya', 'http://www.desiserials.tv/watch-online/star-plus/silsila-pyaar-ka-star/': 'silsilapyaarka', 'http://www.desiserials.tv/watch-online/star-plus/dehleez/': 'dehleez', 'http://www.desiserials.tv/watch-online/star-plus/yeh-hai-mohabbatein-star-plus/': 'yehhaimohabbatein', 'http://www.desiserials.tv/watch-online/sony-tv/the-kapil-sharma-show/': 'kapilsharma', 'http://www.desiserials.tv/watch-online/colors/comedy-nights-live/': 'comedynightslive', 'http://www.desiserials.tv/watch-online/star-plus/yeh-rishta-kya-kehlata-hai-plus/': 'yehrishtakyakehlatahai', 'http://www.desiserials.tv/watch-online/colors/swaragini-tv/': 'swaragini', 'http://www.desiserials.tv/watch-online/star-plus/suhani-si-ek-ladki-plus/': 'suhanisiekladki'}

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

def dl_videos(link1, pwdin):
    try:
        if os.path.isdir(pwdin) == True:
            print "(+) Changing PWD: %s" %pwdin
            os.chdir(pwdin)
        else:
            print "(+) Changing PWD: %s" %base_dir
            os.chdir(base_dir)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link1])
    except Exception as ee:
        print "(-) Error downloading this url"

def dl_link(url2, dayz, monz, yearz):
    today_name = []
    today_dl = []
    req2 = requests.get(url2)
    mysoup2 = BeautifulSoup(req2.content)

    for i in xrange(1, 6):
        rawx = mysoup2.findAll('div', {'class': 'post-content bottom'})[0].findAll('p')[i].findAll('a')
        for each in rawx:
            today_name.append([re.sub('&.*?;', '', each.text.encode('ascii')).lower(), each.get('href').encode('ascii')])

    for earr in today_name:
        if dayz in earr[0]:
            if monz in earr[0]:
                if yearz in earr[0]:
                    today_dl.append(earr[1])
    return today_dl

def get_today_episode(url1, dayii, monthii, yearii):
    today_serial = ''
    req1 = requests.get(url1)
    mysoup1 = BeautifulSoup(req1.content)
    all_links_serialx = mysoup1.findAll('div', {'class': 'ten columns omega blog-3'})
    for eachepisode in all_links_serialx:
        name1 = unicode(eachepisode.findAll('div', {'class': 'post bottom'})[0].find('h2').find('a').text).lower()
        link1 = eachepisode.findAll('div', {'class': 'post bottom'})[0].find('h2').find('a').get('href')
	# this will delete html codes from the string
	# e.g. serial express &#8211; 
	# to avoid matching dates like 1 in 10
	name1 = re.sub('&.*?;', '', name1)
	if yearii in name1:
	    if monthii in name1:
		if dayii in name1:
		    today_serial = str(link1)
    return today_serial

def controller(dayi, monthi, yeari):
    signal.signal(signal.SIGINT, signal_handler)
    curr_today_serial = []
    for eserial in alser:
        try:
            curr_today_serial.append([get_today_episode(alserdict.get(eserial), dayi, monthi, yeari), alserdictrev.get(alserdict.get(eserial))])
	except Exception as err:
	    print err

    for epis in curr_today_serial:
	try:
	    if epis:
		print "Serial: %s" %epis[0]
		curlinks = dl_link(epis[0], dayi, monthi, yeari)
                print "Links: %s" %curlinks
		directory = base_dir + epis[1]
                for ednl in curlinks:
		    try:
			dl_videos(ednl, directory)
		    except Exception as err:
			print err
	        print '\n'
	except Exception as err:
	    print "(-) %s %s" %(epis, err)
    debuglog(" Script completed(drama)\n")

# this will save matching patters that 
# are not needed. e.g. date 1 in 10 etc
def dordinal(dayz):
    if 4 <= dayz <= 20 or 24 <= dayz <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][dayz % 10 - 1]
    return suffix

def process_arguments(args):
    parser = argparse.ArgumentParser(description="CLI tool to download Indian Drama's")
    parser.add_argument('-t',
                        '--today',
		        action='store_true',
                        help="Download all serials released today"
                        )
    parser.add_argument('-d',
                        '--date',
                        help="Regex date:month:year"
                        )
    options = parser.parse_args(args)
    return vars(options)
if len(sys.argv) < 2:
    process_arguments(['-h'])
userOptions = process_arguments(sys.argv[1:])

print "\n"
print signature
print '\n'
print " ---------------------------------"
print "| Indian Dramas:                  |" 
print "|  * Mere Angne Mein              |"
print "|  * Diya Aur Baati Hum           |"
print "|  * Saath Nibhana Saathiya       |"
print "|  * Silsila Pyaar Ka             |"
print "|  * Dehleez                      |"
print "|  * Yeh Hai Mohabbatein          |"
print "|  * Yeh Rishta Kya Kehlata Hai   |"
print "|  * Swaragini                    |"
print "|  * Comedy Nights                |"
print "|  * The Kapil Sharma Show        |"
print ' ---------------------------------\n'

if userOptions["today"] == True:
    tday = str(now.day)
    tday = str(tday) + dordinal(int(tday))
    tyear = str(now.year)
    tmonth = time.strftime("%b").lower()
    controller(tday, tmonth, tyear)
    sys.exit()
else:
    if userOptions["date"] != None:
        xday, xmonth, xyear = userOptions["date"].split(':')
        xday = str(xday) + dordinal(int(xday))
        controller(xday, xmonth, xyear)
	sys.exit()

