from google.appengine.ext import db

class PostLike(db.Model):
    """Reader likes on the main entries of the blog"""
    blogEntryID = db.IntegerProperty(required=True, indexed=True)
    liker = db.StringProperty(required=True, indexed=True)
    likeTime = db.DateTimeProperty(auto_now_add=True)


@db.transactional(xg=True)
def like_post(entry_entity, liker):
    """Adds a PostLike entity and increments the like count for the BlogEntry entity"""
    new_like_entity = PostLike(parent=entry_entity, blogEntryID=entry_entity.key().id(), liker=liker)
    new_like_entity.put()

    entry_entity.likeCount += 1
    entry_entity.put()


@db.transactional(xg=True)
def unlike_post(entry_entity, unliker):
    """Deletes a PostLike entity and decrements the like_entity count for the BlogEntry entity"""
    likes_query = PostLike.all()
    likes_query.ancestor(entry_entity)
    likes_query.filter('liker =', unliker)
    like_entity = likes_query.get()
    like_entity.delete()

    entry_entity.likeCount -= 1
    entry_entity.put()


def post_is_liked(entry_entity, liker):
    """Returns true if a given user (liker) has liked a given entry_entity"""
    entry_id = str(entry_entity.key().id())
    likes_query = db.GqlQuery("SELECT* FROM PostLike WHERE entry_id = %s AND liker = '%s'" % (entry_id, liker))
    return likes_query.count() > 0
