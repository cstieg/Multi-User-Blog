import handlers

class DeleteComment(handlers.Handler):
    """Delete a comment made by the author on a particular post"""
    @handlers.check_logged_in()
    @handlers.check_comment_exists()
    @handlers.check_user_owns_comment()
    def post(self, comment_entity):
        comment_entity.delete()
