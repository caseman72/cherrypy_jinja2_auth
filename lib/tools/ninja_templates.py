# -*- encoding: UTF-8 -*-

"""
A Jinja2 Handler and tool.  This code is in the public domain.

Usage:
@cherrypy.expose
@cherrypy.tools.ninja(tpl='index')
def controller(**kwargs):
    return {
        'foo': 'bar'
    } # This dict is the template context
"""

import cherrypy
import jinja2
import os
from datetime import date

# ninja_templates (nt)'s globals
nt_dir = os.path.join(os.getcwd(), os.path.dirname(__file__))
nt_root = os.path.dirname(os.path.dirname(nt_dir)) # ../..
nt_loader = jinja2.FileSystemLoader(os.path.join(nt_root, 'templates'))
nt_env = jinja2.Environment(loader=nt_loader)


class Jinja2Handler(cherrypy.dispatch.LateParamPageHandler):
    """Callable which sets response.body."""

    def __init__(self, template_name, next_handler):
        self.template_name = template_name
        self.next_handler = next_handler

    def __call__(self ):
        context = {}

        # mako doesn't try/catch this ...
        try:
            context.update(self.next_handler())
        except ValueError, e:
            pass

        # cannot re-map these in my mind-map
        headers = {'YEAR' : date.today().year}
        for k, v in cherrypy.request.header_list:
            headers[k.upper().replace('-', '_')] = v

        context.update({
            'headers': headers,
            'request': cherrypy.request.request_line,
        })

        template = nt_env.get_template(self.template_name + '.mustache')
        return template.render(**context)

#       cherrypy.request.template = template

class Jinja2Loader(object):
    """A CherryPy 3 Tool for loading Jinja2 templates."""

    def __init__(self):
        pass

    def __call__(self, tpl):
        cherrypy.request.handler = Jinja2Handler(tpl, cherrypy.request.handler)

cherrypy.tools.ninja = cherrypy.Tool('on_start_resource', Jinja2Loader(), priority=70)
