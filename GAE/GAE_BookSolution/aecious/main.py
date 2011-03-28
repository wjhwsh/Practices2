from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import handler

def main():
    app = webapp.WSGIApplication([
                ('/', handler.Main),
                ('/avatar/(.*)', handler.Avatar),
                ('/home', handler.Home),
                ('/tag/(.*)', handler.Tag),
                ('/search', handler.Search),
                ('/signup', handler.Signup),
                ('/post', handler.Post),
                ('/user/(.*)', handler.User)
            ], debug=True)
    run_wsgi_app(app)
    
if __name__ == '__main__':
    main()