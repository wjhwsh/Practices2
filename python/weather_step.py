# -*- coding: utf-8 -*-  
  
import urllib  
  
# 抓取Yahoo!奇摩天氣的網頁內容放到WebContent  
weatherWeb = urllib.urlopen("http://tw.weather.yahoo.com/today.html")  
webContent = weatherWeb.read().decode('utf_8')  
weatherWeb.close()  
  
import HTMLParser  
  
# 用來解析台中地區天氣資訊的解析器，繼承自HTMLParser  
class WeaterHTMLParser(HTMLParser.HTMLParser):  
    def handle_starttag(self, tag, attrs):  
        print u'標籤 %s %s 開始' % (tag, attrs)  
  
    def handle_startendtag(self, tag, attrs):  
        print u'空標籤 %s %s' % (tag, attrs)  
  
    def handle_endtag(self, tag):  
        print u'標籤 %s 結束' % tag  
  
    def handle_data(self, data):  
        print u'資料 "%s"' % data  
  
    def handle_comment(self, data):  
        print u'註解 "%s"' % data  
  
    def unknown_decl(self, data):  
        """Override unknown handle method to avoid exception"""  
        pass  
  
Parser = WeaterHTMLParser()  
  
try:  
    # 將網頁內容拆成一行一行餵給Parser  
    for line in webContent.splitlines():  
        # 如果出現停止旗標，停止餵食資料，並且跳出迴圈  
        if hasattr(Parser, 'stop') and Parser.stop:  
            break  
        Parser.feed(line)  
except HTMLParser.HTMLParseError, data:  
    print "# Parser error : " + data.msg  
  
Parser.close()  
  
print "Press enter to continue."  
raw_input()  

