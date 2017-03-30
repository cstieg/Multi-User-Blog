import models, handlers

class EditComment(handlers.Handler):
    """Edit a comment made by the author on a particular post"""
    @handlers.check_logged_in()
    @handlers.check_comment_exists()
    @handlers.check_user_owns_comment()
    def post(self, comment_entity):
        comment_text = handlers.sanitize(self.request.get('comment'))
        if not comment_text:
            self.error(400)
            return

        models.edit_comment(comment_entity, comment_text)
