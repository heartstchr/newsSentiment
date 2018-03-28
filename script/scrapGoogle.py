#!/usr/bin/env python

import sys
import urllib2
import re
import sqlite3
import datetime

from BeautifulSoup import BeautifulSoup  # available at: http://www.crummy.com/software/BeautifulSoup/

conn = sqlite3.connect("espionage.sqlite")
conn.row_factory = sqlite3.Row

def get_google_search_results(keywordPhrase):
    """make the GET request to Google.com for the keyword phrase and return the HTML text
    """
    url='http://www.google.com/search?hl=en&q=' + '+'.join(keywordPhrase.split())
    req = urllib2.Request(url)
    req.add_header('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13')
    page = urllib2.urlopen(req)
    HTML = page.read()
    return HTML

def scrape_ads(text):
    """Scrape the text as HTML, find and parse out all the ads and store them in a database
    """
    soup = BeautifulSoup(text)
    #get the ads on the right hand side of the page
    center = soup.find("div", {"id":"center_col"})
    ads = center.findAll('li', {'class': 'ads-ad'})
    position = 0
    for ad in ads:
        position += 1
        # print '********************************************'
        # print ad
        # print '********************************************'
        #display url
        parts = ad.find('cite').findAll(text=True)
        site = ''.join([word.strip() for word in parts]).strip()
        ad.find('cite').replaceWith("")

        #the header line
        parts = ad.find('a').findAll(text=True)
        title = ' '.join([word.strip() for word in parts]).strip()

        #the destination URL
        href = ad.find('a')['href']
        start = href.find('&q=')

        if start != -1 :
            dest = href[start+3:]
        else :
            dest = href

        ad.find('a').replaceWith("")

        #body of ad
        brs = ad.findAll('br')
        for br in brs:
            br.replaceWith("%BR%")
        parts = ad.findAll(text=True)
        body = ' '.join([word.strip() for word in parts]).strip()
        print '----------------'
        print title
        print site
        print dest
        print body
        print '----------------'



def do_all_keywords():
    html = get_google_search_results('Auto insurance')
    scrape_ads(html)

if __name__ == '__main__' :
    do_all_keywords()
