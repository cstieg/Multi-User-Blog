from google.appengine.ext import db
from handlers import Handler, valid_user_login, get_username

class DeletePost(Handler):
    """Deletes a post passed in from /deletepost/[postID]"""
    def post(self, entry_id=""):
        # check to make sure valid login
        if not valid_user_login(self):
            self.redirect("/login")
        if entry_id:
            # query post by id passed in
            entry_key = db.Key.from_path('BlogEntry', int(entry_id))
            if not entry_key:
                self.error(404)
                return
            entry_entity = db.get(entry_key)
            # only author can delete
            if entry_entity.author == get_username(self):
                entry_entity.delete()
                self.redirect("/")
            else:
                self.error(401)
        else:
            # if post id not found, it is a bad request
            self.error(400)
