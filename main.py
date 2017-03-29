#!/usr/bin/env python
"""Blog app that allows a user to signup, login, post blog entries,
manage one's own entries, view and comment on the entries, and like other
author's entries and comments"""

import webapp2
from handlers import (MainPage, Compose, DeletePost, EditPost, AddComment,
                      DeleteComment, EditComment, Signup, Login, Logout, LikePost,
                      UnlikePost, LikeComment, UnlikeComment)

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/([0-9]+)', MainPage),
                               ('/newpost', Compose),
                               ('/signup', Signup),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/deletepost/([0-9]+)', DeletePost),
                               ('/editpost/([0-9]+)', EditPost),
                               ('/likepost/([0-9]+)', LikePost),
                               ('/unlikepost/([0-9]+)', UnlikePost),
                               ('/addcomment/([0-9]+)', AddComment),
                               ('/deletecomment/([0-9]+)', DeleteComment),
                               ('/editcomment/([0-9]+)', EditComment),
                               ('/likecomment/([0-9]+)', LikeComment),
                               ('/unlikecomment/([0-9]+)', UnlikeComment)
                               ], debug=True)
