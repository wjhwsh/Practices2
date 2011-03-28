#-*- coding: utf-8 -*-
import os
from google.appengine.ext.webapp import template
import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class datum():
    msg1 = u"哈囉".encode('utf-8')
    msg2 = u"世界".encode('utf-8')

class MainPage(webapp.RequestHandler):
  def get(self):
    data = datum();

    template_values = {
        "data": data  
    }

    path = os.path.join(os.path.dirname(__file__), 'dir1/dir2/index.html')
    self.response.out.write(template.render(path, template_values))


application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
