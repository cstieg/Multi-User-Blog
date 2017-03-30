from google.appengine.ext import db
import models

class PostLike(db.Model):
    """Reader likes on the main entries of the blog"""
    blogEntry = db.ReferenceProperty(models.BlogEntry, collection_name='likes')
    liker = db.StringProperty(required=True, indexed=True)
    likeTime = db.DateTimeProperty(auto_now_add=True)

def like_post(entry_entity, liker):
    """Adds a PostLike entity"""
    new_like_entity = PostLike(blogEntry=entry_entity, liker=liker)
    new_like_entity.put()

def unlike_post(entry_entity, unliker):
    """Deletes a PostLike entity"""
    likes_query = PostLike.all()
    likes_query.filter('liker =', unliker)
    like_entity = likes_query.get()
    like_entity.delete()

def post_is_liked(entry_entity, liker):
    """Returns true if a given user (liker) has liked a given entry_entity"""
    likes_query = PostLike.all()
    likes_query.filter('liker =', liker)
    likes_query.filter('blogEntry =', entry_entity)
    return likes_query.count() > 0

def like_count(entry_entity):
    """Returns the number of likes for a blog entry"""
    likes_query = PostLike.all()
    likes_query.filter('blogEntry =', entry_entity)
    return likes_query.count()

def delete_likes(entry_entity):
    """Deletes all likes for a blog entry"""
    likes_query = PostLike.all()
    likes_query.filter('blogEntry =', entry_entity)
    for like in likes_query:
        like.delete()