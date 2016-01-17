#!/usr/bin/python

# Disclaimer: This script is only for educational purposes.
# Please use this at your own risk.
# Author: jsinix(jsinix.1337@gmail.com) 

import calendar, datetime
import smtplib, errno, sys, re
import string, os, time, urllib2
import requests, feedparser
from bs4 import BeautifulSoup
from pprint import pprint
import unicodedata, xmltodict

def secFocusParser():
    file = urllib2.urlopen('http://www.securityfocus.com/rss/vulnerabilities.xml')
    data = file.read()
    file.close()
    data = xmltodict.parse(data)
    secFocusFinalNews = ""
    pageTitle = data['rss']['channel']['title'] + "\n"
    secFocusFinalNews = secFocusFinalNews + "\n" + pageTitle + "--------------------------------------"
    for eachPubVul in range(5):
        eachTitle = data['rss']['channel']['item'][eachPubVul]['title']
        eachTitle+='\n'
        eachLink = data['rss']['channel']['item'][eachPubVul]['link']
        eachLink+='\n'
        eachDesc = data['rss']['channel']['item'][eachPubVul]['description']
        eachDesc+='\n'
        eachJoinNews = eachTitle + eachLink + eachDesc
        secFocusFinalNews = secFocusFinalNews + "\n" + eachJoinNews
    return secFocusFinalNews

d = feedparser.parse('http://feeds.feedburner.com/TheHackersNews')
rssTitle =  d['feed']['title']
def rssParser(counter):
    concatString = ""
    for i in range(counter):
        title =  d['entries'][i]['title']
        tm_year = d['entries'][i]['published_parsed'].tm_year
        tm_mon = d['entries'][i]['published_parsed'].tm_mon
        tm_mday = d['entries'][i]['published_parsed'].tm_mday
        tm_hour = d['entries'][i]['published_parsed'].tm_hour
        tm_min = d['entries'][i]['published_parsed'].tm_min
        tm_sec = d['entries'][i]['published_parsed'].tm_sec
        dayz = str(tm_year)+'-'+str(tm_mon)+'-'+str(tm_mday)
        timez = str(tm_hour)+':'+str(tm_min)+':'+str(tm_sec)
        newzString = dayz+' '+timez+'  '+title
        origLink = d['entries'][i]['feedburner_origlink']
        concatString = concatString+'\n'+ newzString+'\n - '+origLink+'\n'
    return concatString

thHackNewsTotal = rssTitle + '\n' + rssParser(5)
print thHackNewsTotal + '\n\n' + secFocusParser()
