import os
import cgi
import datetime
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


SIMPLE_TYPES = (int, long, float, bool, dict, basestring, list)

def to_dict(model):
    """Converts a datastore entity into a Python dict
    originally written by 'dmw'
    (http://stackoverflow.com/questions/1531501/json-serialization-of-google-app-engine-models)
    slight modifications made"""
    output = {}

    for key, prop in model.properties().iteritems():
        value = getattr(model, key)

        if value is None or isinstance(value, SIMPLE_TYPES):
            output[key] = value
        elif isinstance(value, datetime.date):
            # Convert date/datetime to MILLISECONDS-since-epoch (JS "new Date()").
            # ms = time.mktime(value.utctimetuple()) * 1000
            # ms += getattr(value, 'microseconds', 0) / 1000
            # output[key] = int(ms)
            output[key] = value.strftime('%c')
        elif isinstance(value, db.GeoPt):
            output[key] = {'lat': value.lat, 'lon': value.lon}
        elif isinstance(value, db.Model):
            output[key] = to_dict(value)
        else:
            raise ValueError('cannot encode ' + repr(prop))

    return output


def sanitize(text_to_sanitize):
    """Returns string sanitized of html and script"""
    if text_to_sanitize:
        return cgi.escape(text_to_sanitize)
    else:
        return text_to_sanitize


def check_logged_in(url_args):
    def decorator(func):
        def wrapper(self, entry_id=''):
            if not handlers.valid_user_login(self):
                return self.redirect('/login' + url_args)
            return func(self, entry_id)
        return wrapper
    return decorator
