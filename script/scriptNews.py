#!/usr/bin/env python

import urllib2
import sqlite3
import json

from BeautifulSoup import BeautifulSoup  # available at: http://www.crummy.com/software/BeautifulSoup/

conn = sqlite3.connect("espionage.sqlite")
conn.row_factory = sqlite3.Row

base_url='https://www.moneycontrol.com'

def get_search_results(url):
    req = urllib2.Request(url)
    req.add_header('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13')
    page = urllib2.urlopen(req)
    HTML = page.read()
    return HTML

def scrape_news(text):
    """Scrape the text as HTML, find and parse out all the ads and store them in a database
    """
    soup = BeautifulSoup(text)
    # print soup
    #get the ads on the right hand side of the page
    center = soup.find("div", {"id":"nChrtPrc"})
    basic_info= center.find("div",{"class":"FL gry10"}).findAll(text=True)
    info = ' '.join([word.strip() for word in basic_info]).strip()
    print 'info: '+info
    fls = soup.findAll('div', {'class': 'MT15 PT10 PB10'})
    for fl in fls:
        ads= fl.find('div',{'id':'Moneycontrol/MC_Market/MC_Market_StockPrice_Native_1_div'})
        if ads is None:
            #the header line
            parts = fl.find('strong').findAll(text=True)
            title = ' '.join([word.strip() for word in parts]).strip()
            #link of ad
            link = fl.find('a')['href']
            #body of ad
            para = fl.find('p',{'class':'PT3'})
            data = para.findAll(text=True)
            body = ' '.join([word.strip() for word in data]).strip()

            post = fl.find('p',{'class':'PT3 a_10dgry'})
            post_text = post.findAll(text=True)
            post_at = ' '.join([word.strip() for word in post_text]).strip()
            print '----------------------'
            print 'title: '+title
            print 'body: '+body
            print 'link: '+link
            print 'post_at: '+post_at
            print '----------------------'
        else :
            print 'No news'



def do_all_keywords(query):
    source= get_search_results(base_url+'/mccode/common/autosuggesion.php?query='+query+'&type=3&format=json')
    datastore = json.loads(source)
    link = datastore[0]['link_src']
    html = get_search_results(link)
    scrape_news(html)

if __name__ == '__main__' :
    query_arrray= ['CANFINHOME','HFCL','3IINFOTECH','TATASTEEL','NITCO','ANDHRABANK','KEC']
    # query= 'CANFINHOME'
    for query in query_arrray:
        do_all_keywords(query)