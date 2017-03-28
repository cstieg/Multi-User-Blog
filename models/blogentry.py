from google.appengine.ext import db

class BlogEntry(db.Model):
    """A representation of the main entries of the blog"""
    title = db.StringProperty(required=True, indexed=True)
    entry = db.TextProperty(required=True)
    author = db.StringProperty(required=True, indexed=True)
    posted = db.DateTimeProperty(auto_now_add=True, indexed=True)
    likeCount = db.IntegerProperty(default=0, indexed=True)
    commentCount = db.IntegerProperty(default=0, indexed=True)
