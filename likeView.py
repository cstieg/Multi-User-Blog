"""Handlers for likes on blog entries and comments"""

from google.appengine.ext import db

from handler import Handler
from model import validUserLogin, getUsername, postIsLiked, likePost, unlikePost

class LikePost(Handler):
    """Adds a user like and increments like count for post"""
    def post(self, q=""):
        # check to make sure valid login
        if not validUserLogin(self):
            self.redirect("/login")
        if q:
            # query post by id passed in
            entryKey = db.Key.from_path('BlogEntry', int(q))

            if not entryKey:
                self.error(400)
                return
            blogEntry = db.get(entryKey)

            # author cannot like
            liker = getUsername(self)
            if liker == blogEntry.author:
                self.error(403)
                return
            
            if postIsLiked(blogEntry, liker):
                # forbidden to like twice
                self.error(403)
                return

            likePost(blogEntry, liker)

        else:
            self.error(400)


class UnlikePost(Handler):
    """Cancels a user like and decrements like count for post"""
    def post(self, q=""):
        # check to make sure valid login
        if not validUserLogin(self):
            self.redirect("/login")
        if q:
            # query post by id passed in
            entryKey = db.Key.from_path('BlogEntry', int(q))

            if not entryKey:
                self.error(400)
                return
            blogEntry = db.get(entryKey)

            liker = getUsername(self)
            if not postIsLiked(blogEntry, liker):
                # cannot unlike if not liked
                self.error(403)
                return

            unlikePost(blogEntry, liker)

        else:
            self.error(400)