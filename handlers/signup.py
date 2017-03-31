
import re
from google.appengine.ext import db
import models
import handlers

class Signup(handlers.Handler):
    """Allows a user new user to register to post, comment and like"""
    def get(self):
        """Renders the signup page"""
        self.render('signup.html')

    def post(self):
        """Handles the signup submission"""
        username = handlers.sanitize(self.request.get('username'))
        password = handlers.sanitize(self.request.get('password'))
        verify = handlers.sanitize(self.request.get('verify'))
        email = handlers.sanitize(self.request.get('email'))

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
            self.render('signup.html', username_invalid=username_invalid,
                                    password_invalid=password_invalid,
                                    verify_invalid=verify_invalid,
                                    email_invalid=email_invalid,
                                    invalid_input=invalid_input,
                                    old_username=username,
                                    old_email=email)
        else:
            # Check to make sure no one has already registered with that username
            users_with_same_name_query = db.GqlQuery("SELECT * FROM User WHERE username = '%s'" % username)
            if users_with_same_name_query.count() > 0:

                self.render('signup.html', username_already_taken=True,
                                            old_username=username,
                                            old_email=email)
            else:
                # Add User entity to datastore
                hashSaltPassword = models.hashed_salted_password(password)
                new_user_entity = models.User(username=username, password=hashSaltPassword)
                new_user_entity.put()
                self.response.set_cookie('username', username, max_age=60 * 60 * 24)
                self.redirect('/newpost')
                self.render('success.html', username=username)
