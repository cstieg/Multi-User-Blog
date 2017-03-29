import handlers

class Logout(handlers.Handler):
    """Logs out user"""
    def get(self):
        logout_user(self)
        self.redirect('/')


def logout_user(handler):
    """Logs the current user out by deleting login cookies"""
    handler.response.delete_cookie('username')
    handler.response.delete_cookie('password')
