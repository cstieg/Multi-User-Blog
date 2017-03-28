from google.appengine.ext import db
from handlers import Handler, valid_user_login, get_username
from models import BlogEntry, Comment, delete_comment

class DeleteComment(Handler):
    """Delete a comment made by the author on a particular post"""
    def post(self, comment_id="", parent_id=""):
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

            # only author can delete
            user_id = get_username(self)
            if comment_entity.author == user_id:
                delete_comment(comment_entity, parent_entity)
            else:
                self.error(401)
        else:
            self.error(400)
