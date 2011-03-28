# -*- coding: utf-8 -*-  
  
import urllib  
  
# 抓取Yahoo!奇摩天氣的網頁內容放到WebContent  
weatherWeb = urllib.urlopen("http://tw.weather.yahoo.com/today.html")  
webContent = weatherWeb.read().decode('utf_8')  
weatherWeb.close()  
  
import HTMLParser  

areas = [u'台北市', u'基隆北海岸', u'台北地區', u'桃園地區', u'新竹地區', u'苗栗地區', u'台中地區', u'彰化地區', u'南投地區', u'雲林地區',
         u'嘉義地區', u'台南地區', u'高雄市', u'高雄地區', u'屏東地區', u'恆春半島', u'宜蘭地區', u'花蓮地區', u'台東地區', u'澎湖地區',
         u'金門地區', u'馬祖地區']
exception_data = [u'地區名稱', u'天氣預測', u'氣溫', u'降雨機率']
  
class WeaterHTMLParser(HTMLParser.HTMLParser):    
    def handle_data(self, data):    
        data = data.strip()    
        if hasattr(self, 'found') and data:  
            if data == u'TOP':  
                self.stop = True  
                return  
            if data in exception_data:
                pass
            else:
                weather.append(data)
        for area in areas: 
            if data == area:
                self.found = True
                if area == areas[0]:
                    weather.append(area)
    def unknown_decl(self, data):  
        """Override unknown handle method to avoid exception"""  
        pass  

  
weather = []  
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

for i in range(0, len(areas)):
    print u"%s 的今天天氣是 %s，氣溫是 %s度%s，降雨機率是 %s" % (weather[5*i], weather[5*i+1], weather[5*i+2], weather[5*i+3], weather[5*i+4])  

print "Press enter to continue."  
raw_input()  
