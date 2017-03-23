"""Handlers for adding, editing, and deleting comments"""
import json
from google.appengine.ext import db

from handler import Handler
from model import validUserLogin, getUsername, addComment
from utils import to_dict

class AddComment(Handler):
    """Add a comment to a particular post"""
    def post(self, post=""):
        if not validUserLogin(self):
            self.redirect("/login")
        if post:
            # query post by id passed in
            entryKey = db.Key.from_path('BlogEntry', int(post))

            if not entryKey:
                self.error(400)
                return
            blogEntry = db.get(entryKey)
        else:
            self.error(400)

        commentText = self.request.get('comment')
        userID = getUsername(self)
        if commentText and userID:
            newCommentEntity = addComment(blogEntry, commentText, userID)
            newComment = to_dict(newCommentEntity)
            newComment['id'] = newCommentEntity.key().id()
            self.response.out.write(json.dumps(newComment))
        else:
            self.error(400)
        
class EditComment(Handler):
    """Edit a comment made by the author on a particular post"""
    def post(self, post=""):
        if not validUserLogin(self):
            self.redirect("/login")
        if post:
            # query post by id passed in
            entryKey = db.Key.from_path('BlogEntry', int(post))

            if not entryKey:
                self.error(400)
                return
            blogEntry = db.get(entryKey)
        else:
            self.error(400)

            #TODO
            
class DeleteComment(Handler):
    """Delete a comment made by the author on a particular post"""
    def post(self, post=""):
        if not validUserLogin(self):
            self.redirect("/login")
        if post:
            # query post by id passed in
            entryKey = db.Key.from_path('BlogEntry', int(post))
            
            if not entryKey:
                self.error(400)
                return
            blogEntry = db.get(entryKey)
        else:
            self.error(400)            
            
            #TODO
