from google.appengine.ext import db
import models, handlers

class DeleteComment(handlers.Handler):
    """Delete a comment made by the author on a particular post"""
    @handlers.check_logged_in
    @handlers.check_comment_exists
    def post(self, comment_entity):
        # only author can delete
        user_id = handlers.get_username(self)
        if comment_entity.author == user_id:
            comment_entity.delete()
        else:
            self.error(401)