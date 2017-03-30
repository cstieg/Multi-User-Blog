from google.appengine.ext import db
import models

class BlogEntry(db.Model):
    """A representation of the main entries of the blog"""
    title = db.StringProperty(required=True, indexed=True)
    entry = db.TextProperty(required=True)
    author = db.StringProperty(required=True, indexed=True)
    posted = db.DateTimeProperty(auto_now_add=True, indexed=True)

    @property
    def id(self):
        return self.key().id()

    @property
    def commentCount(self):
        return models.comment_count(self)

    @property
    def likeCount(self):
        return models.like_count(self)

    def liked(self, user_name):
        return models.post_is_liked(self, user_name)
