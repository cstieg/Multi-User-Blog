from google.appengine.ext import db

import models, handlers

class EditComment(handlers.Handler):
    """Edit a comment made by the author on a particular post"""
    @handlers.check_logged_in
    @handlers.check_comment_exists
    def post(self, comment_entity):
        comment_text = handlers.sanitize(self.request.get('comment'))
        if not comment_text:
            self.error(400)

        # only author can edit
        user_id = handlers.get_username(self)
        if comment_entity.author == user_id:
            models.edit_comment(comment_entity, comment_text)
        else:
            self.error(401)
