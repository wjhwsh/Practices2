# -*- coding: utf-8 -*-  
  
import urllib  
  
weatherWeb = urllib.urlopen("http://tw.weather.yahoo.com/today.html")  
webContent = weatherWeb.read().decode('utf_8')  
weatherWeb.close()  
  
import HTMLParser  
import os
from google.appengine.ext.webapp import template
import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
  
class WeaterHTMLParser(HTMLParser.HTMLParser):        
    def handle_data(self, data):    
        data = data.strip()    
        if hasattr(self, 'found') and data:  
            if data == u'高雄地區':  
                self.stop = True  
                return  
            self.weather.append(data)  
        if data == u'高雄市':  
            self.found = True  
            self.weather = []  
            self.weather.append(data)
    def unknown_decl(self, data):  
        """Override unknown handle method to avoid exception"""  
        pass  

class MainPage(webapp.RequestHandler):
    def get(self):  
        Parser = WeaterHTMLParser()  
        for line in webContent.splitlines():  
            if hasattr(Parser, 'stop') and Parser.stop:  
                break  
            Parser.feed(line)  
        template_values = {
            'site': Parser.weather[0],
            'weather': Parser.weather[1],
            'temperature': Parser.weather[2],
            'unit': Parser.weather[3],
            'probability': Parser.weather[4]
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
