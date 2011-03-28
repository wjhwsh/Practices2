import base64
from google.appengine.ext import webapp

class MainPage(webapp.RequestHandler):
    def get(self):
        if not self.request.headers.has_key('Authorization'):
            self.response.set_status(401, 'Authorization Required')
            self.response.headers.add_header('WWW-Authenticate', 'Basic realm="Foo Site Auth"')

        else:
            auth = self.request.headers.get('Authorization')
            idpwd = base64.decodestring(auth.split(' ')[1])
            userid, password = idpwd.split(':')
            # check userid and password
            self.response.out.write('ID: %s, Password: %s' % (userid, password))

def main():
    application = webapp.WSGIApplication([
                      ('/', MainPage),
                  ], debug=True)
    run_wsgi_app(application)


if __name__ == '__main__':
    main()
