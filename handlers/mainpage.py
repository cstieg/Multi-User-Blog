from google.appengine.ext import db
import models, handlers


class MainPage(handlers.Handler):
    """Displays the main blog page from template mainpage.html"""
    @handlers.check_entry_exists(False)
    def get(self, entry_id='', entry_entity=None):
        if entry_id:
            entry_entities = [entry_entity]
        else:
            entry_entities = db.GqlQuery("SELECT* FROM BlogEntry ORDER BY posted DESC")

        # recreate query in list of dicts in order to be able to pass in 'liked' variable
        user_name = handlers.get_username(self)
        entry_list = []
        for entry_entity in entry_entities:
            entry_dict = handlers.to_dict(entry_entity)
            entry_dict['id'] = entry_entity.key().id()
            entry_dict['liked'] = models.post_is_liked(entry_entity, user_name)

            # add in comments
            comment_list = []
            for comment in models.Comment.all().ancestor(entry_entity).order('posted'):
                comment_dict = handlers.to_dict(comment)
                comment_dict['id'] = comment.key().id()
                comment_dict['liked'] = models.comment_is_liked(comment, user_name)
                comment_list.append(comment_dict)

            entry_dict['comments'] = comment_list

            entry_list.append(entry_dict)

        self.render('mainpage.html', blogEntries=entry_list, username=handlers.get_username(self))

