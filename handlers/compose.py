from handlers import Handler, valid_user_login, get_username, sanitize
from models import BlogEntry

class Compose(Handler):
    """Handler for new entry"""
    def get(self):
        """Render compose new entry template"""
        if not valid_user_login(self):
            self.redirect("/login?caller=newpost")
        self.render("compose.html", entry="", username=get_username(self))

    def post(self):
        """Accept new entry"""
        if not valid_user_login(self):
            self.redirect("/login")
        title = sanitize(self.request.get("subject"))
        entry = sanitize(self.request.get("content"))
        username = sanitize(self.request.cookies.get("username"))

        if title and entry:
            new_entry_entity = BlogEntry(title=title, entry=entry, author=username)
            new_entry_entity.put()
            self.redirect("/" + str(new_entry_entity.key().id()))
        else:
            if not title:
                error = "Must input title!"
            if not entry:
                error = "Must input blog entry content!"
            if not title and not entry:
                error = "Must input title and blog entry content!"
            self.render("compose.html", entry=entry, title=title, error=error, username=username)
