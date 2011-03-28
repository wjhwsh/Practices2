from datetime import datetime
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write('<h1>Hello, world</h1>')


class NowPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write('It is <b>%s</b> now.' % datetime.now())


def main():
    application = webapp.WSGIApplication([
                      ('/', MainPage),
                      ('/now', NowPage)
                  ], debug=True)
    run_wsgi_app(application)


if __name__ == '__main__':
    main()
