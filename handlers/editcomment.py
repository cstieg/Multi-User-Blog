from google.appengine.ext import db

import models, handlers

class EditComment(handlers.Handler):
    """Edit a comment made by the author on a particular post"""
    @handlers.check_logged_in
    def post(self, comment_id='', parent_id=''):
        comment_text = handlers.sanitize(self.request.get('comment'))
        if comment_id and parent_id and comment_text:
            # query post by id passed in
            parent_key = models.BlogEntry.get_by_id(int(parent_id)).key()
            parent_entity = db.get(parent_key)
            comment_entity = models.Comment.get_by_id(int(comment_id), parent=parent_key)
            if not comment_entity or not parent_entity:
                self.error(400)
                return

            # only author can edit
            user_id = handlers.get_username(self)
            if comment_entity.author == user_id:
                models.edit_comment(comment_entity, comment_text)
            else:
                self.error(401)
        else:
            self.error(400)

