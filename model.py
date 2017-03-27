
import hashlib

from utils import sanitize
from google.appengine.ext import db

from handler import jinja_env

class BlogEntry(db.Model):
    """A representation of the main entries of the blog"""
    title = db.StringProperty(required=True, indexed=True)
    entry = db.TextProperty(required=True)
    author = db.StringProperty(required=True, indexed=True)
    posted = db.DateTimeProperty(auto_now_add=True, indexed=True)
    likeCount = db.IntegerProperty(default=0, indexed=True)
    commentCount = db.IntegerProperty(default=0, indexed=True)

class Comment(db.Model):
    """Comments subordinate to the main entries of the blog"""
    blogEntryID = db.IntegerProperty(required=True, indexed=True)
    comment = db.TextProperty(required=True)
    author = db.StringProperty(required=True, indexed=True)
    posted = db.DateTimeProperty(auto_now_add=True, indexed=True)
    likeCount = db.IntegerProperty(default=0, indexed=True)

class PostLike(db.Model):
    """Reader likes on the main entries of the blog"""
    blogEntryID = db.IntegerProperty(required=True, indexed=True)
    liker = db.StringProperty(required=True, indexed=True)
    likeTime = db.DateTimeProperty(auto_now_add=True)

class CommentLike(db.Model):
    """Reader likes on the subordinate comments"""
    commentID = db.IntegerProperty(required=True, indexed=True)
    liker = db.StringProperty(required=True, indexed=True)
    likeTime = db.DateTimeProperty(auto_now_add=True)

class User(db.Model):
    """Users registered to create content and comment and like on the blog"""
    username = db.StringProperty(required=True, indexed=True)
    password = db.StringProperty(required=True, indexed=True)
    signedUp = db.DateTimeProperty(auto_now_add=True, indexed=True)

@db.transactional(xg=True)
def likePost(entryEntity, liker):
    """Adds a PostLike entity and increments the like count for the BlogEntry entity"""
    newLikeEntity = PostLike(parent=entryEntity, blogEntryID=entryEntity.key().id(), liker=liker)
    newLikeEntity.put()

    entryEntity.likeCount += 1
    entryEntity.put()

@db.transactional(xg=True)
def unlikePost(entryEntity, unliker):
    """Deletes a PostLike entity and decrements the likeEntity count for the BlogEntry entity"""
    likesQuery = PostLike.all()
    likesQuery.ancestor(entryEntity)
    likesQuery.filter('liker =', unliker)
    likeEntity = likesQuery.get()
    likeEntity.delete()

    entryEntity.likeCount -= 1
    entryEntity.put()

def postIsLiked(entryEntity, likerID):
    """Returns true if a given user (likerID) has liked a given entryEntity"""
    entryID = str(entryEntity.key().id())
    likesQuery = db.GqlQuery("SELECT* FROM PostLike WHERE entryID = %s AND liker = '%s'" % (entryID, likerID))
    return (likesQuery.count() > 0)

def commentIsLiked(commentEntity, likerID):
    """Returns true if a given user (likerID) has liked a given comment"""
    commentID = str(commentEntity.key().id())
    likesQuery = CommentLike.all()
    likesQuery.ancestor(commentEntity)
    likesQuery.filter('liker =', likerID)
    return (likesQuery.count() > 0)

@db.transactional(xg=True)
def likeComment(commentEntity, liker):
    """Adds a CommentLike entity and increments the like count for the Comment entity"""
    newLikeEntity = CommentLike(parent=commentEntity, commentID=commentEntity.key().id(), liker=liker)
    newLikeEntity.put()

    commentEntity.likeCount += 1
    commentEntity.put()

@db.transactional(xg=True)
def unlikeComment(commentEntity, unliker):
    """Deletes a CommentLike entity and decrements the likeEntity count for the Comment entity"""
    likesQuery = CommentLike.all()
    likesQuery.ancestor(commentEntity)
    likesQuery.filter('liker =', unliker)
    likeEntity = likesQuery.get()
    likeEntity.delete()

    commentEntity.likeCount -= 1
    commentEntity.put()

@db.transactional(xg=True)
def addComment(entryEntity, commentText, commenterID):
    """Adds a comment of commentText by user commenterID to a entryEntity
    and increments the comment count on the entry"""
    newCommentEntity = Comment(parent=entryEntity, blogEntryID=entryEntity.key().id(), author=commenterID, comment=commentText)
    newCommentEntity.put()

    entryEntity.commentCount += 1
    entryEntity.put()

    return newCommentEntity

@db.transactional(xg=True)
def deleteComment(commentEntity, parentEntity):
    """Deletes a comment on a blog entry and decrements the comment count on the entry"""
    parentEntity.commentCount -= 1
    parentEntity.put()

    commentEntity.delete()

def editComment(commentEntity, newCommentText):
    """Edits a comment on a blog entry"""
    commentEntity.comment = newCommentText
    commentEntity.put()

def validUserLogin(handler):
    """Returns true if a valid user is logged in, false otherwise"""
    username = handler.request.cookies.get('username')
    password = handler.request.cookies.get('password')
    if not username or not password:
        return False
    return isValidUser(sanitize(username), sanitize(password))

def isValidUser(username, password):
    """Returns true if a given username and password constitutes a valid login"""
    return username and password and db.GqlQuery("SELECT * FROM User WHERE username ='%s' AND password = '%s'" % (username, password)).count() == 1

def getUsername(handler):
    """Returns the username stored in cookies"""
    if validUserLogin(handler):
        return sanitize(handler.request.cookies.get('username'))
    return ""

def logout(handler):
    """Logs the current user out by deleting login cookies"""
    handler.response.delete_cookie('username')
    handler.response.delete_cookie('password')

def formatDate(date):
    """Specifies the date format returned to frontend"""
    return date.strftime("%c")

def saltedHash(text, salt):
    """Converts a password into a salted hash"""
    return hashlib.sha256(text + salt).hexdigest()

def saltedHexString(text, salt):
    """Converts a password into a salted hash, and returns the hash + the salt"""
    return saltedHash(text, salt) + "," + salt

jinja_env.filters['date'] = formatDate