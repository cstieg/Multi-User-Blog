from google.appengine.ext import db
import models, handlers

class LikeComment(handlers.Handler):
    """Adds a user like and increments like count for comment"""
    @handlers.check_logged_in
    @handlers.check_comment_exists
    def post(self, comment_entity):
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


class UnlikeComment(handlers.Handler):
    """Cancels a user like and decrements like count for comment"""
    @handlers.check_logged_in
    @handlers.check_comment_exists
    def post(self, comment_entity):
        liker = handlers.get_username(self)
        if not models.comment_is_liked(comment_entity, liker):
            # cannot unlike if not liked
            self.error(403)
            return

        models.unlike_comment(comment_entity, liker)