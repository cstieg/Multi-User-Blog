from google.appengine.ext import db
import models, handlers

class LikeComment(handlers.Handler):
    """Adds a user like and increments like count for comment"""
    @handlers.check_logged_in
    def post(self, comment_id='', parent_id=''):
        # check to make sure valid login
        if comment_id and parent_id:
            # query post by id passed in
            parent_key = models.BlogEntry.get_by_id(int(parent_id)).key()
            parent_entity = db.get(parent_key)
            comment_entity = models.Comment.get_by_id(int(comment_id), parent=parent_key)
            if not comment_entity or not parent_entity:
                self.error(400)
                return

            # author cannot like
            liker = handlers.get_username(self)
            if liker == comment_entity.author:
                self.error(403)
                return

            if models.comment_is_liked(comment_entity, liker):
                # forbidden to like twice
                self.error(403)
                return

            models.like_comment(comment_entity, liker)

        else:
            self.error(400)


class UnlikeComment(handlers.Handler):
    """Cancels a user like and decrements like count for comment"""
    @handlers.check_logged_in
    def post(self, comment_id='', parent_id=''):
        if comment_id and parent_id:
            # query post by id passed in
            parent_key = models.BlogEntry.get_by_id(int(parent_id)).key()
            parent_entity = db.get(parent_key)
            comment_entity = models.Comment.get_by_id(int(comment_id), parent=parent_key)
            if not comment_entity or not parent_entity:
                self.error(400)
                return

            liker = handlers.get_username(self)
            if not models.comment_is_liked(comment_entity, liker):
                # cannot unlike if not liked
                self.error(403)
                return

            models.unlike_comment(comment_entity, liker)

        else:
            self.error(400)
