import os
import time
import webapp2
import jinja2
import re
import logging
from google.appengine.ext import db
import hashlib

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader(template_dir))

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **kw):
        t = jinja_env.get_template(template)
        return t.render(kw)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class BlogEntry(db.Model):
    title = db.StringProperty(required=True, indexed=True)
    entry = db.TextProperty(required=True)
    author = db.StringProperty(required=True, indexed=True)
    posted = db.DateTimeProperty(auto_now_add=True, indexed=True)
    likes = db.IntegerProperty(default=0, indexed=True)
    comments = db.IntegerProperty(default=0, indexed=True)

class Comment(db.Model):
    blogEntryID = db.IntegerProperty(required=True, indexed=True)
    comment = db.TextProperty(required=True)
    author = db.StringProperty(required=True, indexed=True)
    posted = db.DateTimeProperty(auto_now_add=True, indexed=True)
    likes = db.IntegerProperty()
    
class PostLike(db.Model):
    blogEntryID = db.IntegerProperty(required=True, indexed=True)
    liker = db.StringProperty(required=True, indexed=True)
    likeTime = db.DateTimeProperty(auto_now_add=True)
    

class User(db.Model):
    username = db.StringProperty(required=True, indexed=True)
    password = db.StringProperty(required=True, indexed=True)
    signedUp = db.DateTimeProperty(auto_now_add=True, indexed=True)

class MainPage(Handler):
    def get(self, q=""):       
        if q:
            entryKey = db.Key.from_path('BlogEntry', int(q))
            if not entryKey:
                self.error(404)
                return
            blogEntries = [db.get(entryKey)]
        else:
            blogEntries = db.GqlQuery("SELECT* FROM BlogEntry ORDER BY posted DESC")
    
        # recreate query in list of objects in order to be able to pass in 'liked' variable    
        userName = getUsername(self)
        if userName:
            entryObjects = []
            for blogEntry in blogEntries:
                entryObject = {}
                for field in blogEntry.properties():
                    entryObject[field] = getattr(blogEntry, field)
                entryObject['id'] = blogEntry.key().id() 
                entryObject['liked'] = postIsLiked(blogEntry, userName)
                entryObjects.append(entryObject)
            blogEntries = entryObjects
        
        self.render("mainpage.html", blogEntries=blogEntries, username=getUsername(self))
        
class Compose(Handler):
    def get(self):
        if not validUserLogin(self):
            self.redirect("/login?caller=newpost")
        entryMessage = "Type entry here."
        self.render("compose.html", entry=entryMessage, username=getUsername(self))

    def post(self):
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
            
class LikePost(Handler):
    """Adds a user like and increments like count for post"""
    def post(self, q=""):
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
            
            # author cannot like
            liker = getUsername(self)
            if liker == blogEntry.author:
                self.error(401)
                return
            
            if postIsLiked(blogEntry, liker):
                # forbidden to like twice
                self.error(403)
                return
            
            likePost(blogEntry, liker)
            
        else:
            self.error(400)
          
                
class UnlikePost(Handler):
    """Cancels a user like and decrements like count for post"""
    def post(self, q=""):
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

            liker = getUsername(self)
            if not postIsLiked(blogEntry, liker):
                # cannot unlike if not liked
                self.error(403)
                return
             
            unlikePost(blogEntry, liker)
            
        else:
            self.error(400)
            
class Signup(Handler):
    def get(self):
        self.render("signup.html")
        
    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        # check inputs against regex
        username_re = re.compile("^[a-zA-z0-9_-]{3,20}$")
        username_invalid = not username_re.match(username)

        password_re = re.compile("^.{3,20}$")
        password_invalid = not password_re.match(password)

        verify_invalid = (password != verify)

        email_re = re.compile("^[\S]+@[\S]+.[\S]+$")
        email_invalid = email and not email_re.match(email)

        invalid_input = username_invalid or password_invalid or verify_invalid or email_invalid

        if invalid_input:
            self.render("signup.html", username_invalid=username_invalid,
                                    password_invalid=password_invalid,
                                    verify_invalid=verify_invalid,
                                    email_invalid=email_invalid,
                                    invalid_input=invalid_input,
                                    old_username=username,
                                    old_email=email)
        else:
            usersWithSameName = db.GqlQuery("SELECT * FROM User WHERE username = '%s'" % username)
            if usersWithSameName.count() > 0:
                
                self.render("signup.html", username_already_taken=True,
                                            old_username=username,
                                            old_email=email)
            else:
                newUser = User(username=username, password=password)
                newUser.put()
                self.response.set_cookie('username', username, max_age=60 * 60 * 24)
                self.redirect('/newpost')
                self.render("success.html", username=username)


class Login(Handler):
    def get(self):
        caller = self.request.get('caller')
        self.render("login.html", caller=caller)

    def post(self):
        caller = self.request.get('caller')
        username = self.request.get("username")
        password = self.request.get("password")

        # check username and password
        if isValidUser(username, password):
            # success, redirect to calling page
            logout(self)
            self.response.set_cookie('username', username, max_age=60 * 60 * 24)
            self.response.set_cookie('password', password)
            self.redirect("/" + caller)

        else:
            self.render("login.html", login_error=True, caller=caller)

class Logout(Handler):
    def get(self):
        logout(self)
        self.redirect('/')

def validUserLogin(handler):
    username = handler.request.cookies.get("username")
    password = handler.request.cookies.get("password")
    return isValidUser(username, password)

def isValidUser(username, password):
    return username and password and db.GqlQuery("SELECT * FROM User WHERE username ='%s' AND password = '%s'" % (username, password)).count() == 1

def getUsername(handler):
    if validUserLogin(handler):
        return handler.request.cookies.get("username")
    return ""


def logout(handler):
    handler.response.delete_cookie('username')
    handler.response.delete_cookie('password')

def format_date(date):
    return date.strftime("%c")
jinja_env.filters['date'] = format_date

def saltedHash(text, salt):
    return hashlib.sha256(text + salt).hexdigest()

def saltedHexString(text, salt):
    return saltedHash(text, salt) + "," + salt

@db.transactional(xg=True)
def likePost(blogEntry, liker):
    """Adds a PostLike entity and increments the like count for the BlogEntry entity"""
    newLike = PostLike(parent=blogEntry, blogEntryID=blogEntry.key().id(), liker=liker)
    newLike.put()
    
    blogEntry.likes += 1
    blogEntry.put()
    
@db.transactional(xg=True)
def unlikePost(blogEntry, unliker):
    """Deletes a PostLike entity and decrements the like count for the BlogEntry entity"""
    likesQuery = PostLike.all()
    likesQuery.ancestor(blogEntry)
    likesQuery.filter('liker =', unliker)
    newLike = likesQuery.get()
    newLike.delete()
    
    blogEntry.likes -= 1
    blogEntry.put()
    

def postIsLiked(blogEntry, likerID):
    blogEntryID = str(blogEntry.key().id())
    likesQuery = db.GqlQuery("SELECT* FROM PostLike WHERE blogEntryID = %s AND liker = '%s'" % (blogEntryID, likerID))
    return (likesQuery.count() > 0)
    
app = webapp2.WSGIApplication([('/', MainPage),
                               ('/([0-9]+)', MainPage),
                               ('/newpost', Compose),
                               ('/signup', Signup),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/deletepost/([0-9]+)', DeletePost),
                               ('/editpost/([0-9]+)', EditPost),
                               ('/likepost/([0-9]+)', LikePost),
                               ('/unlikepost/([0-9]+)', UnlikePost)
                               ], debug=True)


