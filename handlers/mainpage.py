from google.appengine.ext import db
import handlers

class MainPage(handlers.Handler):
    """Displays the main blog page from template mainpage.html"""
    @handlers.check_entry_exists(False)
    def get(self, entry_entity=None):
        if entry_entity:
            entry_entities = [entry_entity]
        else:
            entry_entities = db.GqlQuery("SELECT* FROM BlogEntry ORDER BY posted DESC")

        # recreate query in list of dicts in order to be able to pass in 'liked' variable
        user_name = handlers.get_username(self)
        self.render('mainpage.html', blogEntries=entry_entities, username=user_name)
