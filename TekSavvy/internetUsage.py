#!/usr/bin/python

import httplib, json
import smtplib, time

def getUsage():
    APIKEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" # Replace your own key here 
    headers = {"TekSavvy-APIKey": APIKEY}
    conn = httplib.HTTPSConnection("api.teksavvy.com")
    conn.request('GET', '/web/Usage/UsageSummaryRecords?$filter=IsCurrent%20eq%20true', '', headers)
    response = conn.getresponse()
    jsonData = response.read()
    data = json.loads(jsonData)
    pd  = data["value"][0]["OnPeakDownload"]
    pu  = data["value"][0]["OnPeakUpload"]
    opd = data["value"][0]["OffPeakDownload"]
    opu = data["value"][0]["OffPeakUpload"]
    sd  = data["value"][0]["StartDate"]
    ed  = data["value"][0]["EndDate"]
    usageData =  "Start Date: %s  \nEnd Date: %s  \nOn Peak Download: %s  \nOn Peak Upload: %s \nOff Peak Download: %s \nOff Peak Upload: %s" % (sd, ed, pd, pu, opd, opu)
    return usageData

text = getUsage()
logo = '\n\nNote: This is an automated email. This message and any accompanying attachments are intended only for the person(s) to whom this message is addressed and may contain privileged, proprietary and/or confidential information. '
TEXT = text + logo

SERVER = "localhost"
FROM = "jsinix <jsinix@jsinix.com>"
TO = ["Test <test@gmail.com>"]
SUBJECT = "Update | Internet Usage " + (time.strftime("%d:%m:%Y"))
message = """\
From: %s
To: %s
Subject: %s

%s
""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
server = smtplib.SMTP(SERVER)
server.sendmail(FROM, TO, message)
server.quit()
