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

import urllib2, re, sys
from pytube import YouTube
from pprint import pprint
import signal

playlists = ['https://www.youtube.com/playlist?list=PLNhlcxQZJSm_gTMJmDNjUcN15HK6-p4H4',
'https://www.youtube.com/playlist?list=PL_IxoDz1Nq2YahR4DU9q5GWsSTle-mETW',
'https://www.youtube.com/playlist?list=PLdIqs92nsIzQvvbTiWLLjZOVE7jPBDomw',
'https://www.youtube.com/playlist?list=PLnwq8gv9MEKj6p8VtgCwFdh8uthLp75M3',
'https://www.youtube.com/playlist?list=PLxyG_Sh7NFechTfZb2DLQEUvy3FbaR3gD',
'https://www.youtube.com/playlist?list=PLsEd7GTJqlRA2M6hwNzxbwPN04pf0F73U',
'https://www.youtube.com/playlist?list=PL02T0JOKYEq52plvmxiJ1cSbwUgHHvP7H',
'https://www.youtube.com/playlist?list=PLtb1FJdVWjUfZ9fWxPPCrOO7LUquB3WrB',
'https://www.youtube.com/playlist?list=PLtb1FJdVWjUfZ9fWxPPCrOO7LUquB3WrB',
'https://www.youtube.com/playlist?list=PLLEf-wPc7TyY6I8AtHvrSEAj3UNjRnpOZ',
'https://www.youtube.com/playlist?list=PLghf5UNZbzG0zLarfwpw4PxPTS0IWo8vB',
'https://www.youtube.com/playlist?list=PLmv8T5-GONwSuEm2XTeIVi6toZ8stS6J2',
'https://www.youtube.com/playlist?list=PLNhlcxQZJSm86xYFgU3fRB84vvii9oAh0',
'https://www.youtube.com/playlist?list=PLn8ut0t_rVT89PJEnacaOYrmRJQc0TeiQ',
'https://www.youtube.com/playlist?list=PLpr-xdpM8wG93dG_L9QKs0W1cD-esQEzU',
'https://www.youtube.com/playlist?list=PLNhlcxQZJSm_tRDcxhP9vldVoJhTkwdnt',
'https://www.youtube.com/playlist?list=PLyHRd2YK1T4ypek_YcnTux1xC_Pu9JZzF',
'https://www.youtube.com/playlist?list=PLeeS-3Ml-rpoNWewUnljPP7QN4USn4c7H',
'https://www.youtube.com/playlist?list=PL_IxoDz1Nq2ZrTckdtMUV4no50_-b9OkL',
'https://www.youtube.com/playlist?list=PLbRoZ5Rrl5lfeRixThHzgGYj1wu80JOh3',
'https://www.youtube.com/playlist?list=PL9fPq3eQfaaBuHqVvDzPoWxznYYmyx5UX',
'https://www.youtube.com/playlist?list=PLH15HpR5qRsXF78lrpWP2JKpPJs_AFnD7',
'https://www.youtube.com/playlist?list=PLNhlcxQZJSm_wpMC42BKPCknT-JhnZGos',
'https://www.youtube.com/playlist?list=PLFvh_k-n27CnvMIYBLGAjQ7ekaC10t9y4',
'https://www.youtube.com/playlist?list=PLNhlcxQZJSm97gwg__BfWirG5NnkAAENL',
'https://www.youtube.com/playlist?list=PLmfJypsykTLX9mDeChQ7fovybwYzQgr6j',
'https://www.youtube.com/playlist?list=PLNhlcxQZJSm87UHyX3fVU_NnSRjM8CUUw',
'https://www.youtube.com/playlist?list=PLNhlcxQZJSm9TV35bUYvhjUpdAR8iPT5R',
'https://www.youtube.com/playlist?list=PLNhlcxQZJSm9zsNKfwujM4JgEk1wOc44m',
'https://www.youtube.com/playlist?list=PLcrUMxzVpi6waVMFpbc2MFrbE5uB_EPJU',
'https://www.youtube.com/playlist?list=PLJ7_KHVHtAm9YhIzWa_2A61dmFv8cTDO2',
'https://www.youtube.com/playlist?list=PLuUtcRxSUZUpQAa54H6PKkfX6A48ruzhh',
'https://www.youtube.com/playlist?list=PLpr-xdpM8wG-ZTcHhFfAeBthNVZVEtkg9',
'https://www.youtube.com/playlist?list=PLUOjNfYgonUuTk1VXx8CgbzCYq6qOGvWf',
'https://www.youtube.com/playlist?list=PLeUGLKUYzh_hr2_j0RNVSD6wZQIhdfoGe',
'https://www.youtube.com/playlist?list=PLEl1NAXHTFNzlKjae0e_-lIktpPeTRR7e',
'https://www.youtube.com/playlist?list=PLKpjtdatAwij7ajFwQSkmxFm43N9U_T3E',
'https://www.youtube.com/playlist?list=PLu1bAtIWt2VbXiy4kNWdtVkWiRWvPoeD6',
'https://www.youtube.com/playlist?list=PLdh5UOMgeDvkWYaZcUrFagUY2zUtfMafR',
'https://www.youtube.com/playlist?list=PLNhlcxQZJSm9EMEAOlWO40tv4A-2JERPb',
'https://www.youtube.com/playlist?list=PLLVBUs9CnYAcaDxfgdjhdHuI5K1CERGhu',
'https://www.youtube.com/playlist?list=PLXoRjc8jI5RQ5Rr--h0BnuYh17fuQyJwv',
'https://www.youtube.com/playlist?list=PLNhlcxQZJSm_by2u3gZUlcPPU0IQtvRTS',
'https://www.youtube.com/playlist?list=PLfouvuAjspToHlyi9rnayB1WXFVmH037C',
'https://www.youtube.com/playlist?list=PLpr-xdpM8wG-xWNB98Q2uLN7O8E91xJzK',
'https://www.youtube.com/playlist?list=PLNhlcxQZJSm-L0fEgmLzf3Rmyt45M5qw0',
'https://www.youtube.com/playlist?list=PLStO1VqVBvmHyVc71QLOCBKugWQyyM7WE',
'https://www.youtube.com/playlist?list=PLSNlEg26NNpzyo5SOikogTjmACDFghLQP',
'https://www.youtube.com/playlist?list=UUIvfe0KAXCjxIXWabrfn2tA',
'https://www.youtube.com/playlist?list=PLpAqWs_9UQkvsUhUy0fYxhwPB7am3FGMU']

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

vidListFinal = []
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
