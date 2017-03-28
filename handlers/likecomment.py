from google.appengine.ext import db
from handlers import Handler, valid_user_login, get_username
from models import BlogEntry, Comment, comment_is_liked, like_comment, unlike_comment

class LikeComment(Handler):
    """Adds a user like and increments like count for comment"""
    def post(self, comment_id="", parent_id=""):
        # check to make sure valid login
        if not valid_user_login(self):
            self.redirect("/login")
        if comment_id and parent_id:
            # query post by id passed in
            parent_key = BlogEntry.get_by_id(int(parent_id)).key()
            parent_entity = db.get(parent_key)
            comment_entity = Comment.get_by_id(int(comment_id), parent=parent_key)
            if not comment_entity or not parent_entity:
                self.error(400)
                return

            # author cannot like
            liker = get_username(self)
            if liker == comment_entity.author:
                self.error(403)
                return

            if comment_is_liked(comment_entity, liker):
                # forbidden to like twice
                self.error(403)
                return

            like_comment(comment_entity, liker)

        else:
            self.error(400)


class UnlikeComment(Handler):
    """Cancels a user like and decrements like count for comment"""
    def post(self, comment_id="", parent_id=""):
        # check to make sure valid login
        if not valid_user_login(self):
            self.redirect("/login")
        if comment_id and parent_id:
            # query post by id passed in
            parent_key = BlogEntry.get_by_id(int(parent_id)).key()
            parent_entity = db.get(parent_key)
            comment_entity = Comment.get_by_id(int(comment_id), parent=parent_key)
            if not comment_entity or not parent_entity:
                self.error(400)
                return

            liker = get_username(self)
            if not comment_is_liked(comment_entity, liker):
                # cannot unlike if not liked
                self.error(403)
                return

            unlike_comment(comment_entity, liker)

        else:
            self.error(400)
