"""Handlers for user signup and login"""
import re

from google.appengine.ext import db

from handler import Handler
from model import User, isValidUser, logout

class Signup(Handler):
    """Allows a user new user to register to post, comment and like"""
    def get(self):
        """Renders the signup page"""
        self.render("signup.html")

    def post(self):
        """Handles the signup submission"""
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
            # re-render the signup page with info submitted thus far
            self.render("signup.html", username_invalid=username_invalid,
                                    password_invalid=password_invalid,
                                    verify_invalid=verify_invalid,
                                    email_invalid=email_invalid,
                                    invalid_input=invalid_input,
                                    old_username=username,
                                    old_email=email)
        else:
            # Check to make sure no one has already registered with that username
            usersWithSameName = db.GqlQuery("SELECT * FROM User WHERE username = '%s'" % username)
            if usersWithSameName.count() > 0:

                self.render("signup.html", username_already_taken=True,
                                            old_username=username,
                                            old_email=email)
            else:
                # Add User entity to datastore
                newUser = User(username=username, password=password)
                newUser.put()
                self.response.set_cookie('username', username, max_age=60 * 60 * 24)
                self.redirect('/newpost')
                self.render("success.html", username=username)

class Login(Handler):
    """Allows registered user to login"""
    def get(self):
        """Renders login page"""
        caller = self.request.get('caller')
        self.render("login.html", caller=caller)

    def post(self):
        """Accepts login info from login page and sets cookies"""
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
            # Re-render login page if invalid login
            self.render("login.html", login_error=True, caller=caller)

class Logout(Handler):
    """Logs out user"""
    def get(self):
        logout(self)
        self.redirect('/')
