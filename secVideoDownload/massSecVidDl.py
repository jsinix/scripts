#!/usr/bin/python

# Disclaimer: This script is only for educational purposes.
# Please use this at your own risk.
# Author: jsinix(jsinix.1337@gmail.com)

# This script can be used to download the SecTalks indexed here:
# https://github.com/PaulSec/awesome-sec-talks
# Reference:
# http://stackoverflow.com/questions/3041986/python-command-line-yes-no-input
# https://github.com/nficano/pytube
# http://code.activestate.com/recipes/578284-youtube-playlist-parserextractor/

import urllib2, re, signal
from pytube import YouTube
from pprint import pprint
import sys, unicodedata
import urlparse
from BeautifulSoup import BeautifulSoup

def secYTLinks():
    awesomeSecTalks = "http://github.com/PaulSec/awesome-sec-talks"
    rawPage = str(urllib2.urlopen(awesomeSecTalks).read())
    soup = BeautifulSoup(rawPage)
    playlistLinks = []
    directLinks = []
    for tag in soup.findAll('a', href=True):
        currTag = urlparse.urljoin(awesomeSecTalks, tag['href'])
        #tag['href'] = urlparse.urljoin(awesomeSecTalks, tag['href'])
        #currTag = tag['href']
        if 'youtube' in currTag:
            if 'playlist?list' in currTag:
                playlistLinks.append(unicodedata.normalize('NFKD', currTag).encode('ascii','ignore'))
    return playlistLinks

playlists = secYTLinks()
vidListFinal = []

def getPLUrls(url):
    sTUBE = ''
    cPL = ''
    amp = 0
    final_url = []
    if 'list=' in url:
        eq = url.index('=') + 1
        cPL = url[eq:]
        if '&' in url:
            amp = url.index('&')
            cPL = url[eq:amp]
    else:
        print "Incorrect Playlist"
        exit(1)
    try:
        sTUBE = str(urllib2.urlopen(url).read())
    except urllib.error.URLError as e:
        print e.reason
    tmp_mat = re.compile(r'watch\?v=\S+?list=' + cPL)
    mat = re.findall(tmp_mat, sTUBE)
    if mat:
        if mat[0] == mat[1]:
            mat.remove(mat[0])
        for PL in mat:
            yPL = str(PL)
            if '&' in yPL:
                yPL_amp = yPL.index('&')
            final_url.append('http://www.youtube.com/' + yPL[:yPL_amp])
        i = 0
    else:
        print "No videos found."
        sys.exit()
    return final_url

def downloadVideo(url):
    try:
        yt = YouTube(url)
        vidName = str(yt.filename)
        allVidFormat = yt.get_videos()
        higMp4Res = str(yt.filter('mp4')[-1]).split()[-3]
        print "\n(+) Name: %s" %vidName
        print "(+) URL: %s" %url
        print "(+) Resolution: %s" %higMp4Res
        video = yt.get('mp4', higMp4Res)
        userAnswer = raw_input('(+) Want to download?[y/n] ').lower()
        if userAnswer == 'n' or userAnswer == 'N':
           print "(+) Skipping"
        if userAnswer == 'y' or userAnswer == 'Y':
            print "(+) Downloading video"
            video.download('.')
            print "(+) Download complete"
    except Exception as e:
        print "(-) Error: %s" %e

def signal_handler(signal, frame):
    print('\n(-) I quit,  You pressed Ctrl+C\n')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
for eachPL in playlists:
    eachVidList = getPLUrls(eachPL)
    vidListFinal = vidListFinal + eachVidList
vidListFinalUnique = list(set(vidListFinal))
print "(+) Total videos: %s" %len(vidListFinalUnique)
userAnswer = raw_input('(+) Start download?[y/n] ').lower()
if userAnswer == 'n' or userAnswer == 'N':
    print "(+) Exiting"
    sys.exit()
for eachVid in vidListFinalUnique:
    downloadVideo(eachVid)
