"""Namecheap.com marketplace parser.
Returns alist of domains within specified price limits 

Usage:
  namecheap-parse.py <min_price> <max_price> 
"""
from docopt import docopt
#from lxml import 
from lxml.html import fromstring
import requests
import time
import sys
# a time delay between consecutive requests, in seconds
DELAY=1
if __name__ == '__main__':
    arguments = docopt(__doc__)
    price_min=arguments['<min_price>']
    price_max=arguments['<max_price>']
    try:
        price_min=int(price_min)
        price_max=int(price_max)
    except ValueError:
        print "<min_price> and <max_price> must be integer"
        sys.exit(0)   
    filename='namecheap-domains-%s-to-%s-dollars.txt' %(price_min,price_max)
    print "Parsing namecheap for domain %s to %s US dollars worth" %(price_min,price_max)
    print "Expect results in file: %s" % filename
    with open(filename,'w') as f:
        uri=r"https://www.namecheap.com/domains/marketplace/buy-domains.aspx?page=1&size=100&excludehypen=false&excludenumber=false&adultlisting=true&priceRange="+str(price_min)+"%3a"+str(price_max)+"&SortExpression=DomainName_ASC"
        r = requests.get(uri)
        page=fromstring(r.text)
        last_page=int(page.xpath('//li[@class="last"]')[0].xpath('a')[0].text)
        print "Total %s pages" % last_page
        total_domains=0
        for page_num in xrange(1,last_page+1):
            domains=0
            uri=r'https://www.namecheap.com/domains/marketplace/buy-domains.aspx?page='+str(page_num)+r'&size=100&excludehypen=false&excludenumber=false&adultlisting=true&priceRange='+str(price_min)+"%3a"+str(price_max)+'&SortExpression=DomainName_ASC'
            r = requests.get(uri)
            page=fromstring(r.text)
            no_items=u'There are no items to display' in r.text
            if no_items: break
            print "Parsing page %s of %s..." %(page_num,last_page)
            elements=page.xpath('//li[@class="group"]')
            for el in elements:
                domain=el.xpath('div/strong/a')[0].text.strip()
                price=el.xpath('div/span[@class="price"]')[0].text
                s="%s\n"%(domain)
                f.write(s)
                domains+=1
            #print "%s domains" % domains
            total_domains+=domains
        time.sleep(DELAY)
    print "Done, %s domains total." % total_domains
