"""Have a website quickly with django.

This package is to help beginners have a website which can be published of themselves.
The package mainly uses module django. Use command "pip install django" to install it.

All method in one class. Create an example, and call it.
Server.__init__ needs 3 args, they're example "self", the server path and the name of project.
As creating it, it creates a django project for server. And the methods take command args' place.
Common actions of manage.py (django) in class as methods.

e.g.
import beginner_web
server = beginner_web.Server(r'Your_Path', 'Website_Project')
server.add_app(app='user')
server.add_app(app='wrong_app')
server.remove_app(app='wrong_app)
server.include_templates(dirname='Template_Path')
server.add_template(from_='HTML_Path', pack='Template_Save_As_Dir')
server.run(host='localhost', port=8000)
"""

import os
import shutil


def _call(command: str,
          # shell: bool=True,
          ) -> bool:
    """Call CMD command with os.system or os.popen. However, in this version, shell must be True."""
    # if shell:
    #     return bool(os.system(command))
    # else:
    #     return os.popen(command).read()
    return bool(os.system(command))


def module(module_name) -> __import__:
    return __import__(module_name)


class BaseServer:
    """The class of a website server.
    Create its example to have your website."""

    root: str = None
    shell: bool = None
    name: str = None
    url: list = []

    @staticmethod  # Be static method only in this version.
    def call(command):
        """Call "call" function outside."""
        # return _call(command, shell=self.shell)
        return _call(command=command)

    def __init__(self, path: str, name: str):
        """Set the args of server."""

        __file__ = '{}\\{}'.format(path, name)

    @property
    def urls(self):
        return UrlSet(module('{}.urls'.format(self.name)).urlpatterns)

    def exception(self, code, func):
        """View functions called while exceptions happen."""
        exec("module('%.urls' % self.name).handler{} = views.{}".format(code, func))

    def add_view(self, url, func):
        """Add a view function to the root URLs."""
        self.urls.append(url=url, func='view.' + str(func.__name__) + ',')

    def include_views(self, url, app):
        """Include URLs from an application."""
        if type(app) is not str:
            raise TypeError('Arg "app" must be str, not {}.'.format(type(app).__name__))

        apps = module('{}.settings'.format(self.name)).INSTALLED_APPS
        if app not in apps:
            raise ApplicationError('No such application: {}'.format(app))
        del apps

        self.urls.append(url=url, func='include(' + app + '),')

    def manage(self, command: str):
        """Run administrative tasks."""
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{}.settings'.format(self.name))
        try:
            from django.core.management import execute_from_command_line
        except ImportError as exc:
            # raise ImportError(
            #     "Couldn't import Django. Are you sure it's installed and "
            #     "available on your PYTHONPATH environment variable? Did you "
            #     "forget to activate a virtual environment?"
            # ) from exc
            #
            # Django code (manage.py) above.
            raise ModuleNotFoundError('Cannot find the necessary module: django')
        execute_from_command_line(['manage.py'] + command.split(' '))

    def run(self, host: str = '127.0.0.1', port: int = 8000):
        """Run the server."""
        per = 'runserver {}:{}'.format(host, port)
        self.manage(command=per)

    def add_app(self, app: str):
        """Add a web application for project."""
        try:
            self.manage(command='startapp {}'.format(app))
        except Exception:
            raise ApplicationError('An unknown exception happened while creating an application.')

    def remove_app(self, app: str):
        """Remove a web application in the project."""
        apps = module('{}.settings'.format(self.name)).INSTALLED_APPS
        for i, a in enumerate(apps):
            if a == app:
                del apps[i]
                try:
                    shutil.rmtree(app)
                except FileNotFoundError:
                    pass
                return
        raise ApplicationError('No such application: {}'.format(app))

    def include_templates(self, dirname: str):
        """Mark a directory as a template dir."""
        if not os.path.exists(path=dirname):
            raise TemplateError('No such directory: {}'.format(dirname))

        module('{}.settings'.format(self.name)).TEMPLATES[1]['DIRS'].append(
            os.path.join(module('{}.settings'.format(self.name)).BASE_DIR), dirname)

    def add_template_dir(self, dirname: str):
        """Add a directory and mark it as a template dir."""
        os.mkdir(dirname)
        self.include_templates(dirname)

    def add_template(self, from_: str, pack: str, **kwargs):
        new_name = kwargs.get('new_name', from_)
        try:
            f = open(from_, 'rb')
        except FileNotFoundError:
            raise TemplateError('No such template: {}'.format(from_))

        try:
            fw = open('{}\\{}'.format(pack, new_name), 'wb')
        except FileNotFoundError:
            raise TemplateError('No such template directory: {}'.format(pack))

        fw.write(f.read())

        f.close()
        fw.close()

        return pack in module('{}.settings'.format(self.name)).TEMPLATES[1]['DIRS']


class UrlSet:
    """For variables "urlpatterns" in files "urls"."""

    urls: list = []
    string: str = None

    def __init__(self, urls: list):
        self.urls = urls
        self.update()

    def update(self):
        self.string = """[
    {}
]""".format('\n'.join(self.urls))

    def append(self, url, func):
        self.urls.append('url(r"{}", {}'.format(url, func))
        self.update()

    def __str__(self):
        return self.string


class Server(BaseServer):
    def __init__(self, path, name):
        # Higher Version: def __init__(self, path: str, name: str, shell=True):
        """Set the args of server."""

        super(Server, self).__init__(path, name)

        # Check if path is valid.
        if not os.path.exists(path=path):
            raise DirectoryNotFoundError(path=path)
        self.root = path
        self.name = name
        self.shell = True

        _creating = self.call(command='django-admin startproject {}'.format(name))
        if not _creating:
            raise ServerCreatingFailedError()

        with open('{}\\views.py'.format(name), 'w') as f:
            f.write('from django.shoutcut import render')
        module('{}.urls'.format(self.name)).views = module('{}.views'.format(self.name))


class DirectoryNotFoundError(Exception):
    """No such directory with the path."""

    def __init__(self, path):
        """:arg path: Path of the directory not found."""
        self.exc = path

    def __str__(self) -> str:
        return "No such directory: {}".format(self.exc)


class ServerCreatingFailedError(Exception):
    """Exceptions happen while creating server."""

    def __str__(self) -> str:
        return "Creating server failed."


class ApplicationError(Exception):
    """Exceptions in apps."""

    def __init__(self, text):
        self.exc = text

    def __str__(self) -> str:
        return self.exc


class TemplateError(Exception):
    """Exceptions in templates."""

    def __init__(self, text):
        self.exc = text

    def __str__(self) -> str:
        return self.exc
