# -*- encoding: UTF-8 -*-
#
# Form based authentication for CherryPy. Requires the
# Session tool to be loaded.
#

import cherrypy

def check_credentials(username, password):
    """
        Verifies credentials for username and password.
        Returns None on success or a string describing the error on failure
    """
    # Adapt to your needs
    if username in ('joe', 'steve') and password == 'secret':
        return None
    else:
        return u'Incorrect username or password.'

    # An example implementation which uses an ORM could be:
    # u = User.get(username)
    # if u is None:
    #     return u"Username %s is unknown to me." % username
    # if u.password != md5.new(password).hexdigest():
    #     return u"Incorrect password"

def check_auth(*args, **kwargs):
    """
        A tool that looks in config for 'auth.require'. If found and it
        is not None, a login is required and the entry is evaluated as a
        list of conditions that the user must fulfill
    """
    require = cherrypy.request.config.get('auth.require', False)

    if require:
        session_key = cherrypy.request.config.get('session.key', '~ae!creds~')

        username = cherrypy.session.get(session_key)
        if username:
            cherrypy.request.login = username

        else:
            raise cherrypy.HTTPRedirect('/login/')


def require():
    """
        A decorator that appends conditions to the auth.require config
        variable.
    """
    def decorate(f):
        if not hasattr(f, '_cp_config'):
            f._cp_config = dict()

        if 'auth.require' not in f._cp_config:
            f._cp_config['auth.require'] = True

        return f

    return decorate


class AuthController(object):

    def on_login(self, username):
        """Called on successful login"""

    def on_logout(self, username):
        """Called on logout"""

    def get_loginform(self, username, msg="Enter login information", from_page="/"):
        return """<html>
            <body>
            <form method="post" action="/auth/login">
            <input type="hidden" name="from_page" value="%(from_page)s" />
            %(msg)s<br />
            Username: <input type="text" name="username" value="%(username)s" /><br />
            Password: <input type="password" name="password" /><br />
            <input type="submit" value="Log in" />
        </body>
        </html>""" % locals()

    @cherrypy.expose
    def login(self, username=None, password=None, from_page="/"):
        if username is None or password is None:
            return self.get_loginform("", from_page=from_page)

        error_msg = check_credentials(username, password)
        if error_msg:
            return self.get_loginform(username, error_msg, from_page)
        else:
            session_key = cherrypy.request.config.get('session.key', '~ae!creds~')
            cherrypy.session[session_key] = cherrypy.request.login = username
            self.on_login(username)
            raise cherrypy.HTTPRedirect(from_page or "/")

    @cherrypy.expose
    def logout(self, from_page="/"):
        sess = cherrypy.session
        session_key = cherrypy.request.config.get('session.key', '~ae!creds~')

        username = sess.get(session_key, None)
        sess[session_key] = None
        if username:
            cherrypy.request.login = None
            self.on_logout(username)

        raise cherrypy.HTTPRedirect(from_page or "/")


