#!/usr/bin/env python

import urllib2
import sqlite3
import json
import string

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
    center = soup.find("div",{"class":"boxBg"})
    # print center

    table_data = [[cell.text for cell in row("td")]
                  for row in center("tr")]
    jsonTable = json.loads(table_data)

    print jsonTable


def do_all_keywords(query):
    source= get_search_results(base_url+'/mccode/common/autosuggesion.php?query='+query+'&type=3&format=json')
    datastore = json.loads(source)
    link = datastore[0]['link_src']
    new_str = string.replace(link, 'company-article', 'competition')
    new_str = string.replace(new_str,'news','comparison')
    print new_str
    html = get_search_results(new_str)
    scrape_news(html)

if __name__ == '__main__' :
    # query_arrray= ['CANFINHOME','HFCL','3IINFOTECH','TATASTEEL','NITCO','ANDHRABANK','KEC']
    # query= 'CANFINHOME'
    query_array = ['YESBANK']
    for query in query_array:
        do_all_keywords(query)