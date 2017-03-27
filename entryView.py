
import time
from utils import sanitize
from google.appengine.ext import db

from handler import Handler
from model import getUsername, validUserLogin, postIsLiked, commentIsLiked, BlogEntry, Comment
from utils import to_dict


class MainPage(Handler):
    """Displays the main blog page from template mainpage.html"""
    def get(self, q=""):
        if q:
            entryKey = db.Key.from_path('BlogEntry', int(q))
            if not entryKey:
                self.error(404)
                return
            entryEntities = [db.get(entryKey)]
        else:
            entryEntities = db.GqlQuery("SELECT* FROM BlogEntry ORDER BY posted DESC")

        # recreate query in list of dicts in order to be able to pass in 'liked' variable
        userName = getUsername(self)
        entryList = []
        for entryEntity in entryEntities:
            entryDict = to_dict(entryEntity)
            entryDict['id'] = entryEntity.key().id()
            entryDict['liked'] = postIsLiked(entryEntity, userName)

            # add in comments
            commentList = []
            for comment in Comment.all().ancestor(entryEntity).order('posted'):
                commentDict = to_dict(comment)
                commentDict['id'] = comment.key().id()
                commentDict['liked'] = commentIsLiked(comment, userName)
                commentList.append(commentDict)

            entryDict['comments'] = commentList

            entryList.append(entryDict)

        self.render("mainpage.html", blogEntries=entryList, username=getUsername(self))

class Compose(Handler):
    """Handler for new entry"""
    def get(self):
        """Render compose new entry template"""
        if not validUserLogin(self):
            self.redirect("/login?caller=newpost")
        self.render("compose.html", entry="", username=getUsername(self))

    def post(self):
        """Accept new entry"""
        if not validUserLogin(self):
            self.redirect("/login")
        title = sanitize(self.request.get("subject"))
        entry = sanitize(self.request.get("content"))
        username = sanitize(self.request.cookies.get("username"))

        if title and entry:
            newEntryEntity = BlogEntry(title=title, entry=entry, author=username)
            newEntryEntity.put()
            self.redirect("/" + str(newEntryEntity.key().id()))
        else:
            if not title:
                error = "Must input title!"
            if not entry:
                error = "Must input blog entry content!"
            if not title and not entry:
                error = "Must input title and blog entry content!"
            self.render("compose.html", entry=entry, title=title, error=error, username=username)

class DeletePost(Handler):
    """Deletes a post passed in from /deletepost/[postID]"""
    def post(self, q=""):
        # check to make sure valid login
        if not validUserLogin(self):
            self.redirect("/login")
        if q:
            # query post by id passed in
            entryKey = db.Key.from_path('BlogEntry', int(q))
            if not entryKey:
                self.error(404)
                return
            entryEntity = db.get(entryKey)
            # only author can delete
            if entryEntity.author == getUsername(self):
                entryEntity.delete()
                self.redirect("/")
            else:
                self.error(401)
        else:
            # if post id not found, it is a bad request
            self.error(400)

class EditPost(Handler):
    """Replaces the blog text with the text passed in from /editpost/[postid]"""
    def get(self, q=""):
        """Render template for editing entry"""
        if not validUserLogin(self):
            self.redirect("/login")
        if q:
            # query entryEntity by id passed in
            entryKey = db.Key.from_path('BlogEntry', int(q))
            entryEntity = db.get(entryKey)

            self.render("edit.html", postID=q, entry=entryEntity.entry, title=entryEntity.title, username=getUsername(self))
        else:
            self.error(400)

    def post(self, q=""):
        """Accept edited entry"""
        # check to make sure valid login
        if not validUserLogin(self):
            self.redirect("/login")
        if q:
            # query post by id passed in
            entryKey = db.Key.from_path('BlogEntry', int(q))

            if not entryKey:
                self.error(400)
                return
            entryEntity = db.get(entryKey)

            # only author can delete
            if entryEntity.author == getUsername(self):
                title = sanitize(self.request.get("subject"))
                entry = sanitize(self.request.get("content"))

                # validate input
                if title and entry:
                    entryEntity.title = title
                    entryEntity.entry = entry
                    db.put(entryEntity)

                    # workaround to wait for eventual consistency in datastore
                    # so as not to redirect back to home page before updating
                    while entryEntity.title != title or entryEntity.entry != entry:
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
