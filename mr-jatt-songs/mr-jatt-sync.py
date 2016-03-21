#!/usr/bin/python2.7
import requests, re, urllib2, os, urllib
from BeautifulSoup import BeautifulSoup
import dropbox, signal, sys, argparse

def get_dnld_link(inurl):
    try:
        all_dl_links = []
        req = requests.get(inurl)
        mysoup = BeautifulSoup(req.content)
        interest_objs = mysoup.findAll("a", {"class": "touch"})
        for objx in interest_objs:
	    if 'kbps' in str(objx.text):
	        all_dl_links.append(str(objx.get('href')))
        return all_dl_links[-1]		
    except Exception as err:
	error = err

def subpage_parse(inurl):
    try:
	song_dict = {}
        req = requests.get(inurl)
        mysoup = BeautifulSoup(req.content)
        interest_objs = mysoup.findAll("a", {"class": "touch"})
        for objx in interest_objs:
            if "Top 20" not in str(objx):
	        song_name = str(objx.text.split(' ', 1)[1]) 
	        song_url = str(objx.get('href'))
		song_dict[song_name] = song_url
        return song_dict
    except Exception as err:
	error = err

def dbox_sync(filein):
    try:
	dbox_api = "=================-Token-Here-================="
	# Go here: https://www.dropbox.com/developers
	# API v2 > Dropbox API > Full Dropbox
        client = dropbox.client.DropboxClient(dbox_api)
        filename = filein.split('/')[-1]
        print "(+) Transferring %s to dropbox" %filename
        f = open(filein, 'rb')
        response = client.put_file('/Mr-Jatt/'+filename, f)
    except Exception as err:
	error = err
	print "(-) Cannot transfer %s" %filename

def dlsong(inurl):
    try:
	#inurl = inurl.replace(" ", "%20")
        dir_to_save = "/mnt/storage/media/Songs/Mr-Jatt/"
        file_name = inurl.split('/')[-1]
        full_file_path = dir_to_save+str(file_name)
	inurl = inurl.replace(" ", "%20")
        if os.path.exists(full_file_path) == False:
	    print "(+) Downloading %s" %file_name
	    print "(=) %s" %inurl
            dlhandle = urllib2.urlopen(inurl)
	    data = dlhandle.read()
	    with open(full_file_path, "wb") as code:
	        code.write(data)
	    dbox_sync(full_file_path, )
        else:
	    print "(=) %s already exist" %file_name
	    print "(=) %s" %inurl
    except Exception as err:
	error = err
	print "(-) Download failed %s" %err
	print "(-) %s" %inurl

def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

def controller():
    signal.signal(signal.SIGINT, signal_handler)
    all_urls = ['http://mr-jatt.com/punjabisong-top20-singletracks.html', 'http://mr-jatt.com/punjabisongs-top20.html', 'http://djgaa.com/hindisongs-top20.html']
    glob_dict = {}
    dir_to_save = "/mnt/storage/media/Songs/Mr-Jatt/"
    print "(+) All songs will be saved under %s" %dir_to_save 
    print "(+) Generating all song URL's"
    for urlx in all_urls:
        glob_dict.update(subpage_parse(urlx))
    print "(+) Total songs on website: %s" %len(glob_dict)
    for sname, surl in glob_dict.iteritems():
	try:
	    dl_linkx = get_dnld_link(surl)
            print "(+) %s" %sname
	    dlsong(str(dl_linkx))
	    print "\n"
	except Exception as err:
	    print "(-) %s failed" %sname


def process_arguments(args):
    parser = argparse.ArgumentParser(description="CLI tool to sync songs from mr-jatt.com to dropbox")
    parser.add_argument('-d',
                        '--dbox',
                        help="Just send a song to dropbox"
                        )
    parser.add_argument('-r',
                        '--run',
			action='store_true',
                        help="Run the full script"
                        )
    options = parser.parse_args(args)
    return vars(options)
if len(sys.argv) < 2:
    process_arguments(['-h'])
userOptions = process_arguments(sys.argv[1:])

if userOptions["run"] == True:
    controller()
    sys.exit()
elif userOptions["dbox"] != None:
    sname = userOptions["dbox"]
    if os.path.exists(sname) == True:
	dbox_sync(sname)    
    else:
	print "(-) Filename doesnot exist, recheck"
	sys.exit()
