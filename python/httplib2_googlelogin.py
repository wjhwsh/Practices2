 #!/usr/bin/env python
import urllib 
import httplib2 
http = httplib2.Http() 
url = 'https://www.google.com/accounts/Login?hl=zh-TW&continue=http://www.google.com.tw/'
body = {'USERNAME': 'name','PASSWORD': 'passwd'} 
headers = {'Content-type': 'application/x-www-form-urlencoded', 'User-agent': 'Mozilla/5.0'}
response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))
print content
headers = {'Cookie': response['set-cookie'], 'User-agent': 'Mozilla/5.0'} 
print response['set-cookie']
#url = 'http://www.google.com.tw/dictionary/wordlist?hl=zh-TW'
url = 'https://www.google.com/history/trends?hl=zh-TW'
response,content = http.request(url, 'GET', headers=headers) 


#h = httplib2.Http(".cache")
#h.add_credentials('name', 'password')
#resp, content = h.request("https://example.org/chap/2", "PUT", body="This is text", headers={'content-type':'text/plain'} )
