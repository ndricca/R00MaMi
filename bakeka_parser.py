import re
import requests
import pandas as pd
import xml.etree.ElementTree as ET
import datetime
import urllib2
from xml.dom import minidom
from bs4 import BeautifulSoup as BS
from numpy import genfromtxt

with open('bakeka_store.msg', 'rb') as f:
    old_df = pd.read_msgpack(f.read())
old_df['pubdate'] = pd.to_datetime(old_df['pubdate'],infer_datetime_format=True)
old_max = max(old_df['pubdate'])

def getxmlcontent(url):
    r = requests.get(url)
    return r.content

def striplink(link):
    strippedlink = re.search("^(.*)\?", link).group(1)
    return strippedlink

def getvaluesBS(beautiful_soup, html_attrval, html_el = "div", html_attr = "class", html_attrval2=None):
    if html_attrval2 is None:
        val = beautiful_soup.findAll(html_el,{html_attr : html_attrval})
    else:
        val = beautiful_soup.find(html_el,{html_attr : html_attrval})[html_attrval2]
    return val

base_url = 'http://milano.bakeca.it/rss20-offro-camera.xml'
bakeka_res = getxmlcontent(base_url)
bakeka_etree = ET.fromstring(bakeka_res)
bk_dict = {}

for j,item in enumerate(bakeka_etree.findall('.//channel/item')):
    pubdate = item.find('pubDate').text
    pubtime = datetime.datetime.strptime(pubdate.replace(" +0200","",1),"%a, %d %b %Y %H:%M:%S")
    if old_max > pubtime :
        print "annuncio n. {} risultato: {}".format(j+1,"vecchio")
        pass
    else:
        title = item.find('title').text
        link = striplink(item.find('link').text)
        try:
            soup = BS(getxmlcontent(link), "lxml")
            block_content = soup.findAll("div", {"class": "bk-dett-block-content"})
            # block_content = getvaluesBS(soup, html_attrval="bk-dett-block-content")
            description = block_content[1].get_text().replace("\t", "").replace("\r", "").replace("\n", "")
            # print description
            details = block_content[0]
            labels = getvaluesBS(details, "bk-dett-meta-label", "strong")
            values = getvaluesBS(details, "bk-dett-meta-value", "span")
            labs = []
            vals = []
            for l in labels:
                labs.append(unicode(str(l.get_text().strip())).replace("&nbsp", "").encode('utf-8'))
            for v in values:
                vals.append(
                    v.get_text().strip().encode('utf-8').replace("\xe2\x82\xac", "euro").replace("\xc2\xb2", "q"))
            if 'Inserzionista:' in labs:
                k = labs.index('Inserzionista:')
                type_offer = vals[k]
            else:
                type_offer = "-"
            if 'Affitto:' in labs:
                k = labs.index('Affitto:')
                price = vals[k]
            else:
                price = "-"
            if 'Classe energetica:' in labs:
                k = labs.index('Classe energetica:')
                energy_class = vals[k]
            else:
                energy_class = "-"
            if 'Quartiere:' in labs:
                k = labs.index('Quartiere:')
                neighbourhood = vals[k]
            else:
                neighbourhood = "-"
            try:
                address = getvaluesBS(soup, html_attr="id", html_attrval="googlemap", html_attrval2="data-bk-address")
                geo_coord = getvaluesBS(soup, html_attr="id", html_attrval="googlemap",
                                        html_attrval2="data-bk-geolocation")
            except:
                address = "-"
                geo_coord = "-"
            try:
                phone = getvaluesBS(soup, "bk-dett-contacts-telefoni bk-hidden").text.strip().replace("\n", " ")
            except:
                phone = "-"
            lst = [title, link, pubdate, description.encode('utf-8').strip(), phone, price, geo_coord,
                   address.encode('utf-8'),
                   neighbourhood, energy_class.encode('utf-8'), type_offer.encode('utf-8')]
            bk_dict[j] = lst
            print "annuncio n.{}, risultato: {}".format(j + 1, "ok")
            # print bk_dict[j]
        except:
            description = "-"
            phone = "-"
            price = "-"
            geo_coord = "-"
            address = "-"
            neighbourhood = "-"
            energy_class = "-"
            type_offer = "-"
            print j
            lst = [title, link, pubdate, description, phone, price, geo_coord, address,
                   neighbourhood, energy_class, type_offer]
            bk_dict[j] = lst
            print "annuncio n.{}, risultato: {}".format(j + 1, "errore")

new_df = pd.DataFrame.from_items(bk_dict.items(),
                             orient="index",
                             columns=["title", "link", "pubdate", "description", "phone", "price", "geo_coord",
                                      "address","neighbourhood", "energy_class", "type_offer"])
new_df['pubdate'] = pd.to_datetime(new_df['pubdate'],infer_datetime_format=True)

df = old_df.append(new_df,ignore_index=True)
#print "\n\n#####\n\n"
#print df['pubdate']

store = df.to_msgpack('bakeka_store.msg')


'''
import re
import requests
import pandas as pd
import xml.etree.ElementTree as ET
import datetime
from bs4 import BeautifulSoup as BS


base_url = 'http://milano.bakeca.it/rss20-offro-camera.xml'

def getxmlcontent(url):
    r = requests.get(url)
    return r.content

def striplink(link):
    strippedlink = re.search("^(.*)\?", link).group(1)
    return strippedlink


def getvaluesBS(beautiful_soup, html_attrval, html_el = "div", html_attr = "class", html_attrval2=None):
    if html_attrval2 is None:
        val = beautiful_soup.findAll(html_el,{html_attr : html_attrval})
    else:
        val = beautiful_soup.find(html_el,{html_attr : html_attrval})[html_attrval2]
    return val


bakeka_res = getxmlcontent(base_url)
bakeka_etree = ET.fromstring(bakeka_res)

bk_dict = {}

for j,item in enumerate(bakeka_etree.findall('.//channel/item')):
    title = item.find('title').text
    link = striplink(item.find('link').text)
    pubdate = item.find('pubDate').text
    try:
        soup = BS(getxmlcontent(link), "lxml")
        block_content = soup.findAll("div", {"class": "bk-dett-block-content"})
        #block_content = getvaluesBS(soup, html_attrval="bk-dett-block-content")
        description = block_content[1].get_text().replace("\t", "").replace("\r", "").replace("\n", "")
        #print description
        details = block_content[0]
        labels = getvaluesBS(details, "bk-dett-meta-label", "strong")
        values = getvaluesBS(details, "bk-dett-meta-value", "span")
        labs = []
        vals = []
        for l in labels:
            labs.append(unicode(str(l.get_text().strip())).replace("&nbsp", "").encode('utf-8'))
        for v in values:
            vals.append(v.get_text().strip().encode('utf-8').replace("\xe2\x82\xac", "euro").replace("\xc2\xb2", "q"))
        if 'Inserzionista:' in labs:
            k = labs.index('Inserzionista:')
            type_offer = vals[k]
        else:
            type_offer = "-"
        if 'Affitto:' in labs:
            k = labs.index('Affitto:')
            price = vals[k]
        else:
            price = "-"
        if 'Classe energetica:' in labs:
            k = labs.index('Classe energetica:')
            energy_class = vals[k]
        else:
            energy_class = "-"
        if 'Quartiere:' in labs:
            k = labs.index('Quartiere:')
            neighbourhood = vals[k]
        else:
            neighbourhood = "-"
        try:
            address = getvaluesBS(soup, html_attr="id", html_attrval="googlemap", html_attrval2="data-bk-address")
            geo_coord = getvaluesBS(soup, html_attr="id", html_attrval="googlemap", html_attrval2="data-bk-geolocation")
        except:
            address = "-"
            geo_coord = "-"
        try:
            phone = getvaluesBS(soup, "bk-dett-contacts-telefoni bk-hidden").text.strip().replace("\n", " ")
        except:
            phone = "-"
        lst = [title,link,pubdate,description.encode('utf-8').strip(),phone,price,geo_coord,address.encode('utf-8'),
           neighbourhood,energy_class.encode('utf-8'),type_offer.encode('utf-8')]
        bk_dict[j] = lst
        print "annuncio n.{}, risultato: {}".format(j+1,"ok")
        #print bk_dict[j]
    except:
        description = "-"
        phone = "-"
        price = "-"
        geo_coord = "-"
        address = "-"
        neighbourhood = "-"
        energy_class = "-"
        type_offer = "-"
        print j
        lst = [title, link, pubdate, description, phone, price, geo_coord,address,
               neighbourhood, energy_class, type_offer]
        bk_dict[j] = lst
        print "annuncio n.{}, risultato: {}".format(j + 1, "errore")

df = pd.DataFrame.from_items(bk_dict.items(),
                             orient="index",
                             columns=["title", "link", "pubdate", "description", "phone", "price", "geo_coord",
                                      "address","neighbourhood", "energy_class", "type_offer"])

#print df.head()
print "dimensions: {}".format(df.shape)
print "\n\n\n"
print "head: {}".format(df.head(1))
print "\n\n\n"
print "summary: {}".format(df.describe(include='all'))
print "\n\n\n"
print "average price: {}".format(df['price'].mean)


store = df.to_msgpack('bakeka_store.msg')


with open('bakeka_store.msg', 'rb') as f:
    old_df = msgpack.unpackb(f.read())

print old_df[]

'''