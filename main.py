import os
import time
import webapp2
import jinja2
import re
from google.appengine.ext import db
import hashlib

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(autoescape = True, loader = jinja2.FileSystemLoader(template_dir))

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **kw):
        t = jinja_env.get_template(template)
        return t.render(kw)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class BlogEntry(db.Model):
    title = db.StringProperty(required = True)
    entry = db.TextProperty(required = True)
    author = db.TextProperty(required = True)
    posted = db.DateTimeProperty(auto_now_add = True)
    likes = db.IntegerProperty(default = 0)
    comments = db.IntegerProperty(default = 0)

class Comment(db.Model):
    blogEntryID = db.IntegerProperty(required = True)
    comment = db.TextProperty(required = True)
    author = db.TextProperty(required = True)
    posted = db.DateTimeProperty(auto_now_add = True)
    likes = db.IntegerProperty()

class User(db.Model):
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    signedUp = db.DateTimeProperty(auto_now_add = True)

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

class Signup(Handler):
    def get(self):
        self.render("signup.html")
        
    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        #check inputs against regex
        username_re = re.compile("^[a-zA-z0-9_-]{3,20}$")
        username_invalid = not username_re.match(username)

        password_re = re.compile("^.{3,20}$")
        password_invalid = not password_re.match(password)

        verify_invalid = (password != verify)

        email_re = re.compile("^[\S]+@[\S]+.[\S]+$")
        email_invalid = email and not email_re.match(email)

        invalid_input = username_invalid or password_invalid or verify_invalid or email_invalid

        if invalid_input:
            self.render("signup.html", username_invalid = username_invalid,
                                    password_invalid = password_invalid,
                                    verify_invalid = verify_invalid,
                                    email_invalid = email_invalid,
                                    invalid_input = invalid_input,
                                    old_username = username,
                                    old_email = email)
        else:
            usersWithSameName = db.GqlQuery("SELECT * FROM User WHERE username = '%s'" % username)
            if usersWithSameName.count() > 0:
                
                self.render("signup.html",  username_already_taken = True,
                                            old_username = username,
                                            old_email = email)
            else:
                newUser = User(username=username, password=password)
                newUser.put()
                self.response.set_cookie('username', username, max_age=60*60*24)
                self.response.redirect('/newpost')
                self.render("success.html", username = username)


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
            self.response.set_cookie('username', username, max_age=60*60*24)
            self.response.set_cookie('password', password)
            self.redirect("/" + caller)

        else:
            self.render("login.html", login_error = True, caller=caller)

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

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/([0-9]+)', MainPage),
                               ('/newpost', Compose),
                               ('/signup', Signup),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/deletepost/([0-9]+)', DeletePost),
                               ('/editpost/([0-9]+)', EditPost)],
                                debug=True)


