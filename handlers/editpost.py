import time
from google.appengine.ext import db
import handlers

class EditPost(handlers.Handler):
    """Replaces the blog text with the text passed in from /editpost/[postid]"""
    @handlers.check_logged_in
    def get(self, entry_id=''):
        """Render template for editing entry"""
        if entry_id:
            # query entryEntity by id passed in
            entryKey = db.Key.from_path('BlogEntry', int(entry_id))
            entryEntity = db.get(entryKey)

            self.render('edit.html', postID=entry_id, entry=entryEntity.entry, title=entryEntity.title, username=handlers.get_username(self))
        else:
            self.error(400)

    @handlers.check_logged_in
    def post(self, entry_id=''):
        """Accept edited entry"""
        if entry_id:
            # query post by id passed in
            entry_key = db.Key.from_path('BlogEntry', int(entry_id))

            if not entry_key:
                self.error(400)
                return
            entry_entity = db.get(entry_key)

            # only author can delete
            if entry_entity.author == handlers.get_username(self):
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

                    self.redirect("/")
                else:
                    self.error(400)
            else:
                # unauthorized
                self.error(401)
        else:
            # if post id not found, it is a bad request
            self.error(400)
