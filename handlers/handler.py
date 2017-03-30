import datetime
import os
import cgi
from functools import wraps
import webapp2
import jinja2
from google.appengine.ext import db
import handlers

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), *[os.pardir, 'templates'])
JINJA_ENV = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader(TEMPLATE_DIR))


class Handler(webapp2.RequestHandler):
    """Abstraction for webapp2 request handler"""
    def write(self, *a, **kw):
        """Convenience wrapper for writing a response to HTTP request"""
        self.response.out.write(*a, **kw)

    def render_str(self, template, **kw):
        """Gets a template from the jinja environment and renders it"""
        template = JINJA_ENV.get_template(template)
        return template.render(kw)

    def render(self, template, **kw):
        """Convenience method to be used to render a template with data"""
        self.write(self.render_str(template, **kw))


def sanitize(text_to_sanitize):
    """Returns string sanitized of html and script"""
    if text_to_sanitize:
        return cgi.escape(text_to_sanitize)
    else:
        return text_to_sanitize


def check_logged_in(url_args=''):
    """
    Decorator to check if a user is logged in.  If user is not logged in, calls
    the login page.  Must be called with (), and may pass the optional argument 
    of the calling page to return to after logging in.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(handler, *args, **kwargs):
            if not handlers.valid_user_login(handler):
                handler.redirect('/login' + url_args)
            func(handler, *args, **kwargs)
        return wrapper
    return decorator


def check_entry_exists(entry_id_required=True):
    """
    Decorator to check if a given entry exists.  If it does not, it returns an
    HTTP 400 error.  Must be called with (), and may pass the optional argument
    of whether the id is required.  If the id is passed, it will be checked
    against entities of the BlogEntry kind, and a 400 error will be returned if
    it is not found.  If the id is not passed, an error will be returned, unless
    the argument is False.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, entry_id=''):
            entry_entity = None
            if entry_id:
                entry_key = db.Key.from_path('BlogEntry', int(entry_id))
                entry_entity = db.get(entry_key)
                if not entry_entity:
                    # bad request
                    return self.error(400)
            elif entry_id_required:
                return self.error(400)
            func(self, entry_entity)
        return wrapper
    return decorator


def check_comment_exists(comment_id_required=True):
    """
    Decorator to check if a given comment exists.  If it does not, it returns an
    HTTP 400 error.  Must be called with (), and may pass the optional argument
    of whether the id is required.  If the id is passed, it will be checked
    against entities of the Comment kind, and a 400 error will be returned if
    it is not found.  If the id is not passed, an error will be returned, unless
    the argument is False.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, comment_id=''):
            comment_entity = None
            if comment_id:
                comment_key = db.Key.from_path('Comment', int(comment_id))
                comment_entity = db.get(comment_key)
                if not comment_entity:
                    # bad request
                    return self.error(400)
            elif comment_id_required:
                return self.error(400)
            func(self, comment_entity)
        return wrapper
    return decorator


def check_user_owns_entry(must_own=True):
    """
    Decorator to check if the user owns a given entry.  Must be called with (),
    and may pass the optional argument of whether the user must own it.
    If the user must own it (default) but does not, it returns a 401 error.
    If the user must not own it (must_own=False), but does, it likewise returns
    a 401 error (used in case where user cannot like his own entry).
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, entry_entity):
            user_id = handlers.get_username(self)
            if (entry_entity.author == user_id and must_own) or \
               (entry_entity.author != user_id and not must_own):
                func(self, entry_entity)
            else:
                # unauthorized
                return self.error(401)
        return wrapper
    return decorator

def check_user_owns_comment(must_own=True):
    """
    Decorator to check if the user owns a given comment.  Must be called with (),
    and may pass the optional argument of whether the user must own it.
    If the user must own it (default) but does not, it returns a 401 error.
    If the user must not own it (must_own=False), but does, it likewise returns
    a 401 error (used in case where user cannot like his own comment).
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, comment_entity):
            user_id = handlers.get_username(self)
            if (comment_entity.author == user_id and must_own) or \
               (comment_entity.author != user_id and not must_own):
                func(self, comment_entity)
            else:
                # unauthorized
                return self.error(401)
        return wrapper
    return decorator


"""
written by dmw, modified slightly
(http://stackoverflow.com/questions/1531501/json-serialization-of-google-app-engine-models)
converts datastore model to dict
"""

SIMPLE_TYPES = (int, long, float, bool, dict, basestring, list)

def to_dict(model):
    output = {}

    for key, prop in model.properties().iteritems():
        value = getattr(model, key)

        if value is None or isinstance(value, SIMPLE_TYPES):
            output[key] = value
        elif isinstance(value, datetime.date):
            output[key] = value.strftime('%c')
        elif isinstance(value, db.GeoPt):
            output[key] = {'lat': value.lat, 'lon': value.lon}
        elif isinstance(value, db.Model):
            output[key] = to_dict(value)
        else:
            raise ValueError('cannot encode ' + repr(prop))

    return output