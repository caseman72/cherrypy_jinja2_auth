# -*- encoding: UTF-8 -*-

import cherrypy
import tools.ninja_templates

class WebServer:

    @cherrypy.expose
    @cherrypy.tools.ninja(tpl='index')
    def index(self):
        return {
            'title': 'Welcome',
            'desc' : 'Welcome to the newest web-server',
            'author': 'Casey Manion'
        }


if __name__ == '__main__':
    cherrypy.quickstart(WebServer())
