from google.appengine.ext.db import BadValueError
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import memcache
import os
import model

MSGS_PER_PAGE = 10

class MainPage(webapp.RequestHandler):
    def get(self, page):
        if len(page):
            page = int(page)
        else:
            page = 1
        
        total_msgs = memcache.get('total_msgs')
        if total_msgs is None:
            counter = model.Counter.get_by_key_name('message')
            if counter is None:
                total_msgs = 0
            else:
                total_msgs = counter.value
            memcache.set('total_msgs', total_msgs)
                
        total_page = total_msgs / MSGS_PER_PAGE
        if total_msgs % MSGS_PER_PAGE > 0:
            total_page = total_page + 1
        
        import pickle
        pickled_msgs = memcache.get('msgs_%d' % page)
        if pickled_msgs is None:
            query = model.Message.all()
            query.order('created')
            msgs = query.fetch(MSGS_PER_PAGE, (page - 1) * MSGS_PER_PAGE)
            memcache.set('msgs_%d' % page, pickle.dumps(msgs), time=60)
        else:
            msgs = pickle.loads(pickled_msgs)
        
        self.response.out.write(
            template.render('index.html', {'messages': msgs, 'total_page_list': range(1, total_page+1)})
        )
        
class SubmitAction(webapp.RequestHandler):
    def post(self):
        name = self.request.get('name', '')
        comment = self.request.get('comment', '')

        try:
            message = model.Message(name=name, comment=comment)
            message.put()
            
            counter = model.Counter.get_by_key_name('message')
            if counter is None:
                counter = model.Counter(key_name='message')
            counter.value = counter.value + 1
            counter.put()
            if memcache.get('total_msgs'):
                memcache.incr('total_msgs')
            else:
                total_msgs = counter.value
                memcache.set('total_msgs', total_msgs)

            total_pages = counter.value / MSGS_PER_PAGE
            if counter.value % MSGS_PER_PAGE:
                total_pages += 1
            
            if memcache.get('msgs_%d' % total_pages):
                memcache.delete('msgs_%d' % total_pages)
            
            self.redirect('/')
        except BadValueError:
            self.response.out.write('You have not filled the name or comment field. <a href="/">Back &raquo;</a>')
        
def main():
    app = webapp.WSGIApplication([
            ('/(\d*)', MainPage),
            ('/submit', SubmitAction)
          ], debug=True)
    run_wsgi_app(app)
    
if __name__ == '__main__':
    main()
