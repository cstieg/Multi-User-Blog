import handlers
import models

class DeletePost(handlers.Handler):
    """Deletes a post passed in from /deletepost/[postID]"""
    @handlers.check_logged_in()
    @handlers.check_entry_exists()
    @handlers.check_user_owns_entry()
    def post(self, entry_entity):
        models.delete_comments(entry_entity)
        models.delete_likes(entry_entity)
        entry_entity.delete()
        self.redirect('/')
