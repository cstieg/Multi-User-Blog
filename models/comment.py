from google.appengine.ext import db
import models

class Comment(db.Model):
    """Comments subordinate to the main entries of the blog"""
    blogEntry = db.ReferenceProperty(models.BlogEntry, collection_name='comments')
    # blogEntryID = db.IntegerProperty(required=True, indexed=True)
    comment = db.TextProperty(required=True)
    author = db.StringProperty(required=True, indexed=True)
    posted = db.DateTimeProperty(auto_now_add=True, indexed=True)

    @property
    def id(self):
        return self.key().id()

    @property
    def likeCount(self):
        return models.comment_like_count(self)

    def liked(self, user_name):
        return models.comment_is_liked(self, user_name)


def add_comment(entry_entity, comment_text, commenter):
    """Adds a comment of comment_text by user commenter to a entry_entity
    and increments the comment count on the entry"""
    new_comment_entity = Comment(blogEntry=entry_entity, author=commenter, comment=comment_text)
    new_comment_entity.put()
    return new_comment_entity

def edit_comment(comment_entity, new_comment_text):
    """Edits a comment on a blog entry"""
    comment_entity.comment = new_comment_text
    comment_entity.put()

def delete_comments(entry_entity):
    """Deletes all comments for a blog entry"""
    comments_query = Comment.all()
    comments_query.filter('blogEntry =', entry_entity)
    for comment in comments_query:
        models.delete_comment_likes(comment)
        comment.delete()

def comment_count(entry_entity):
    """Count all comments for a blog entry"""
    comments_query = Comment.all()
    comments_query.filter('blogEntry = ', entry_entity)
    return comments_query.count()
