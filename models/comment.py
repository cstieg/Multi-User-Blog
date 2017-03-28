from google.appengine.ext import db

class Comment(db.Model):
    """Comments subordinate to the main entries of the blog"""
    blogEntryID = db.IntegerProperty(required=True, indexed=True)
    comment = db.TextProperty(required=True)
    author = db.StringProperty(required=True, indexed=True)
    posted = db.DateTimeProperty(auto_now_add=True, indexed=True)
    likeCount = db.IntegerProperty(default=0, indexed=True)


@db.transactional(xg=True)
def add_comment(entry_entity, comment_text, commenter):
    """Adds a comment of comment_text by user commenter to a entry_entity
    and increments the comment count on the entry"""
    new_comment_entity = Comment(parent=entry_entity, blogEntryID=entry_entity.key().id(), author=commenter, comment=comment_text)
    new_comment_entity.put()

    entry_entity.commentCount += 1
    entry_entity.put()

    return new_comment_entity


@db.transactional(xg=True)
def delete_comment(comment_entity, parent_entity):
    """Deletes a comment on a blog entry and decrements the comment count on the entry"""
    parent_entity.commentCount -= 1
    parent_entity.put()

    comment_entity.delete()


def edit_comment(comment_entity, new_comment_text):
    """Edits a comment on a blog entry"""
    comment_entity.comment = new_comment_text
    comment_entity.put()
