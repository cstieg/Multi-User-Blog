import json
from google.appengine.ext import db
from handlers import Handler, sanitize, valid_user_login, get_username, to_dict
from models import add_comment

class AddComment(Handler):
    """Add a comment to a particular post"""
    def post(self, entry_id=""):
        if not valid_user_login(self):
            self.redirect("/login")
        if entry_id:
            # query post by id passed in
            entry_key = db.Key.from_path('BlogEntry', int(entry_id))

            if not entry_key:
                self.error(400)
                return
            entry_entity = db.get(entry_key)
        else:
            self.error(400)

        comment_text = sanitize(self.request.get('comment'))
        user_id = get_username(self)
        if comment_text and user_id:
            new_comment_entity = add_comment(entry_entity, comment_text, user_id)
            new_comment_dict = to_dict(new_comment_entity)
            new_comment_dict['id'] = new_comment_entity.key().id()
            self.response.out.write(json.dumps(new_comment_dict))
        else:
            self.error(400)
