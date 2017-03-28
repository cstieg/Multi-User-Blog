import hashlib
from google.appengine.ext import db

class User(db.Model):
    """Users registered to create content and comment and like on the blog"""
    username = db.StringProperty(required=True, indexed=True)
    password = db.StringProperty(required=True, indexed=True)
    signedUp = db.DateTimeProperty(auto_now_add=True, indexed=True)


def is_valid_user(username, password):
    """Returns true if a given username and password constitutes a valid login"""
    return username and password and \
        db.GqlQuery("SELECT * FROM User WHERE username ='%s' AND password = '%s'" \
                    % (username, password)).count() == 1


def salted_hash(text, salt):
    """Converts a password into a salted hash"""
    return hashlib.sha256(text + salt).hexdigest()


def salted_hex_string(text, salt):
    """Converts a password into a salted hash, and returns the hash + the salt"""
    return salted_hash(text, salt) + "," + salt
