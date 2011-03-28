#! -*- coding: utf-8 -*-
import pickle
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import login_required
from google.appengine.ext import db
from google.appengine.ext.db import BadValueError
from google.appengine.api import users
from google.appengine.api import memcache
import model

ITEMS_PER_PAGE = 20

class Avatar(webapp.RequestHandler):
    def get(self, name):
        avatar = memcache.get('avatar_%s' % name)
        if not avatar:
            user = model.User.gql('WHERE name = :1', name).get()
            avatar = user.avatar
            memcache.set('avatar_%s' % name, avatar, time=3600)
            
        self.response.headers['Content-Type'] = 'image/png'
        self.response.out.write(avatar)
            

class Main(webapp.RequestHandler):
    def get(self):
        latest = model.Stat.get_by_key_name('stat_latest')
        if latest is None:
            bookmarks = []
        else:
            bookmarks = model.Bookmark.get(latest.data)
        bookmarks = reversed(bookmarks)
        self.response.out.write(
            template.render('templates/list.html', {
                'bookmarks': bookmarks,
                'title': '首頁'
            })
        )
        
class Home(webapp.RequestHandler):
    @login_required
    def get(self):
        guser = users.get_current_user()
        user = model.User.gql('WHERE google_user = :1', guser).get()
        if user is None:
            self.redirect('/signup')
        else:
            # bookmarks
            self.response.out.write(
                template.render('templates/home.html', {'user': user})
            )


class User(webapp.RequestHandler):
    def get(self, username):
        user = model.User.gql('WHERE name = :1', username).get()
        if user is None:
            self.response.out.write('查無使用者: %s' % username)
        else:
            bookmarks = model.Bookmark.gql('WHERE private = False and user = :1', user)
            self.response.out.write(
                template.render('templates/list.html', {
                    'title': '%s 的公開書籤列表' % username,
                    'bookmarks': bookmarks
                })
            )


class Signup(webapp.RequestHandler):
    @login_required
    def get(self):
        guser = users.get_current_user()
        self.response.out.write(
            template.render('templates/signup.html', {
                'email': guser.email(),
                'title': '註冊身份'
            })
        )
        
    def post(self):
        from google.appengine.api import images
        guser = users.get_current_user()
        
        resized_img = images.resize(self.request.get('avatar'),
                                    width=48, height=48,
                                    output_encoding=images.PNG)
        
        user = model.User(
            google_user=guser,
            name=self.request.get('name'),
            avatar=resized_img
        )
        user.put()
        self.redirect('/home')
  

class Post(webapp.RequestHandler):
    @login_required
    def get(self):
        self.response.out.write(
            template.render('templates/post.html', {})
        )
        
    def post(self):
        try:
            guser = users.get_current_user()
            user = model.User.gql('WHERE google_user = :1', guser).get()

            url = db.Link(self.request.get('url'))
            title = self.request.get('title')
            desc = db.Text(self.request.get('desc'))
            tags = self.request.get('tags').split(',')
            for i in range(len(tags)):
                tags[i] = tags[i].strip()
            private = self.request.get('private') == 'on'
            
            bookmark = model.Bookmark(parent=user,
                                user=user,
                                url=url,
                                title=title,
                                desc=desc,
                                tags=tags,
                                private=private)
            bookmark.put()
            
            counter = model.Counter.get_by_key_name('%s_bookmark_counter' % guser,
                                                    parent=user)
            if counter is None:
                counter = model.Counter(key_name='%s_bookmark_counter' % guser, parent=user)
            counter.count += 1
            counter.put()
            
            latest = model.Stat.get_by_key_name('stat_latest')
            if latest is None:
                latest = model.Stat(key_name='stat_latest')
            latest.data = [bookmark.key()] + latest.data
            latest.put()
            
            self.redirect('/home')
        except Exception,ex:
            self.response.out.write(ex)
            

class Search(webapp.RequestHandler):
    def get(self):
        keyword = self.request.get('q')
        page = int(self.request.get('page', '1'))
        offset = (page-1) * ITEMS_PER_PAGE
        bookmarks = model.Bookmark.gql(
            'WHERE private = False and title >= :1 and title < :2 LIMIT %d,%d' % (offset, ITEMS_PER_PAGE),
            keyword, unicode(keyword) + u'\ufffd')
        self.response.out.write(
            template.render('templates/list.html', {
                'title': '搜尋「%s」的結果' % keyword.encode('utf-8'), 
                'bookmarks': bookmarks
            })
        )


class Tag(webapp.RequestHandler):
    def get(self, tag):
        import urllib
        tag = urllib.unquote(tag)
        query = model.Bookmark.gql('WHERE private = False and tags = :1', tag)
        bookmarks = query.fetch(1000)
        self.response.out.write(
            template.render('templates/list.html', {
                'title': '標籤為「%s」的公開書籤' % tag,
                'bookmarks': bookmarks
            })
        )
