from google.appengine.ext import db

class CommentLike(db.Model):
    """Reader likes on the subordinate comments"""
    comment = db.IntegerProperty(required=True, indexed=True)
    liker = db.StringProperty(required=True, indexed=True)
    likeTime = db.DateTimeProperty(auto_now_add=True)

def like_comment(comment_entity, liker):
    """Adds a CommentLike entity"""
    new_like_entity = CommentLike(comment=comment_entity, liker=liker)
    new_like_entity.put()

def unlike_comment(comment_entity, unliker):
    """Deletes a CommentLike entity"""
    likes_query = CommentLike.all()
    likes_query.filter('liker =', unliker)
    like_entity = likes_query.get()
    like_entity.delete()

def comment_is_liked(comment_entity, liker):
    """Returns true if a given user (liker) has liked a given comment"""
    likes_query = CommentLike.all()
    likes_query.filter('liker =', liker)
    likes_query.filter('comment =', comment_entity)
    return likes_query.count() > 0

def comment_like_count(comment_entity):
    """Returns the number of likes for a comment"""
    likes_query = CommentLike.all()
    likes_query.filter('Comment =', comment_entity)
    return likes_query.count()

def delete_comment_likes(comment_entity):
    """Deletes all the likes for a comment"""
    likes_query = CommentLike.all()
    likes_query.filter('Comment =', comment_entity)
    for like in likes_query:
        like.delete()
