import logging
import hashlib
from google.appengine.ext import db

from handler import jinja_env

class BlogEntry(db.Model):
    title = db.StringProperty(required=True, indexed=True)
    entry = db.TextProperty(required=True)
    author = db.StringProperty(required=True, indexed=True)
    posted = db.DateTimeProperty(auto_now_add=True, indexed=True)
    likeCount = db.IntegerProperty(default=0, indexed=True)
    commentCount = db.IntegerProperty(default=0, indexed=True)

class Comment(db.Model):
    blogEntryID = db.IntegerProperty(required=True, indexed=True)
    comment = db.TextProperty(required=True)
    author = db.StringProperty(required=True, indexed=True)
    posted = db.DateTimeProperty(auto_now_add=True, indexed=True)
    likeCount = db.IntegerProperty(default=0, indexed=True)
    
class PostLike(db.Model):
    blogEntryID = db.IntegerProperty(required=True, indexed=True)
    liker = db.StringProperty(required=True, indexed=True)
    likeTime = db.DateTimeProperty(auto_now_add=True)

class CommentLike(db.Model):
    commentID = db.IntegerProperty(required=True, indexed=True)
    liker = db.StringProperty(required=True, indexed=True)
    likeTime = db.DateTimeProperty(auto_now_add=True)

class User(db.Model):
    username = db.StringProperty(required=True, indexed=True)
    password = db.StringProperty(required=True, indexed=True)
    signedUp = db.DateTimeProperty(auto_now_add=True, indexed=True)

@db.transactional(xg=True)
def likePost(blogEntry, liker):
    """Adds a PostLike entity and increments the like count for the BlogEntry entity"""
    newLike = PostLike(parent=blogEntry, blogEntryID=blogEntry.key().id(), liker=liker)
    newLike.put()
    
    blogEntry.likeCount += 1
    blogEntry.put()
    
@db.transactional(xg=True)
def unlikePost(blogEntry, unliker):
    """Deletes a PostLike entity and decrements the like count for the BlogEntry entity"""
    likesQuery = PostLike.all()
    likesQuery.ancestor(blogEntry)
    likesQuery.filter('liker =', unliker)
    like = likesQuery.get()
    like.delete()
    
    blogEntry.likeCount -= 1
    blogEntry.put()
    
def postIsLiked(blogEntry, likerID):
    """Returns true if a given user (likerID) has liked a given blogEntry"""
    blogEntryID = str(blogEntry.key().id())
    likesQuery = db.GqlQuery("SELECT* FROM PostLike WHERE blogEntryID = %s AND liker = '%s'" % (blogEntryID, likerID))
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
    newLike = CommentLike(parent=commentEntity, commentID=commentEntity.key().id(), liker=liker)
    newLike.put()
    
    commentEntity.likeCount += 1
    commentEntity.put()

@db.transactional(xg=True)
def unlikeComment(commentEntity, unliker):
    """Deletes a CommentLike entity and decrements the like count for the Comment entity"""
    likesQuery = CommentLike.all()
    likesQuery.ancestor(commentEntity)
    likesQuery.filter('liker =', unliker)
    like = likesQuery.get()
    like.delete()
    
    commentEntity.likeCount -= 1
    commentEntity.put()

@db.transactional(xg=True)
def addComment(blogEntry, commentText, commenterID):
    """Adds a comment of commentText by user commenterID to a blogEntry
    and increments the comment count on the entry"""
    newComment = Comment(parent=blogEntry, blogEntryID=blogEntry.key().id(), author=commenterID, comment=commentText)
    newComment.put()
    
    blogEntry.commentCount += 1
    blogEntry.put()
    
    return newComment

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
    return commentEntity

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