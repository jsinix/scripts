#So basicaly what this script does is scrap 
#the address/contact details of a company or 
#something similar, goes through page by page 
#and prints it. These details usualy incluse
#name, addess, phone etc

#!/usr/bin/python
import requests
from bs4 import BeautifulSoup
import re
def jsinix_grabber(uri):
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    links = soup.find_all("a")
    g_data = soup.find_all("div", {"class": "article phone1 "})
    qwerty = []
    for item in g_data:
        items = re.sub('[\n]', '', item.text)
        qwerty.append(items)
    for i in qwerty:
        print "\n" 
        print i
for counter in range(1,10):
    url = "http://www.yellowpages.ca/search/si/"+str(counter)+"/Walmart/Toronto%2C%20ON"
    jsinix_grabber(url)
