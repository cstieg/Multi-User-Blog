from google.appengine.ext import db
from handlers import Handler, valid_user_login, get_username
from models import post_is_liked, like_post, unlike_post

class LikePost(Handler):
    """Adds a user like and increments like count for post"""
    def post(self, entry_id=""):
        # check to make sure valid login
        if not valid_user_login(self):
            self.redirect('/login')
        if entry_id:
            # query post by id passed in
            entryKey = db.Key.from_path('BlogEntry', int(entry_id))

            if not entryKey:
                self.error(400)
                return
            entry_entity = db.get(entryKey)

            # author cannot like
            liker = get_username(self)
            if liker == entry_entity.author:
                self.error(403)
                return

            if post_is_liked(entry_entity, liker):
                # forbidden to like twice
                self.error(403)
                return

            like_post(entry_entity, liker)

        else:
            self.error(400)


class UnlikePost(Handler):
    """Cancels a user like and decrements like count for post"""
    def post(self, entry_id=""):
        # check to make sure valid login
        if not valid_user_login(self):
            self.redirect('/login')
        if entry_id:
            # query post by id passed in
            entryKey = db.Key.from_path('BlogEntry', int(entry_id))

            if not entryKey:
                self.error(400)
                return
            entryEntity = db.get(entryKey)

            liker = get_username(self)
            if not post_is_liked(entryEntity, liker):
                # cannot unlike if not liked
                self.error(403)
                return

            unlike_post(entryEntity, liker)

        else:
            self.error(400)