
import webapp2
import jinja2
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader(template_dir))


class Handler(webapp2.RequestHandler):
    """Abstraction for webapp2 request handler"""
    def write(self, *a, **kw):
        """Convenience wrapper for writing a response to HTTP request"""
        self.response.out.write(*a, **kw)

    def render_str(self, template, **kw):
        """Gets a template from the jinja environment and renders it"""
        t = jinja_env.get_template(template)
        return t.render(kw)

    def render(self, template, **kw):
        """Convenience method to be used to render a template with data"""
        self.write(self.render_str(template, **kw))
