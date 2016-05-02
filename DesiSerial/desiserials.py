#!/usr/bin/python2.7

#from __future__ import unicode_literals
import requests, datetime, os, youtube_dl
import time, argparse, sys, signal, ssl
from BeautifulSoup import BeautifulSoup
now = datetime.datetime.now()
today_serial = []
today_dl = []

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
all_serials = ['http://www.desiserials.tv/watch-online/star-plus/mere-angne-mein/', 'http://www.desiserials.tv/watch-online/star-plus/diya-aur-baati-hum-star-plus/', 'http://www.desiserials.tv/watch-online/star-plus/saath-nibhana-saathiya-star-plus/', 'http://www.desiserials.tv/watch-online/star-plus/silsila-pyaar-ka-star/', 'http://www.desiserials.tv/watch-online/star-plus/dehleez/', 'http://www.desiserials.tv/watch-online/star-plus/yeh-hai-mohabbatein-star-plus/']

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

def dl_videos(link1):
    # Uncomment this if you want the files to be stored in different directory e.g NAS etc
    #os.chdir('/path/to/directory/')

    #commd = 'youtube-dl -f 1 ' + link1
    #os.system(commd)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	ydl.download([link1])

def dl_link(url2):
    req2 = requests.get(url2)
    mysoup2 = BeautifulSoup(req2.content)
    raw2 = mysoup2.findAll('div', {'class': 'post-content bottom'})[0].findAll('p')[3].findAll('a')
    for each in raw2:
	#print each.get('href')
        today_dl.append(str(each.get('href')))

def get_today_episode(url1, dayii, monthii, yearii):
    req1 = requests.get(url1)
    mysoup1 = BeautifulSoup(req1.content)
    all_links_serialx = mysoup1.findAll('div', {'class': 'ten columns omega blog-3'})
    for eachepisode in all_links_serialx:
        name1 = unicode(eachepisode.findAll('div', {'class': 'post bottom'})[0].find('h2').find('a').text).lower()
        link1 = eachepisode.findAll('div', {'class': 'post bottom'})[0].find('h2').find('a').get('href')
	if yearii in name1:
	    if monthii in name1:
		if dayii in name1:
		    today_serial.append(str(link1))	

def controller(dayi, monthi, yeari):
    signal.signal(signal.SIGINT, signal_handler)
    for eachSerial in all_serials:
        try:
            get_today_episode(eachSerial, dayi, monthi, yeari)
	except Exception as err:
	    print err
    for eachLink in today_serial:
        try:
            dl_link(eachLink)
        except Exception as err:
	    print err
    for elink in today_dl:
	dl_videos(elink)

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
print " ---------------------------"
print "| Indian Dramas:            |" 
print "|  * Mere Angne Mein        |"
print "|  * Diya Aur Baati Hum     |"
print "|  * Saath Nibhana Saathiya |"
print "|  * Silsila Pyaar Ka Star  |"
print "|  * Dehleez                |"
print "|  * Yeh Hai Mohabbatein    |"
print ' ---------------------------\n'

if userOptions["today"] == True:
    day = str(now.day)
    year = str(now.year)
    month = time.strftime("%b").lower()
    controller(day, month, year)
    sys.exit()
else:
    if userOptions["date"] != None:
        day, month, year = userOptions["date"].split(':')
        controller(day, month, year)
	sys.exit()
