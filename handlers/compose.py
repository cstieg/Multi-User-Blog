import models, handlers

class Compose(handlers.Handler):
    """Handler for new entry"""
    @handlers.check_logged_in('?caller=newpost')
    def get(self):
        """Render compose new entry template"""
        self.render('compose.html', entry='', username=handlers.get_username(self))

    @handlers.check_logged_in()
    def post(self):
        """Accept new entry"""
        # TODO: put these variables into entry dict
        title = handlers.sanitize(self.request.get('subject'))
        entry = handlers.sanitize(self.request.get('content'))
        username = handlers.sanitize(self.request.cookies.get('username'))

        if title and entry:
            new_entry_entity = models.BlogEntry(title=title, entry=entry, author=username)
            new_entry_entity.put()
            self.redirect("/" + str(new_entry_entity.key().id()))
        else:
            if not title:
                error = 'Must input title!'
            if not entry:
                error = 'Must input blog entry content!'
            if not title and not entry:
                error = 'Must input title and blog entry content!'
            self.render('compose.html', entry=entry, title=title, error=error, username=username)
