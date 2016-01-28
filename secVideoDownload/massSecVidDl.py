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
import sys, unicodedata, time
import urlparse, argparse
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
        print "(+) Downloading video"
        start_time = time.time()
        video.download('.')
        print "(+) Download complete"
        print("(+) Download Time: %s sec" % round((time.time() - start_time), 2))
    except Exception as e:
        print "(-) Error: %s" %e

def signal_handler(signal, frame):
    print('\n(-) I quit,  You pressed Ctrl+C\n')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def downloadAllSec():
    playlists = secYTLinks()
    vidListFinal = []
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

def process_arguments(args):
    parser = argparse.ArgumentParser(description="Youtube video download tool")
    parser.add_argument('-l',
                        '--link',
                        #action='store_true',
                        help="Single youtube video to download"
                        )
    parser.add_argument('-p',
                        '--playlist',
                        #action='store_true',
                        help='Youtube playlist url to download all videos'
                        )
    parser.add_argument('-s',
                        '--sec',
                        action='store_true',
                        help='All sec-talk videos'
                        )
    options = parser.parse_args(args)
    return vars(options)
if len(sys.argv) < 2:
    process_arguments(['-h'])
userOptions = process_arguments(sys.argv[1:])

if userOptions["sec"] == True:
    downloadAllSec()
    print "(+) Exiting"
    sys.exit()
if userOptions["playlist"] != None:
    ytpllink = userOptions["playlist"]
    vidList = getPLUrls(ytpllink)
    vidListUnique = list(set(vidList))
    print "(+) Total videos: %s" %len(vidListUnique)
    userAnswer = raw_input('(+) Start download?[y/n] ').lower()
    if userAnswer == 'n' or userAnswer == 'N':
        print "(+) Exiting"
        sys.exit()
    for eachLink in vidListUnique:
        downloadVideo(eachLink)
    print "(+) Exiting"
    sys.exit()
if userOptions["link"] != None:
    vidLink = userOptions["link"]
    downloadVideo(vidLink)
    print "(+) Exiting"
    sys.exit()
