import models, handlers

class Login(handlers.Handler):
    """Allows registered user to login"""
    def get(self):
        """Renders login page"""
        caller = handlers.sanitize(self.request.get('caller'))
        self.render('login.html', caller=caller)

    def post(self):
        """Accepts login info from login page and sets cookies"""
        caller = handlers.sanitize(self.request.get('caller'))
        username = handlers.sanitize(self.request.get('username'))
        password = handlers.sanitize(self.request.get('password'))

        # check username and password
        if models.is_valid_user(username, password):
            # success, redirect to calling page
            handlers.logout_user(self)
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
    return models.is_valid_user(handlers.sanitize(username), handlers.sanitize(password))


def get_username(handler):
    """Returns the username stored in cookies"""
    if valid_user_login(handler):
        return handlers.sanitize(handler.request.cookies.get('username'))
    return ''

