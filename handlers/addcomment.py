import json
import models, handlers

class AddComment(handlers.Handler):
    """Add a comment to a particular post"""
    @handlers.check_logged_in
    @handlers.check_entry_exists
    @handlers.check_user_owns_entry
    def post(self, entry_entity):
        comment_text = handlers.sanitize(self.request.get('comment'))
        if not comment_text:
            self.error(400)
            return

        user_id = handlers.get_username(self)
        new_comment_entity = models.add_comment(entry_entity, comment_text, user_id)
        self.response.out.write(json.dumps(new_comment_entity))
