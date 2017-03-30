from webapp2_extras import json
import models
import handlers


class AddComment(handlers.Handler):
    """Add a comment to a particular post"""
    @handlers.check_logged_in()
    @handlers.check_entry_exists()
    @handlers.check_user_owns_entry()
    def post(self, entry_entity):
        comment_text = handlers.sanitize(self.request.get('comment'))
        if not comment_text:
            self.error(400)
            return

        user_id = handlers.get_username(self)
        new_comment_entity = models.add_comment(entry_entity, comment_text, user_id)
        new_comment_dict = handlers.to_dict(new_comment_entity)
        new_comment_dict['liked'] = False
        self.response.out.write(json.encode(new_comment_dict))
