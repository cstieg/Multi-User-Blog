import models, handlers

class LikePost(handlers.Handler):
    """Adds a user like and increments like count for post"""
    @handlers.check_logged_in()
    @handlers.check_entry_exists()
    @handlers.check_user_owns_entry(False)  # author cannot like own entry
    def post(self, entry_entity):
        liker = handlers.get_username(self)
        if models.post_is_liked(entry_entity, liker):
            # forbidden to like twice
            self.error(403)
            return

        models.like_post(entry_entity, liker)


class UnlikePost(handlers.Handler):
    """Cancels a user like and decrements like count for post"""
    @handlers.check_logged_in()
    @handlers.check_entry_exists()
    def post(self, entry_entity):
        liker = handlers.get_username(self)
        if not models.post_is_liked(entry_entity, liker):
            # cannot unlike if not liked
            self.error(403)
            return

        models.unlike_post(entry_entity, liker)
