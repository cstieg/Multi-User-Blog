from google.appengine.ext import db
import handlers

class DeletePost(handlers.Handler):
    """Deletes a post passed in from /deletepost/[postID]"""
    @handlers.check_logged_in
    def post(self, entry_id=''):
        if entry_id:
            # query post by id passed in
            entry_key = db.Key.from_path('BlogEntry', int(entry_id))
            if not entry_key:
                self.error(404)
                return
            entry_entity = db.get(entry_key)
            # only author can delete
            if entry_entity.author == handlers.get_username(self):
                entry_entity.delete()
                self.redirect("/")
            else:
                self.error(401)
        else:
            # if post id not found, it is a bad request
            self.error(400)
