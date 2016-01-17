#!/usr/bin/python

# Disclaimer: This script is only for educational purposes.
# Please use this at your own risk.
# Author: jsinix(jsinix.1337@gmail.com) 

# Do not forget to enable access
# https://www.google.com/settings/security/lesssecureapps

import smtplib, getpass, os, argparse, sys
from tempfile import NamedTemporaryFile
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

# This module is the main email packer that will pack
# all of your headers, body and any attachments that need
# to be sent along with the email.
# Reference: http://kutuma.blogspot.ca/2007/08/sending-emails-via-gmail-with-python.html
def emailSender(usernameIn, passwordIn, fromIn, ToIn, msgIn, subjectIn, attach=None):
    try:
        os.system("clear")
        print "\n\n"
        msg = MIMEMultipart()
        msg['From'] = usernameIn+'@gmail.com'
        msg['To'] = ToIn
        msg['Subject'] = subjectIn
        msg.attach(MIMEText(msgIn))
        if attach != None:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(attach, 'rb').read())
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attach))
            msg.attach(part)
        mailServer = smtplib.SMTP("smtp.gmail.com", 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(usernameIn, passwordIn)
        mailServer.sendmail(usernameIn, ToIn, msg.as_string())
        print "\n\n"
        print "Details".center(20, '+')
        print "\n"
        print "From: %s" % fromIn
        print "To: %s" % ToIn
        print "Subject: %s" % subjectIn
        print "\n"
        print "Message: %s" % msgIn
        print "Attachment: %s" % attach
        mailServer.close()
    except Exception as eErr:
        print "(-) %s" % eErr

# This module will return username and password
# for your gmail account.
def getCredentials(unameIn):
    try:
        rawUser = unameIn
        rawPass = getpass.getpass('(+) Password: ')
        return rawUser, rawPass
    except Exception as credErr:
        print "(-) %s" % credErr
        return None, None

# This module will launch a vim editor from inside
# a program to enter the email body text.
# Reference: https://code.activestate.com/recipes/286238-spawning-an-editor-from-a-script/
def edit(filehandle):
    try:
        editor = os.getenv('EDITOR','vim')
        x = os.spawnlp(os.P_WAIT,editor,editor,filehandle.name)
        if x != 0:
            print "Error opening editor"
        return filehandle.read()
    except Exception as fErr:
        print "(-) %s" % fErr
        return None

# This module will capture all the user input
# that is entered using various arguments.
def process_arguments(args):
    parser = argparse.ArgumentParser(description="Command line email client for Gmail")
    parser.add_argument('-u',
                        '--username',
                        required=True,
                        help="Username for gmail account"
                        )
    parser.add_argument('-r',
                        '--recipient',
                        required=True,
                        help="Recipient email address"
                        )
    parser.add_argument('-s',
                        '--subject',
                        required=True,
                        help="Subject of the email"
                        )
    parser.add_argument('-a',
                        '--attachment',
                        help="Attachment filename"
                        )
    options = parser.parse_args(args)
    return vars(options)

# Print help if the script is run without any
# arguments
if len(sys.argv) < 2:
    process_arguments(['-h'])
userOptions = process_arguments(sys.argv[1:])

if __name__ == '__main__':
    # These lines handle the username and password
    # to login to your gmail account.
    username, password = getCredentials(userOptions["username"])
    if (username == None) or (password == None):
        sys.exit()

    # Capture the subjet for the email
    if userOptions["subject"] != None:
        SUBJECT = userOptions["subject"]

    # Capture the username and sender
    if username[-10:] != '@gmail.com':
        FROM = username+'@gmail.com'
    else:
        FROM = username
        username = username[:-10]

    # Capture the recipient address
    if userOptions["recipient"] != None:
        TO = userOptions["recipient"]

    # Capture the text for the email body
    # Note that vim editor will be opened
    # to get this data
    fd = NamedTemporaryFile()
    TEXT = edit(fd)

    # Send email without an attachment
    if userOptions["attachment"] == None:
        emailSender(username, password, FROM, TO, TEXT, SUBJECT)

    # Send email with an attachment
    else:
        try:
            if os.path.isfile(userOptions["attachment"]) == True:
                emailSender(username, password, FROM, TO, TEXT, SUBJECT, attach = userOptions["attachment"])
        except Exception as err:
            print "(-) %s" % err
