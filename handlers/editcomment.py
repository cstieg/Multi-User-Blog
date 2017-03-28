from google.appengine.ext import db

from handlers import Handler, valid_user_login, sanitize, get_username
from models import BlogEntry, Comment, edit_comment

class EditComment(Handler):
    """Edit a comment made by the author on a particular post"""
    def post(self, comment_id="", parent_id=""):
        if not valid_user_login(self):
            self.redirect("/login")
        comment_text = sanitize(self.request.get('comment'))
        if comment_id and parent_id and comment_text:
            # query post by id passed in
            parent_key = BlogEntry.get_by_id(int(parent_id)).key()
            parent_entity = db.get(parent_key)
            comment_entity = Comment.get_by_id(int(comment_id), parent=parent_key)
            if not comment_entity or not parent_entity:
                self.error(400)
                return

            # only author can edit
            user_id = get_username(self)
            if comment_entity.author == user_id:
                edit_comment(comment_entity, comment_text)
            else:
                self.error(401)
        else:
            self.error(400)

