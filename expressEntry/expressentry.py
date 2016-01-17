#!/usr/bin/python

# Disclaimer: This script is only for educational purposes.
# Please use this at your own risk.
# Author: jsinix(jsinix.1337@gmail.com) 

# This script is a quick way to find out whenever there is any change in 
# the express antry draw points. It will send out an email to the interested 
# person. This script is for educational purposes only. I am not liable 
# for any other uses for this. 

import requests, smtplib
from bs4 import BeautifulSoup
import re, time, os, sys

def runCic():
    url = "http://www.cic.gc.ca/english/express-entry/rounds.asp"
    r = requests.get(url)
    matchObj = re.findall(r'<tr>(.*?)</tr>', r.content, re.M|re.I|re.S)
    totalPass = matchObj[1].split()[0][4:][:-4]
    cutOff = int(matchObj[1].split()[6][4:][:-17])
    dateTime = time.strftime("%c")
    return cutOff, totalPass, dateTime

def emailBodyGen():
    finalString = ""
    score3, people3, nowDate3 = runCic()
    finalString = finalString + nowDate3 +"\n"
    finalString = finalString + "Lowest Rank: "+str(score3) + "\n"
    finalString = finalString + "Number of invitations: "+str(people3) + "\n"
    return finalString

def comparison():
    if os.path.isfile('/var/log/lastCutOff.txt'):
        with open('/var/log/lastCutOff.txt') as f:
            content = f.readlines()
            con = content[0]
            score1, people1, nowDate1 = runCic()
            if int(score1) == int(con):
                print "Point has not changed: %s" % score1
                return False, None
            else:
                print "Point changed: %s" % score1
                finalText = emailBodyGen()
                wr = open('/var/log/lastCutOff.txt','w')
                wr.write(str(score1)+'\n')
                wr.close()
                return True, finalText

    else:
        try:
            f = open('/var/log/lastCutOff.txt','w')
            score2, people2, nowDate2 = runCic()
            f.write(str(score2)+'\n')
            f.close()
            print "[+] Creating lastCutOff.txt"
            finalText = emailBodyGen()
            return True, finalText

        except Exception as e:
            print "[-] Unable to create lastCutOff.txt"
            return False, None

TEXT = ""
bit, retrn = comparison()
if bit == False:
    sys.exit()
elif bit == True:
    TEXT = retrn + '\n\nNote: This is an automated email. This message and any accompanying attachments are intended only for the person(s) to whom this message is addressed and may contain privileged, proprietary and/or confidential information. '

subb = "Express Entry | Update"
SERVER = "localhost"
FROM = "secbot <secbot@jsinix.com>"
TO = ["jsinix <jsinix.1337@gmail.com>"]
SUBJECT = subb
message = """\
From: %s
To: %s
Subject: %s

%s
""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
server = smtplib.SMTP(SERVER)
server.sendmail(FROM, TO, message)
server.quit()
