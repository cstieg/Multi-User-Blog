from handlers import Handler, sanitize, logout_user
from models import is_valid_user

class Login(Handler):
    """Allows registered user to login"""
    def get(self):
        """Renders login page"""
        caller = sanitize(self.request.get('caller'))
        self.render('login.html', caller=caller)

    def post(self):
        """Accepts login info from login page and sets cookies"""
        caller = sanitize(self.request.get('caller'))
        username = sanitize(self.request.get('username'))
        password = sanitize(self.request.get('password'))

        # check username and password
        if is_valid_user(username, password):
            # success, redirect to calling page
            logout_user(self)
            self.response.set_cookie('username', username, max_age=60 * 60 * 24)
            self.response.set_cookie('password', password)
            self.redirect('/' + caller)

        else:
            # Re-render login page if invalid login
            self.render('login.html', login_error=True, caller=caller)


def valid_user_login(handler):
    """Returns true if a valid user is logged in, false otherwise"""
    username = handler.request.cookies.get('username')
    password = handler.request.cookies.get('password')
    if not username or not password:
        return False
    return is_valid_user(sanitize(username), sanitize(password))


def get_username(handler):
    """Returns the username stored in cookies"""
    if valid_user_login(handler):
        return sanitize(handler.request.cookies.get('username'))
    return ""

