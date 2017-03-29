from google.appengine.ext import db
import handlers

class DeletePost(handlers.Handler):
    """Deletes a post passed in from /deletepost/[postID]"""
    @handlers.check_logged_in
    @handlers.check_entry_exists
    def post(self, entry_id, entry_entity):
        # only author can delete
        if entry_entity.author == handlers.get_username(self):
            entry_entity.delete()
            self.redirect('/')
        else:
            self.error(401)