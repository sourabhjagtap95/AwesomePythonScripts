import httplib2
import pdfcrowd
from bs4 import BeautifulSoup, SoupStrainer
 
http = httplib2.Http()
s= 'http : // www. geeksforgeeks. org/ '
to_crawl=[]
crawled=[]
i=0
to_crawl.append(s)
status, response = http.request(s)
crawled.append(s)
 
 for link in BeautifulSoup(response, parse_only=SoupStrainer('a')):
        if link.has_attr('href'):
            li=link['href']
            #print li
            if li.find('http : // www. geeksforgeeks. org/')==0 and li not in crawled and li.find('forums')<0:
                to_crawl.append(li)
            
 
#print to_crawl
print len(to_crawl)
count=0
 
def get_page(page):
    import urllib2
    source=urllib2.urlopen(page)
    return source.read()
 
 
def save_as_pdf(s):
    global i
    try:
        client = pdfcrowd.Client("mkap1234", "fc5ada9fbd1c55f46822d6e9e985a9bb")
        output_file = open('amazon'+str(i)+'.pdf', 'wb')
        i=i+1
        html=get_page(s)
        client.convertHtml(html, output_file)
        output_file.close()
    except pdfcrowd.Error,why:
        print 'Failed:', why
 
 
while len(to_crawl):
    b=to_crawl.pop()
    if b.find('http : // www. geeksforgeeks. org/')==0 and b not in crawled and b.find('forums')<0:
        count=count+1
        print count
        crawled.append(b)
        status, response = http.request(b)
        for link in BeautifulSoup(response, parse_only=SoupStrainer('a')):
            if link.has_attr('href'):
                li=link['href']
                if b.find('http : // www. geeksforgeeks. org/')==0 and li not in crawled:
                    to_crawl.append(li)
                    
amazon=[ ]
 
for st in crawled:
    if st.find('amazon')>=0 and st.find('#')<0 and st.find('tag')<0 and st.find('forum')<0:
        print st
        amazon.append(st)
 
 
 
print "Finished"
print len(amazon)
        
  
for page in amazon:
    save_as_pdf(page)
