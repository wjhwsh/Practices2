# model.py
from google.appengine.ext import db

class Blog(db.Model):
    title = db.StringProperty(required=True)
    description = db.StringProperty(required=True, multiline=True)
    articles_per_page = db.IntegerProperty(required=True, default=10)
    created = db.DateTimeProperty(auto_now_add=True)

class Article(db.Model):
    author = db.UserProperty()
    blog = db.ReferenceProperty(Blog, collection_name='articles')
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True, default=db.Text(''))
    tags = db.StringListProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)

class Comment(db.Model):
    article = db.ReferenceProperty(Article, collection_name='comments')
    user = db.StringProperty(required=True)
    comment = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True)

class Counter(db.Model):
    count = db.IntegerProperty(required=True, default=0)
