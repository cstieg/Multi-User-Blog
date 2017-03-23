import time
from google.appengine.ext import db

from handler import Handler
from model import getUsername, validUserLogin, postIsLiked, BlogEntry, Comment
from utils import to_dict


class MainPage(Handler):
    """Displays the main blog page from template mainpage.html"""
    def get(self, q=""):
        if q:
            entryKey = db.Key.from_path('BlogEntry', int(q))
            if not entryKey:
                self.error(404)
                return
            blogEntries = [db.get(entryKey)]
        else:
            blogEntries = db.GqlQuery("SELECT* FROM BlogEntry ORDER BY posted DESC")

        # recreate query in list of dicts in order to be able to pass in 'liked' variable
        userName = getUsername(self)
        entryList = []
        for blogEntry in blogEntries:
            entryDict = to_dict(blogEntry)
            entryDict['id'] = blogEntry.key().id()       
            entryDict['liked'] = postIsLiked(blogEntry, userName)
                
            # add in comments
            commentList = []
            for comment in Comment.all().ancestor(blogEntry).order('posted'):
                commentDict = to_dict(comment)
                commentDict['id'] = comment.key().id()
                #commentObject['liked'] = commentIsLiked(comment, userName)
                commentList.append(commentDict)
                
            entryDict['comments'] = commentList
            
            entryList.append(entryDict)

        self.render("mainpage.html", blogEntries=entryList, username=getUsername(self))
        
class Compose(Handler):
    """handler for new entry"""
    def get(self):
        """Render compose new entry template"""
        if not validUserLogin(self):
            self.redirect("/login?caller=newpost")
        entryMessage = "Type entry here."
        self.render("compose.html", entry=entryMessage, username=getUsername(self))

    def post(self):
        """Accept new entry"""
        if not validUserLogin(self):
            self.redirect("/login")
        title = self.request.get("subject")
        entry = self.request.get("content")
        username = self.request.cookies.get("username")

        if title and entry:
            newEntry = BlogEntry(title=title, entry=entry, author=username)
            newEntry.put()
            self.redirect("/" + str(newEntry.key().id()))
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
            blogEntry = db.get(entryKey)
            # only author can delete
            if blogEntry.author == getUsername(self):
                blogEntry.delete()
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
            # query post by id passed in
            entryKey = db.Key.from_path('BlogEntry', int(q))
            post = db.get(entryKey)
            
            self.render("edit.html", postID=q, entry=post.entry, title=post.title, username=getUsername(self))
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
            blogEntry = db.get(entryKey)

            # only author can delete
            if blogEntry.author == getUsername(self):
                title = self.request.get("subject")
                entry = self.request.get("content")

                # validate input
                if title and entry:
                    blogEntry.title = title
                    blogEntry.entry = entry
                    db.put(blogEntry)

                    # workaround to wait for eventual consistency in datastore
                    # so as not to redirect back to home page before updating
                    while blogEntry.title != title or blogEntry.entry != entry:
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
