#!/usr/bin/python
"""
@author = eliezer silva (djosacv@gmail.com)
@copyleft

instructions: 
1) make sure you can run the script with something like chmod a+x .. 
2) bibfinder.py "query publication name string" [author name] (optional)

examples:
bibfinder.py "latent dirichlet allocation"
bibfinder.py "latent dirichlet allocation" "blei"

limitations:
- the normal query processing of bdlp returns 25 results, usually the most recent,
we didn't try to tweak it in any way, so for now this is the main limitation
"""

import sys
import feedparser
import urllib.request, urllib.parse, urllib.error
import re
from html.parser import HTMLParser
from urllib.parse import urlparse
import urllib.request, urllib.error, urllib.parse

class mydblpbibparser(HTMLParser):
    def __init__(self):
        self.reset()
        self.bibtex_section=False
        self.indata=False
        self.result=[]

    def handle_starttag(self, tag, attrs):
        if(tag == 'div'):
            for name, value in attrs:
                if name == 'id' and value=='bibtex-section':
                    self.bibtex_section=True
                    #print value
        if(self.bibtex_section and tag=="pre"):
            #class="verbatim select-on-click"
            for name, value in attrs:
                if name=="class" and value=="verbatim select-on-click":
                    self.indata=True
                    
    def handle_endtag(self,tag):
        if(tag == 'div' and self.bibtex_section):
            self.bibtex_section=False
        if(tag=='pre' and self.indata):
            self.indata=False
    def handle_data(self, data):
        if(self.indata):
            #print data
            self.result.append(data)

class mydblpparser(HTMLParser):
    def __init__(self,author_name=None):
        self.reset()
        self.in_result_list=False
        self.inentry=False
        self.inauthorlist=False
        self.count_links=0
        self.count_in=0
        self.count_li=0
        self.actual_link=""
        self.result=[]
        self.author=author_name
        self.found_auth=False

    def handle_starttag(self, tag, attrs):
        if(tag == 'div' and self.in_result_list):
            self.count_in+=1
        if(tag == 'div' and not self.in_result_list):
            for name, value in attrs:
                if name == 'id' and value=='completesearch-publs':
                    self.in_result_list=True

        if(self.in_result_list and self.inentry and tag=="a"):
            for name, value in attrs:
                if name=="href" and "bibtex" in value:
                    self.actual_link=value
                    self.count_links+=1

                    
        if(tag == "li"):
            if(self.inentry):
                self.count_li+=1
            else:
                for name, value in attrs:
                    if name=="class" and "entry" in value:
                        self.inentry=True
                        self.found_auth=False
                        self.count_links=0
                        
        if(self.inentry and tag == "span"):
            for name, value in attrs:
                if name=="itemprop" and "author"==value:
                    self.inauthorlist=True
    def handle_endtag(self,tag):
        if(tag == 'div' and self.in_result_list):
            if(self.count_in==0):
                self.in_result_list=False
            else:
                self.count_in-=1
        if(tag == 'li' and self.inentry):
            if(self.count_li==0):
                self.inentry=False
                if(len(self.actual_link)>0):
                    if(self.found_auth or self.author==None):
                        print("bib link="+self.actual_link)
                        self.result.append("".join(process_item(self.actual_link,mydblpbibparser())))
                        
                
                self.actual_link=""
            else:
                self.count_li-=1
        if(tag == "span" and self.inauthorlist):
            self.inauthorlist=False
                
    def handle_data(self, data):
        if(self.inauthorlist and self.author!=None):
            if self.author.lower() in data.lower():
                self.found_auth=True
                print("Found author: "+data)


def openurlitem(item):
    print("link ="+item)
    req = urllib.request.Request(item)
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0")
    fp=urllib.request.urlopen(req)
    data=fp.read()
    #print data
    return data

def process_item(url_link,parser):
    #parser = myhtmlparser()
    parser.feed(openurlitem(url_link))
    return parser.result


def main(argv):
    linkstr="http://dblp.uni-trier.de/search?q="
    if(len(argv)==2):
        print("\n".join(process_item(linkstr+argv[1].replace(" ","+"),mydblpparser())))
    if(len(argv)==3):
        print("\n".join(process_item(linkstr+argv[1].replace(" ","+"),mydblpparser(argv[2]))))


if __name__ == "__main__":
    main(sys.argv)
