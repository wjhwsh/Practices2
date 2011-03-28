from google.appengine.ext import db

class Message(db.Model):
    name = db.StringProperty(required=True)
    comment = db.StringProperty(required=True, multiline=True)
    created = db.DateTimeProperty(auto_now_add=True)

class Counter(db.Model):
    value = db.IntegerProperty(required=True, default=0)
