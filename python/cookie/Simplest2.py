import urllib, urllib2, cookielib
import re


cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib2.install_opener(opener)
login_page_contents = opener.open('https://www.google.com/accounts/ServiceLogin').read()
# Find GALX value
galx_match_obj = re.search(r'name="GALX"\s*value="([^""]+)"', login_page_contents, re.IGNORECASE)
galx_value = galx_match_obj.group(1) if galx_match_obj.group(1) is not None else ''

body = urllib.urlencode( {
                                       'Email' : 'modcarl',
                                       'Passwd' : 'au4a832rrijaai',
                                       'continue' : 'http://www.google.com.tw/dictionary/wordlist?hl=zh-TW',
                                       'GALX': galx_value
                           })
opener.open('https://www.google.com/accounts/ServiceLogin', body)
resp =  opener.open('http://www.google.com.tw/dictionary/wordlist?hl=zh-TW')
print resp
