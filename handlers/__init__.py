"""URL handlers"""
from handlers.handler import (Handler, to_dict, sanitize, check_logged_in,
                              check_entry_exists, check_comment_exists,
                              check_user_owns_comment, check_user_owns_entry)
from handlers.logout import Logout, logout_user
from handlers.login import Login, valid_user_login, get_username
from handlers.signup import Signup
from handlers.mainpage import MainPage
from handlers.compose import Compose
from handlers.deletepost import DeletePost
from handlers.editpost import EditPost
from handlers.addcomment import AddComment
from handlers.deletecomment import DeleteComment
from handlers.editcomment import EditComment
from handlers.likepost import LikePost, UnlikePost
from handlers.likecomment import LikeComment, UnlikeComment
