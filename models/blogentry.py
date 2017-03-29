from google.appengine.ext import db
import models

class BlogEntry(db.Model):
    """A representation of the main entries of the blog"""
    title = db.StringProperty(required=True, indexed=True)
    entry = db.TextProperty(required=True)
    author = db.StringProperty(required=True, indexed=True)
    posted = db.DateTimeProperty(auto_now_add=True, indexed=True)
    # likeCount = db.IntegerProperty(default=0, indexed=True)
    # commentCount = db.IntegerProperty(default=0, indexed=True)

    @property
    def likeCount(self):
        return models.like_count(self)

    @property
    def commentCount(self):
        return models.comment_count(self)

    @property
    def id(self):
        return self.key().id()

    def liked(self, user_name):
        return models.post_is_liked(self, user_name)
