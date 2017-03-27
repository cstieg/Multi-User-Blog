"""Handlers for likes on blog entries and comments"""
from google.appengine.ext import db

from handler import Handler
from model import (BlogEntry, Comment, validUserLogin, getUsername,
                   postIsLiked, likePost, unlikePost, commentIsLiked,
                   likeComment, unlikeComment)

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
            entryEntity = db.get(entryKey)

            # author cannot like
            liker = getUsername(self)
            if liker == entryEntity.author:
                self.error(403)
                return

            if postIsLiked(entryEntity, liker):
                # forbidden to like twice
                self.error(403)
                return

            likePost(entryEntity, liker)

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
            entryEntity = db.get(entryKey)

            liker = getUsername(self)
            if not postIsLiked(entryEntity, liker):
                # cannot unlike if not liked
                self.error(403)
                return

            unlikePost(entryEntity, liker)

        else:
            self.error(400)


class LikeComment(Handler):
    """Adds a user like and increments like count for comment"""
    def post(self, commentID="", parentID=""):
        # check to make sure valid login
        if not validUserLogin(self):
            self.redirect("/login")
        if commentID and parentID:
            # query post by id passed in
            parentKey = BlogEntry.get_by_id(int(parentID)).key()
            parentEntity = db.get(parentKey)
            commentEntity = Comment.get_by_id(int(commentID), parent=parentKey)
            if not commentEntity or not parentEntity:
                self.error(400)
                return

            # author cannot like
            liker = getUsername(self)
            if liker == commentEntity.author:
                self.error(403)
                return

            if commentIsLiked(commentEntity, liker):
                # forbidden to like twice
                self.error(403)
                return

            likeComment(commentEntity, liker)

        else:
            self.error(400)


class UnlikeComment(Handler):
    """Cancels a user like and decrements like count for comment"""
    def post(self, commentID="", parentID=""):
        # check to make sure valid login
        if not validUserLogin(self):
            self.redirect("/login")
        if commentID and parentID:
            # query post by id passed in
            parentKey = BlogEntry.get_by_id(int(parentID)).key()
            parentEntity = db.get(parentKey)
            commentEntity = Comment.get_by_id(int(commentID), parent=parentKey)
            if not commentEntity or not parentEntity:
                self.error(400)
                return

            liker = getUsername(self)
            if not commentIsLiked(commentEntity, liker):
                # cannot unlike if not liked
                self.error(403)
                return

            unlikeComment(commentEntity, liker)

        else:
            self.error(400)
