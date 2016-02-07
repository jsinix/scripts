#!/usr/bin/python

import requests, re, random, json
from BeautifulSoup import BeautifulSoup, Comment
baseurlclfu = "http://www.commandlinefu.com/commands/browse/"

def getUpperVal(baseurlIn):
    r = requests.get(baseurlIn)
    soup = BeautifulSoup(r.content)
    g_data = soup.find("div", {"class": "pagination"})
    for each in g_data.findAll('a', href=True):
        if 'Last' in str(each):
            upperval = re.findall('browse/(.*?)">', str(each), re.DOTALL)
    return int(upperval[0])

def getCfuCommands():
    finalCommandString = ""
    fivevalues = random.sample(range(1, getUpperVal(baseurlclfu)), 5)
    for eachval in fivevalues:
        currUrl = baseurlclfu + "json/" + str(eachval)
        currresponse = requests.get(currUrl)
        json_data = json.loads(currresponse.text)
        curpagelen = len(json_data)
        curpagerand =  random.sample(range(1, curpagelen), 1)
        currSummary = str(json_data[int(curpagerand[0])].get('summary'))
        currCommand = str(json_data[int(curpagerand[0])].get('command'))
        finalCommandString = finalCommandString + '## ' + currSummary + '\n' + '## ' + currCommand + '\n\n'
    return finalCommandString
    
print getCfuCommands()
