from google.appengine.ext import db

class CommentLike(db.Model):
    """Reader likes on the subordinate comments"""
    commentID = db.IntegerProperty(required=True, indexed=True)
    liker = db.StringProperty(required=True, indexed=True)
    likeTime = db.DateTimeProperty(auto_now_add=True)

def comment_is_liked(comment_entity, liker):
    """Returns true if a given user (liker) has liked a given comment"""
    likes_query = CommentLike.all()
    likes_query.ancestor(comment_entity)
    likes_query.filter('liker =', liker)
    return (likes_query.count() > 0)


@db.transactional(xg=True)
def like_comment(comment_entity, liker):
    """Adds a CommentLike entity and increments the like count for the Comment entity"""
    new_like_entity = CommentLike(parent=comment_entity, commentID=comment_entity.key().id(), liker=liker)
    new_like_entity.put()

    comment_entity.likeCount += 1
    comment_entity.put()


@db.transactional(xg=True)
def unlike_comment(comment_entity, unliker):
    """Deletes a CommentLike entity and decrements the like_entity count for the Comment entity"""
    likes_query = CommentLike.all()
    likes_query.ancestor(comment_entity)
    likes_query.filter('liker =', unliker)
    like_entity = likes_query.get()
    like_entity.delete()

    comment_entity.likeCount -= 1
    comment_entity.put()
