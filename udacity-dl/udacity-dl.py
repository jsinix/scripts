#!/usr/bin/python2.7
import requests, signal, os, sys, urllib2
from BeautifulSoup import BeautifulSoup

base_url = "https://www.udacity.com/courses/all"
base_storage = "/mnt/storage/media/Udacity/"

def dl_file(dl_url, dl_path):
    try:
	dl_fname = dl_url.split('/')[-1]
	dl_file_path = dl_path+dl_fname
        if os.path.exists(dl_file_path) == False:
	    print "(-) Downloading %s" %dl_fname
	    print "(-) %s" %str(dl_url)
            dlhandle = urllib2.urlopen(str(dl_url))
	    data = dlhandle.read()
	    with open(dl_file_path, "wb") as code:
	        code.write(data)
        else:
	    print "(-) %s already exist" %dl_fname
	    print "(-) %s" %dl_url
    except Exception as err:
	error = err
	print "(~) Download failed %s" %err
	print "(~) %s" %dl_url

def gen_dl_links(dl_page):
    try:
        dl_dict = {}
        req = requests.get(dl_page)
        mysoup = BeautifulSoup(req.content)
        for tag in mysoup.findAll('a', href=True):
            if '.zip' in str(tag):
	        dl_url = str(tag['href'])
	        dl_name = dl_url.split('/')[-1]
  	        dl_dict[dl_name] = dl_url
        return dl_dict
    except Exception as err:
	print "(~) Error generating files dl links"

def all_cs_courses(urlin):
    try:
        req = requests.get(urlin)
        mysoup = BeautifulSoup(req.content)
        courses = mysoup.findAll("div", {"class": "col-sm-9"})
        course_dict = {}
        for course in courses:
            course_url = str(course.findAll('a')[0].get('href'))
            course_name =  str(course.findAll('a')[0].text)
            if 'cs' in course_url.split('--')[-1]:
                #print "%s : %s" %(course_name, course_url)
                course_dict[course_name] = 'https://www.udacity.com'+course_url
        return course_dict
    except Exception as err:
	print "(~) Error generating all courses"

def gen_dl_page(curlin):
    try:
        pad_left = "https://www.udacity.com/wiki/" 
        pad_right = "/downloads"
        dl_url = pad_left+curlin.split('--')[-1]+pad_right
        return dl_url
    except Exception as err:
	print "(~) Error generating course dl link" 

def controller():
    all_course_index = all_cs_courses(base_url)
    for cname, clink in all_course_index.iteritems():
        print "(+) Course name: %s" %cname
        print "(-) Course link: %s" %clink
        cdllink = gen_dl_page(clink) 
        print "(-) Course dl: %s" %cdllink
        cdetail = gen_dl_links(cdllink)
        print "(-) Total Files: %s" %len(cdetail)    
	cdir = cname.replace (" ", "_")

	if os.path.isdir(base_storage+cdir) == False:
	    os.makedirs(base_storage+cdir)
	    print "(-) Directory %s created" %(base_storage+cdir)
	else:
	    print "(-) Directory %s exist" %(base_storage+cdir)
	
	for fname, furl in cdetail.iteritems():
	    dl_file(furl, base_storage+cdir+'/')	
        print "\n"

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    controller()
