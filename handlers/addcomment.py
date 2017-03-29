import json
from google.appengine.ext import db
import models, handlers

class AddComment(handlers.Handler):
    """Add a comment to a particular post"""
    @handlers.check_logged_in
    def post(self, entry_id=''):
        if entry_id:
            # query post by id passed in
            entry_key = db.Key.from_path('BlogEntry', int(entry_id))

            if not entry_key:
                self.error(400)
                return
            entry_entity = db.get(entry_key)
        else:
            self.error(400)

        comment_text = handlers.sanitize(self.request.get('comment'))
        user_id = handlers.get_username(self)
        if comment_text and user_id:
            new_comment_entity = models.add_comment(entry_entity, comment_text, user_id)
            new_comment_dict = handlers.to_dict(new_comment_entity)
            new_comment_dict['id'] = new_comment_entity.key().id()
            self.response.out.write(json.dumps(new_comment_dict))
        else:
            self.error(400)
