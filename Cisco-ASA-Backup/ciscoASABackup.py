#!/usr/bin/python

# Disclaimer: This script is only for educational purposes.
# Please use this at your own risk.
# Author: jsinix(jsinix.1337@gmail.com)

import getpass, subprocess
import pexpect, sys, colorama
import time, random, datetime
import calendar, argparse, os
import shutil, logging, signal
import logging.handlers, tarfile
from colorama import Fore, Back, Style

userMap = {'userID1': 'UserName1', 'userID2': 'UserName2'}
asaBoxesNC = ['ASA1', 'AsA2']
asaBoxesC = ['ASA1', 'AsA2']
asaMap = {'ASA1': '1.1.1.1', 'ASA2': '2.2.2.2'}

timeOut = 160
TIMEOUT = [30, 45]
prefixonall=""
jTerminal = "terminal pager 0"
verboseBit = 2
jssLogger = logging.getLogger('jsLogger')
jssLogger.setLevel(logging.DEBUG)
logHandler = logging.handlers.SysLogHandler(address = '/dev/log')
jssLogger.addHandler(logHandler)
myRunningUser = getpass.getuser()
whoIsRunning = myRunningUser +" : jsS : " +myRunningUser +" started script jss "
my_curr_user = getpass.getuser()

# This function is just to make the execution look
# pretty. Not need to include this is you do not want.
def progressBarProcess(it, prefix = "", size = 60):
    count = len(it)
    def _show(_i):
        x = int(size*_i/count)
        sys.stdout.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), _i, count))
        sys.stdout.flush()
    _show(0)
    for i, item in enumerate(it):
        yield item
        _show(i+1)
    sys.stdout.write("\n")
    sys.stdout.flush()
def progressBarCtl():
    for i in progressBarProcess(range(15), "\t\t\033[1;32m(+)\033[1;m Processing: ", 40):
        time.sleep(0.2)

def countdownTime():
    for i in range(5,-1,-1):
        time.sleep(1)
        sys.stdout.write("\r\t\t\033[1;32m(+)\033[1;m Escaping in %d" % i)
        sys.stdout.flush()
    print "\n"

# This module is used to compress the backup config
def compressAllToOne(fileArr, zippedFileName):
    tar = tarfile.open(zippedFileName, "w:bz2")
    for name in fileArr:
        tar.add(name)
    tar.close()
    print ("\t\t" +Fore.GREEN+ "(+)" +Style.RESET_ALL+ " File successfully compressed")

# Moving the backed up files to a single
# directory. New directory is created for
# every day this script is run.
def fileStorageHandler(filesMoveLocal):
    myCurid = str(getpass.getuser())
    finalStorageDir = "/var/configBackup/"
    if os.path.isdir(finalStorageDir) == False:
        os.makedirs(finalStorageDir)
        print("\t\t" +Fore.GREEN+ "(+) " +Style.RESET_ALL +finalStorageDir +" created")
    jDateStruct = datetime.datetime.now()
    jYear = str(jDateStruct.year)
    jMonth = str(jDateStruct.month)
    jDay = str(jDateStruct.day)
    dirStruct = jYear+"-"+jMonth+"-"+jDay
    currDateDir = str(finalStorageDir)+(dirStruct)
    if os.path.isdir(currDateDir) == False:
        os.makedirs(currDateDir)
        os.chmod(currDateDir, 0777)
        print("\t\t"+Fore.GREEN+ "(+) " +Style.RESET_ALL+ currDateDir + " created")
    for eachFile in filesMoveLocal:
        if os.path.isfile(eachFile) == True:
            shutil.move(eachFile, currDateDir+"/"+eachFile)
            print("\t\t"+Fore.GREEN+ "(+) " +Style.RESET_ALL+"Compressed file moved to " +currDateDir)

# http://stackoverflow.com/questions/9370886/pexpect-if-else-statement 
# http://eli.thegreenplace.net/2010/06/25/aes-encryption-of-files-in-python-with-pycrypto/ 
# http://www.irongeek.com , http://linux.byexamples.com/archives/346/python-how-to-access-ssh-with-pexpect/
def asaConfigBackup(jHostnameIpLocal, jHostnameLocal, jUserLocal, jenpassLocal, enablePassLocal):
    try:
        child = pexpect.spawn ('ssh ' + jUserLocal + '@' + jHostnameIpLocal)
        child.maxread=999999999
        child.delaybeforesend = 0
        argLen = len(sys.argv)

        if argLen > 1:
            if sys.argv[1] == '--debug':
                child.logfile = sys.stdout
            if sys.argv[1] == '-d':
                child.logfile = sys.stdout

        ssh_newkey = 'Are you sure you want to continue connecting'
        i = child.expect([ssh_newkey, '.*assword:.*', pexpect.EOF, pexpect.TIMEOUT], 1)

        if i==0:
            print("\t\t"+Fore.GREEN+ "(+) "+Style.RESET_ALL+ "Accepting SSH keys from " +jHostnameLocal)
            child.sendline('yes')
            i = child.expect([ssh_newkey, '.*assword:.*', pexpect.EOF, pexpect.TIMEOUT], 1)
        elif i==1:
            print("\t\t"+Fore.GREEN+ "(+) "+Style.RESET_ALL+ "Authenticating ")
            child.sendline(jenpassLocal)
            child.sendline("\r")
            child.expect('.*>')
            child.sendline('enable')
            child.expect('.*assword:.*')
            child.sendline(enablePassLocal)
            child.expect(".*# ")
            child.sendline("terminal pager 0")
            child.expect(".*# ")
            child.sendline()
            child.expect (".*# ")

            if jHostnameLocal in asaBoxesNC:
                # Regex to compare standalone device
                boxNameRegex01 = jHostnameLocal[:-4]+".*# "
            else:
                # Regex to check if ASA is in Active/Standby mode
                boxNameRegex01 = jHostnameLocal[:-4]+".*./(act|stby|sec|pri)/(pri|sec|act|stby).*# "

            child.sendline('show run')
            child.expect(boxNameRegex01, timeout=200)
            configlines=child.after.splitlines()
            localFileNamesTemp = []

            # Uncomment the below line to print a progress bar.
            #progressBarCtl()

            # Timestamp for generating backup filename
            epocTime = str(calendar.timegm(time.gmtime()))
            # Filename to save the config
            jFnameLocal = prefixonall+jHostnameLocal+"-RunningConfigBackup-"+epocTime+".TXT"

            f = open(jFnameLocal, 'w')
            f.writelines(["%s\r\n" % line for line in configlines[1:-1]])
            f.close()
            print("\t\t"+Fore.GREEN+ "(+) "+Style.RESET_ALL+ "Saved to " +jFnameLocal)
            child.sendline('exit')
            localFileNamesTemp = []
            localFileNamesTemp.append(jFnameLocal)
            jFnameLocalZip = jFnameLocal+".tar.bz2"
            compressAllToOne(localFileNamesTemp, jFnameLocalZip)
            compressedFileArray = []
            compressedFileArray.append(jFnameLocalZip)
            fileStorageHandler(compressedFileArray)
            os.remove(jFnameLocal)
        elif i==2:
            print "\t"+Fore.GREEN+ "(+) "+Style.RESET_ALL+ "Wrong Password or Unknown Error"

    except Exception as e:
        print "\t"+Fore.GREEN+ "(+) "+Style.RESET_ALL+ "Error: " +str(e)

def help():
    os.system('clear')
    print "Something to display for help"
    signal.alarm(TIMEOUT[0])
    blackHole = raw_input("\n\t\t(+) Press enter to continue ")
    signal.alarm(0)
    starter()

def controller():
    os.system('clear')
    print "\t\t1.  ASA1 \t 2.  ASA2"
    print("\n\t\tPress [" + Fore.GREEN + "H" + Style.RESET_ALL + "]elp for help," + " Press [" + Fore.GREEN + "Q" + Style.RESET_ALL + "]uit to quit" )
    for eachUser in userMap:
        if my_curr_user in userMap:
            print "\n\t\t"+Fore.GREEN+"(+)"+Style.RESET_ALL+" Welcome "+userMap[my_curr_user]
            break
    signal.alarm(TIMEOUT[1])
    jUserOption = raw_input("\t\t" + Fore.GREEN + "(+)" +Style.RESET_ALL + " Select device: ")
    signal.alarm(0)

    if jUserOption=='1':
        asaBoxes = ['ASA1']
    elif jUserOption=='2':
        asaBoxes = ['ASA2']
    elif jUserOption=='q':
        print "\t\t"+Fore.GREEN+ "(+) "+Style.RESET_ALL+ "Quitting"
        sys.exit()
    elif jUserOption=='h':
        help()
        sys.exit()
    else:
        print("\t\t"+Fore.GREEN+ "(+) "+Style.RESET_ALL+ "Wrong choice !")
        print("\t\t"+Fore.GREEN+ "(+) "+Style.RESET_ALL+ "Quitting")
        sys.exit()

    for eachBox in asaBoxes:
        jHostname = eachBox
        jHostnameIP = asaMap.get(eachBox)
        print("\t\t" +Fore.GREEN+ "(+) "+Style.RESET_ALL+ "Connecting to " +jHostnameIP+ "("+jHostname+")")

        jUser = my_curr_user
        # I assume here that the username who ran this command is/will be
        # same as the one on ASA. Ypu may need to change that by either
        # hardcoding the username or ask as input from user.

        print("\t\t"+Fore.GREEN+ "(+) "+Style.RESET_ALL+ "Username: "+jUser)
        signal.alarm(TIMEOUT[1])
        enable5Pass = getpass.getpass("\t\t"+Fore.GREEN+"(+) "+Style.RESET_ALL+ "Enter enable password: ")
        signal.alarm(0)
        signal.alarm(TIMEOUT[1])

        # The below password is login password. Usually in organizations
        # this is done by using combination of PIN+OTP. So that is the reason
        # I asked enable password before this OTP as the OTP will change if
        # wait for the user input for enable password.
        jenpass = getpass.getpass("\t\t"+Fore.GREEN+"(+) "+Style.RESET_ALL+ "Enter user password: ")

        signal.alarm(0)
        asaConfigBackup(jHostnameIP, jHostname, jUser, jenpass, enable5Pass)
    countdownTime()
    globalBlackHole = raw_input("\t\t"+Fore.GREEN+ "(+) "+Style.RESET_ALL+ "Press enter to continue ")

controller()
