import re
import urllib2
from xml.dom import minidom
from bs4 import BeautifulSoup
from numpy import genfromtxt


directory = "C:\\Users\\andrea.ricca\\Desktop\\"
base_url = 'http://milano.bakeca.it/rss20-offro-camera.xml'

xmlresponse = urllib2.urlopen(base_url)
http_status = xmlresponse.getcode()
xmlread = xmlresponse.read()
xmldoc = minidom.parseString(xmlread)
# Parse xml nodes:
channel = xmldoc.getElementsByTagName("channel")[0]
items = channel.getElementsByTagName("item")

progress = 0
print "Starting.."

prev = open(directory + 'previous.csv',"a+")

my_data = genfromtxt(directory + 'previous.csv',skip_header=True)


for item in items:
    link = item.getElementsByTagName("link")[0].firstChild.nodeValue
    link_id = re.sub(r'.*\/(\S+)\?.*', r'\1', link)
#    if link_id in set(prev['link_id']):
    if link_id in my_data:
        print "old - %s" % (link_id)
    else:
        print "new - %s" % (link_id)
        prev.write(link_id)

#        new_prev = "%s\n" % (link_id)
#        new_prev.encode('utf-8')
#        prev.write(new_prev)

#prev.to_csv(directory + 'previous.csv',header=True)
#print prev
prev.close()


'''
prev = open(directory + 'previous.csv', "w")
prev.write("link_id \n")

for item in items:
        link = item.getElementsByTagName("link")[0].firstChild.nodeValue
        link_id = re.sub(r'.*\/(\S+)\?.*',r'\1',link)
        raw = "%s\n" % (link_id)
        prev.write(raw)
        progress += 1
        print progress

prev.close()
'''
