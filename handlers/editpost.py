import time
from google.appengine.ext import db
import handlers

class EditPost(handlers.Handler):
    """Replaces the blog text with the text passed in from /editpost/[postid]"""
    @handlers.check_logged_in
    @handlers.check_entry_exists
    @handlers.check_user_owns_entry
    def get(self, entry_id, entry_entity):
        """Render template for editing entry"""
        self.render('edit.html', postID=entry_id, entry=entry_entity.entry, title=entry_entity.title, username=handlers.get_username(self))

    @handlers.check_logged_in
    @handlers.check_entry_exists
    @handlers.check_user_owns_entry
    def post(self, entry_id, entry_entity):
        """Accept edited entry"""
        title = handlers.sanitize(self.request.get('subject'))
        entry = handlers.sanitize(self.request.get('content'))

        # validate input
        if title and entry:
            entry_entity.title = title
            entry_entity.entry = entry
            db.put(entry_entity)

            # workaround to wait for eventual consistency in datastore
            # so as not to redirect back to home page before updating
            while entry_entity.title != title or entry_entity.entry != entry:
                time.sleep(0.01)

            self.redirect('/')
        else:
            self.error(400)