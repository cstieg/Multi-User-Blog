from google.appengine.ext import db
from handlers import Handler, to_dict, get_username
from models import Comment, post_is_liked, comment_is_liked


class MainPage(Handler):
    """Displays the main blog page from template mainpage.html"""
    def get(self, entry_id=""):
        if entry_id:
            entry_key = db.Key.from_path('BlogEntry', int(entry_id))
            if not entry_key:
                self.error(404)
                return
            entry_entities = [db.get(entry_key)]
        else:
            entry_entities = db.GqlQuery("SELECT* FROM BlogEntry ORDER BY posted DESC")

        # recreate query in list of dicts in order to be able to pass in 'liked' variable
        user_name = get_username(self)
        entry_list = []
        for entry_entity in entry_entities:
            entry_dict = to_dict(entry_entity)
            entry_dict['id'] = entry_entity.key().id()
            entry_dict['liked'] = post_is_liked(entry_entity, user_name)

            # add in comments
            comment_list = []
            for comment in Comment.all().ancestor(entry_entity).order('posted'):
                comment_dict = to_dict(comment)
                comment_dict['id'] = comment.key().id()
                comment_dict['liked'] = comment_is_liked(comment, user_name)
                comment_list.append(comment_dict)

            entry_dict['comments'] = comment_list

            entry_list.append(entry_dict)

        self.render('mainpage.html', blogEntries=entry_list, username=get_username(self))

