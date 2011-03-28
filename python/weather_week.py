# -*- coding: utf-8 -*-  
  
import urllib  
from BeautifulSoup import BeautifulSoup          # For processing HTML
# 抓取Yahoo!奇摩天氣的網頁內容放到WebContent  
weatherWeb = urllib.urlopen("http://tw.weather.yahoo.com/week.html")
webContent = weatherWeb.read().decode('utf_8')  
weatherWeb.close()  

soup = BeautifulSoup(webContent)

raw_arealist = soup.findAll("td", { "height" : "70" })#solved
del raw_arealist[0]
arealist = []

weatherlist = soup.findAll("img", { "width" : "35" })#needn't to change   OK
for i in range(len(weatherlist)):
    print weatherlist[i]
raw_tlist = soup.findAll("td", { "class" : "t" })
tlist = []

raw_datelist = soup.findAll("td", { "class" : "sbody1" })
del raw_datelist[0]
datelist = []


'''
for i in range(len(raw_arealist)):
    soup = BeautifulSoup(str(raw_arealist[i]))
    arealist.append(soup.td.span.contents)
    print arealist
'''
for i in range(len(raw_tlist)):
    soup = BeautifulSoup(str(raw_tlist[i]))
    tlist.append(soup.div.contents)
del tlist[0:7]
#print tlist                                                           

for i in range(0, len(raw_datelist)):
    soup = BeautifulSoup(str(raw_datelist[i]))
    datelist.append(soup.div.contents[0]);
#print datelist                                                             OK

