# -*- coding: utf-8 -*-  
import urllib, re, os
from BeautifulSoup import BeautifulSoup          # For processing HTML

#http://wwwc.moex.gov.tw/problem/tsv_32dlist.asp?D2=9410
weatherWeb = urllib.urlopen("http://wwwc.moex.gov.tw/problem/tsv_32dlist.asp?D2=9401")


def getLinksOfCurrentPage(url):
    downloadList = []
    weatherWeb = urllib.urlopen(url)
    webContent = weatherWeb.read().decode('big5')  
    weatherWeb.close()  
    
    soup = BeautifulSoup(webContent)
    keywords = [u'財稅行政']
    for keyword in keywords:
        result = soup.findAll(text=re.compile(keyword))
        if len(result) == 0:
            continue
        else:
            for r in result:
                print r
                list = r.parent
                hyperlink = list.nextSibling.nextSibling
                
                parseList = []
                for achor in hyperlink.findAll('a'):
                    parseList.append(str(achor['href']))
                
                downloadList = []
                for i in range(0, len(parseList)):
                    if i%2 == 1:
                        downloadList.append("http://wwwc.moex.gov.tw" + parseList[i])
    return downloadList

def getPageNumsOfYear(year):
    url = "http://wwwc.moex.gov.tw/problem/tsv_32dtop.asp?D1=" + year
    web = urllib.urlopen(url)
    webContent = web.read().decode('big5')
    web.close()

    soup = BeautifulSoup(webContent)
    list = soup.findAll('option')

    relatedExamNumbers = []
    keywords = [u'財稅', u'五等', u'初等', u'三等', u'四等', u'高考', u'普考'] # future work: don't repeat the links
    for keyword in keywords:
        pattern = keyword

        for l in list:
            string = unicode(str(l), encoding='utf-8') # Exam name

            if re.search(pattern, string) is not None:
                relatedExamNumbers.append(l['value'])

    return relatedExamNumbers


def writeToScript(links):
    fout.write('mkdir -p ' + downloadPath + str(links)[35:40] + '\n')
    
    for link in links:
        fout.write('wget ' + link + ' -O ' + downloadPath + str(link)[33:49] + '\n')
    fout.write('#===============================================\n')





year = raw_input('which year to download? ')
examNumbers = getPageNumsOfYear(year)

# initialize the script
filepath = os.getcwd() + '/scripts/'
downloadPath = os.getcwd() + '/Downloads/'
filename = year + '.sh'
fout = open(filepath + filename, 'a')
fout.write(r'#!/usr/bin/bash')
fout.write('\nmkdir ' + downloadPath + year + '\n')


for exam in examNumbers:
    url = "http://wwwc.moex.gov.tw/problem/tsv_32dlist.asp?D2=" + exam
    print url
    list = getLinksOfCurrentPage(url)
    if len(list) != 0:
        writeToScript(list)
        for l in list:
            print l
        print "================================================================"




    
    
