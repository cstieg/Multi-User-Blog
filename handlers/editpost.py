import time
from google.appengine.ext import db
from handlers import Handler, sanitize, valid_user_login, get_username

class EditPost(Handler):
    """Replaces the blog text with the text passed in from /editpost/[postid]"""
    def get(self, entry_id=""):
        """Render template for editing entry"""
        if not valid_user_login(self):
            self.redirect("/login")
        if entry_id:
            # query entryEntity by id passed in
            entryKey = db.Key.from_path('BlogEntry', int(entry_id))
            entryEntity = db.get(entryKey)

            self.render("edit.html", postID=entry_id, entry=entryEntity.entry, title=entryEntity.title, username=get_username(self))
        else:
            self.error(400)

    def post(self, entry_id=""):
        """Accept edited entry"""
        # check to make sure valid login
        if not valid_user_login(self):
            self.redirect("/login")
        if entry_id:
            # query post by id passed in
            entry_key = db.Key.from_path('BlogEntry', int(entry_id))

            if not entry_key:
                self.error(400)
                return
            entry_entity = db.get(entry_key)

            # only author can delete
            if entry_entity.author == get_username(self):
                title = sanitize(self.request.get("subject"))
                entry = sanitize(self.request.get("content"))

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
