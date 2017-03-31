import hashlib
import random
from google.appengine.ext import db

class User(db.Model):
    """Users registered to create content and comment and like on the blog"""
    username = db.StringProperty(required=True, indexed=True)
    password = db.StringProperty(required=True, indexed=True)
    signedUp = db.DateTimeProperty(auto_now_add=True, indexed=True)


def is_valid_user(username, password):
    """Returns true if a given username and password constitutes a valid login"""
    if not username or not password:
        return False

    user_query = User.all()
    user_query.filter('username =', username)
    if user_query.count() != 1:
        return False

    user = user_query.get()
    user_pwd_salt = user.password.split(',')[1]
    return user.password == salted_hex_string(password, user_pwd_salt)


def hashed_salted_password(password):
    """Returns hashed, salted password, with its salt after a comma"""
    return salted_hex_string(password, random_text())

def salted_hex_string(text, salt):
    """Converts a password into a salted hash, and returns the hash + the salt"""
    return salted_hash(text, salt) + "," + salt

def salted_hash(text, salt):
    """Converts a password into a salted hash"""
    return hashlib.sha256(text + salt).hexdigest()

def random_text(text_length=32):
    """Produces random characters of specified length for use in password or text"""
    possible_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!#$%()*+-/:;<=>?@[\]^_`{|}~'
    text = ''
    for _ in range(text_length):
        text += random.SystemRandom().choice(possible_chars)
    return text
