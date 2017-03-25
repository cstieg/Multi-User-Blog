"""Handlers for adding, editing, and deleting comments"""
import json
import logging
from google.appengine.ext import db

from handler import Handler
from model import (BlogEntry, Comment, validUserLogin, getUsername, addComment, 
                   editComment, deleteComment)
from utils import to_dict

class AddComment(Handler):
    """Add a comment to a particular post"""
    def post(self, postID=""):
        if not validUserLogin(self):
            self.redirect("/login")
        if postID:
            # query post by id passed in
            entryKey = db.Key.from_path('BlogEntry', int(postID))

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
    def post(self, commentID="", parentID=""):
        if not validUserLogin(self):
            self.redirect("/login")
        commentText = self.request.get('comment')
        if commentID and parentID and commentText:
            # query post by id passed in
            parentKey = BlogEntry.get_by_id(int(parentID)).key()
            parentEntity = db.get(parentKey)
            commentEntity = Comment.get_by_id(int(commentID), parent=parentKey)
            if not commentEntity or not parentEntity:
                self.error(400)
                return

            # only author can edit
            userID = getUsername(self)
            if commentEntity.author == userID:
                 editComment(commentEntity, commentText)
            else:
                self.error(401)
        else:
            self.error(400)            
            
            
class DeleteComment(Handler):
    """Delete a comment made by the author on a particular post"""
    def post(self, commentID="", parentID=""):
        if not validUserLogin(self):
            self.redirect("/login")
        if commentID and parentID:
            # query post by id passed in
            parentKey = BlogEntry.get_by_id(int(parentID)).key()
            parentEntity = db.get(parentKey)
            commentEntity = Comment.get_by_id(int(commentID), parent=parentKey)
            if not commentEntity or not parentEntity:
                self.error(400)
                return

            # only author can delete
            userID = getUsername(self)
            if commentEntity.author == userID:
                deleteComment(commentEntity, parentEntity)
            else:
                self.error(401)
        else:
            self.error(400)            
            
