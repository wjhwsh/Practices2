# -*- coding: utf-8 -*-  
  
import urllib   
import HTMLParser  
import os

import cgi
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from BeautifulSoup import BeautifulSoup 

weatherWeb = urllib.urlopen("http://tw.weather.yahoo.com/today.html")  
webContent = weatherWeb.read().decode('utf_8')  
weatherWeb.close()  
weatherWeb = urllib.urlopen("http://tw.weather.yahoo.com/week.html")  
webContent_week = weatherWeb.read().decode('utf_8')  
weatherWeb.close()  

areas = [u'台北市', u'基隆北海岸', u'台北地區', u'桃園地區', u'新竹地區', u'苗栗地區', u'台中地區', u'彰化地區', u'南投地區', u'雲林地區',
         u'嘉義地區', u'台南地區', u'高雄市', u'高雄地區', u'屏東地區', u'恆春半島', u'宜蘭地區', u'花蓮地區', u'台東地區', u'澎湖地區',
         u'金門地區', u'馬祖地區']
exception_data = [u'地區名稱', u'天氣預測', u'氣溫', u'降雨機率']

'''  
class AreasClass(db.Model):
    herf = db.StringProperty(multiline=False)
    site = db.StringProperty(multiline=False)
    weather = db.StringProperty(multiline=False) 
    temporature = db.StringProperty(multiline=False)
:1: Command not found.
    probability = db.StringProperty(multiline=False)
'''
class AreasClass():
    def nothing(self):
        pass

class WeekWeatherClass():
    def nothing(self):
        pass

class WeatherHTMLParser(HTMLParser.HTMLParser):        
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

class MainPage(webapp.RequestHandler):
    def get(self):  
        global weather
        weather = []
        Parser = WeatherHTMLParser()
        TodayWeathers = []
        for line in webContent.splitlines():  
            if hasattr(Parser, 'stop') and Parser.stop:  
                break             
            Parser.feed(line)  
        
        for i in range(0, len(areas)):
            AreaObj = AreasClass()
            AreaObj.href = '\"#area'+str(i)+'\"'
            AreaObj.site = weather[5*i]
            AreaObj.weather = weather[5*i+1]
            AreaObj.temporature = weather[5*i+2]
            AreaObj.unit = weather[5*i+3]
            AreaObj.probability = weather[5*i+4]
            TodayWeathers.append(AreaObj)
        del TodayWeathers[0]
        del TodayWeathers[0]
        del TodayWeathers[10]
        del TodayWeathers[12]
   
        for i in range(len(TodayWeathers)):
            TodayWeathers[i].href = '\"#area'+str(i)+'\"'
        
        #week weather
        WeekObjSet = []
        soup = BeautifulSoup(webContent_week)
        arealist = soup.findAll("td", { "height" : "70" })
        del arealist[0]
        weatherlist = soup.findAll("img", { "width" : "35" })
        del weatherlist[0:6]
        raw_tlist = soup.findAll("td", { "class" : "t" })
        tlist = []
        raw_datelist = soup.findAll("td", { "class" : "sbody1"})
        del raw_datelist[0] 
        datelist = []

        for i in range(len(raw_tlist)):
            soup = BeautifulSoup(str(raw_tlist[i]))
            tlist.append(soup.div.contents)
        del tlist[0:7]
        for i in range(0, len(raw_datelist)):
            soup = BeautifulSoup(str(raw_datelist[i]))
            datelist.append(soup.div.contents[0]);
        
        for i in range(0, 9):
            WeekObj = WeekWeatherClass()
            WeekObj.area = []
            WeekObj.weatherlist = []
            WeekObj.tlist = []
            WeekObj.area.append(arealist[i])
            for d in range(0,7):
                WeekObj.weatherlist.append(weatherlist[7*i+d])
                WeekObj.tlist.append(tlist[7*i+d]) 
            WeekObjSet.append(WeekObj)

        for i in range(len(TodayWeathers)):
            TodayWeathers[i].datelist = []
            TodayWeathers[i].tlist = []
            TodayWeathers[i].weatherlist = []
            if 0<= i and i<=3:
                TodayWeathers[i].tlist = WeekObjSet[0].tlist
                TodayWeathers[i].weatherlist = WeekObjSet[0].weatherlist
                TodayWeathers[i].areabelong = WeekObjSet[0].area
            elif 4<=i and i<=8:
                TodayWeathers[i].tlist = WeekObjSet[1].tlist
                TodayWeathers[i].weatherlist = WeekObjSet[1].weatherlist
                TodayWeathers[i].areabelong = WeekObjSet[1].area
            elif 9<=i and i<=11:
                TodayWeathers[i].tlist = WeekObjSet[2].tlist
                TodayWeathers[i].weatherlist = WeekObjSet[2].weatherlist
                TodayWeathers[i].areabelong = WeekObjSet[2].area
            elif 12==i:
                TodayWeathers[i].tlist = WeekObjSet[3].tlist
                TodayWeathers[i].weatherlist = WeekObjSet[3].weatherlist
                TodayWeathers[i].areabelong = WeekObjSet[3].area
            elif 13==i:
                TodayWeathers[i].tlist = WeekObjSet[4].tlist
                TodayWeathers[i].weatherlist = WeekObjSet[4].weatherlist
                TodayWeathers[i].areabelong = WeekObjSet[4].area
            elif 14==i:
                TodayWeathers[i].tlist = WeekObjSet[5].tlist
                TodayWeathers[i].weatherlist = WeekObjSet[5].weatherlist
                TodayWeathers[i].areabelong = WeekObjSet[5].area
            elif 15==i:
                TodayWeathers[i].tlist = WeekObjSet[6].tlist
                TodayWeathers[i].weatherlist = WeekObjSet[6].weatherlist
                TodayWeathers[i].areabelong = WeekObjSet[6].area
            elif 16==i:
                TodayWeathers[i].tlist = WeekObjSet[7].tlist
                TodayWeathers[i].weatherlist = WeekObjSet[7].weatherlist
                TodayWeathers[i].areabelong = WeekObjSet[7].area
            else:
                TodayWeathers[i].tlist = WeekObjSet[8].tlist
                TodayWeathers[i].weatherlist = WeekObjSet[8].weatherlist
                TodayWeathers[i].areabelong = WeekObjSet[8].area
            
    
        template_values = {
            'TodayWeathers': TodayWeathers,
            'datelist': datelist
        }
        Parser.close()                                          
        path = os.path.join(os.path.dirname(__file__), 'web-app/index.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication(
                                     [('/', MainPage)], debug=True)
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
