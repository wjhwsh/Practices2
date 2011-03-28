from google.appengine.ext import db

class Counter(db.Model):
    count = db.IntegerProperty(required=True, default=0)

class User(db.Model):
    google_user = db.UserProperty()
    name = db.StringProperty()
    avatar = db.BlobProperty()

class Bookmark(db.Model):
    user = db.ReferenceProperty(User, collection_name='bookmarks')
    url = db.LinkProperty(required=True)
    title = db.StringProperty(required=True)
    desc = db.TextProperty(required=True, default=db.Text(''))
    tags = db.StringListProperty()
    private = db.BooleanProperty(required=True, default=False)
    created = db.DateTimeProperty(auto_now_add=True)

class Stat(db.Model):
    name = db.StringProperty()
    data = db.ListProperty(db.Key)

