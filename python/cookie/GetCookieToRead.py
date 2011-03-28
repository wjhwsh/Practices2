import os.path, urllib2
import urllib, time
import re
from urllib2 import urlopen, Request
import cookielib

COOKIEFILE = 'cookies2.lwp'   # "cookiejar" file for cookie saving/reloading
cj = cookielib.LWPCookieJar()

# Now load the cookies, if any, and build+install an opener using them
if cj is not None:
    if os.path.isfile(COOKIEFILE):
        print "Loading the file..."
        cj.load(COOKIEFILE)
    if cookielib:
        print "Printing..."
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
        print opener.open('http://www.google.com.tw/dictionary/wordlist?hl=zh-TW')
    else:
        opener = ClientCookie.build_opener(ClientCookie.HTTPCookieProcessor(cj))
        ClientCookie.install_opener(opener)

