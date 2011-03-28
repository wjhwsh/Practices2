import os.path, urllib2
import urllib, time
import re
from urllib2 import urlopen, Request
import cookielib

COOKIEFILE = 'cookies.lwp'   # "cookiejar" file for cookie saving/reloading
cj = cookielib.LWPCookieJar()

# Now load the cookies, if any, and build+install an opener using them
if cj is not None:
    if os.path.isfile(COOKIEFILE):
        print "Loading the file..."
        cj.load(COOKIEFILE)
    if cookielib:
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
    else:
        opener = ClientCookie.build_opener(ClientCookie.HTTPCookieProcessor(cj))
        ClientCookie.install_opener(opener)

# for example, try a URL that sets a cookie
theurl = 'https://www.google.com/accounts/ServiceLoginAuth' # write ur URL here


txdata = None

txheaders =  {'User-agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}

try:
    req = Request(theurl, txdata, txheaders)  # create a request object
    handle = urlopen(req)                     # and open it
except IOError, e:
    print 'Failed to open "%s".' % theurl
    if hasattr(e, 'code'):
        print 'Error code: %s.' % e.code
else:
    print 'Here are the headers of the page:'
    print handle.info()
# you can also use handle.read() to get the page, handle.geturl() to get the
# the true URL (could be different from `theurl' if there have been redirects)
if cj is None:
    print "Sorry, no cookie jar, can't show you any cookies today"
else:
    print 'Here are the cookies received so far:'
    for index, cookie in enumerate(cj):
        print index, ': ', cookie
    cj.save(COOKIEFILE, True, True)                     # save the cookies again


