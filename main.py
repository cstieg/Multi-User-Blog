"""Blog app that allows a user to signup, login, post blog entries,
manage one's own entries, view and comment on the entries, and like other
author's entries and comments"""

import webapp2

from entryView import MainPage, Compose, DeletePost, EditPost
from commentView import AddComment, DeleteComment, EditComment
from loginView import Signup, Login, Logout
from likeView import LikePost, UnlikePost

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
                               ('/deletecomment/([0-9]+)/([0-9]+)', DeleteComment),
                               ('/editcomment/([0-9]+)/([0-9]+)', EditComment)
                               ], debug=True)

