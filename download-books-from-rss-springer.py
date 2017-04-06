#!/usr/bin/python
""" @copyleft Eliezer Silva (djosacv@gmail.com)
This script was developed mostly for recreative and educational purpose, so you use it on your own risk and as it is.
With this script you can crawl in springer book search results and download all the book listed in the page. It checks if the result set includes many 
pages and navigate through this pages.

There's two ways of using it:
1) Link to a single book ulr in springer page:
	python download-books-from-rss-springer.py 'http://rd.springer.com/book/10.1007/978-3-662-07003-1'
2) Link to a search result with many books:
	python download-books-from-rss-springer.py -s 'http://rd.springer.com/search?facet-series=%223214%22&facet-content-type=%22Book%22&showAll=false'
"""
import urllib
from HTMLParser import HTMLParser
from urlparse import urlparse
import urllib2

import sys


def downloader(url,filename=None):
    file_name = filename
    if(filename==None):
        file_name = url.split('/')[-1]
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes to %s" % ( file_size, file_name)
    
    file_size_dl = 0
    block_sz = 8192
    parcels = file_size/30
    disp = False
    c=1
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
    
        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        #print status,
	if (file_size_dl > c*parcels):
		c+=1
		disp=True
	if(disp == True):
        	print "_"+r"%3.2f%%" % (file_size_dl * 100. / file_size),
		disp=False
    print ""
    f.close()


class myhtmlparser(HTMLParser):
    def __init__(self,link):
        self.reset()
        self.inLink=False
        self.domain=self.get_domain(link)
        self.pdflink=""
        self.bookname=None
	self.is_searching=True
	self.inyear=False
	self.year=""
    	self.author_list=[]
	self.inauthorlist=False
	self.inauth=False
    def handle_starttag(self, tag, attrs):
	if(tag == 'span' and ('class','copyright-year') in attrs):
		self.inyear=True
        if(tag == 'a' and self.find_link(attrs) and self.is_searching):
		self.inLink=True
    	if(tag == 'div' and (('class','author-list') in attrs or ('class','editor-list') in attrs)):
		self.inauthorlist=True
	if(tag == 'a' and ('itemprop','name') in attrs and self.inauthorlist):
		self.inauth=True


    def handle_endtag(self,tag):
	if(tag == 'div' and self.inauthorlist):
		self.inauthorlist=False
    def handle_data(self, data):
        if(self.inLink):
            print data
            print "pdf link "+self.pdflink
	    year = ""
	    if(self.year!=""):
		year="["+self.year+"]"
	    authn=",".join(self.author_list)
	    if(authn!=""):
		authn="["+authn+"]"
	    self.is_searching=False
            self.inLink=False
	if(self.inyear):
	    self.year=data.replace("\n","").replace(" ","")
	    self.inyear=False
    	if(self.inauth):
	    self.author_list.append(data.replace("\n","").replace("  "," ").split()[-1])
	    self.inauth=False
    def doDownload(self):
	    year = ""
	    if(self.year!=""):
		year="["+self.year+"]"
	    authn=",".join(self.author_list)
	    if(authn!=""):
		authn="["+authn+"]"
            downloader(self.pdflink,year+authn+self.bookname+".pdf")
    def find_link(self,attrs):
        attrnames=zip(*attrs)[0]
        vals=zip(*attrs)[1]
        ret=False
        bookn=""
        if('doi' in attrnames and ('contenttype', 'Book') in attrs and 'href' in attrnames):
            for pair_val in attrs:
                if(pair_val[0]=='href' and pair_val[1].endswith('pdf')):
                    self.pdflink = self.domain+pair_val[1]
                    ret = True
                if(pair_val[0]=='publication'):
                    bookn=pair_val[1].replace('/','.').split("|")[1]+"."+pair_val[1].replace('/','.').split("|")[0]
        if(ret):
            self.bookname=bookn
        return ret
    
    def get_domain(self,url):
        parsed_uri = urlparse( url )
        domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        return domain

def openurlitem(item):
    fp=urllib.urlopen(item)
    data=fp.read().replace('\n', '')
    return data

def process_item(url_link):
    parser = myhtmlparser(url_link)
    parser.feed(openurlitem(url_link))
    parser.doDownload()


    
class mylisthtmlparser(myhtmlparser):
    def __init__(self,link):
        self.reset()
        self.inLink=False
        self.inResultList=False
        self.domain=self.get_domain(link)
	self.nextlink=""
	self.pagination=False

    def handle_starttag(self, tag, attrs):
        if(self.inResultList):
            if(tag == 'a' and ('class','title') in attrs):
                self.inLink=True
		self.pdflink = self.getHref(attrs)
                
        if(tag == 'ol' and ('id','results-list') in attrs):
            self.inResultList=True
	if(tag=='form' and ('class','pagination') in attrs):
	    self.pagination = True
	if(self.pagination and tag == 'a' and ('class','next') in attrs and ('title','next') in attrs):
	    self.nextlink = self.pdflink = self.getHref(attrs)
	    print "next link = "+self.nextlink
    
             
    def handle_endtag(self, tag):
        if(tag == 'ol' and self.inResultList):
            self.inResultList=False
	if(tag == 'form' and self.pagination):
	    self.pagination= False
            
    
    def handle_data(self, data):
        if(self.inLink):
            print "Opening "+data
            print "url link "+self.pdflink
            try:
                process_item(self.pdflink)
            except:
                print "error : "
            self.inLink=False
    def hasNext(self):
	return self.nextlink.startswith("http")
    def getHref(self,attrs):
	for pair_val in attrs:
		if(pair_val[0]=='href'):
			return self.domain+pair_val[1]   
 

def process_page(url):
    parser = mylisthtmlparser(url)
    parser.feed(openurlitem(url))
    while(parser.hasNext()):
	url = parser.nextlink
	parser = mylisthtmlparser(url)
    	parser.feed(openurlitem(url))

if(len(sys.argv) >= 2):
    args=sys.argv[1:]
    if(len(args)==2):
        if args[0]=="-s":
            try:
                process_page(args[1])
            except:
                print "processing error. check your url"
                print "format: 'python download-books-from-rss-springer.py [-s] url'"
        else:
            print "format: 'python download-books-from-rss-springer.py [-s] url'"
    elif len(args)==1:
        try:
            process_item(args[0])
        except:
            print "processing error. check your url"
            print "format: 'python download-books-from-rss-springer.py [-s] url'"
    else:
        print "format: 'python download-books-from-rss-springer.py [-s] url'"
        print "if argument -s is passed, the script will assume the link is a rss feed with a list of books"
        print "otherwise, it will assume the link is a url of a single book"        
else:
    print "python download-books-from-rss-springer.py [-s] url"

# process_page("http://rd.springer.com/search?facet-series=%223214%22&facet-content-type=%22Book%22&showAll=false")
