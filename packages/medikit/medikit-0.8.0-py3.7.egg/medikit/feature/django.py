"""
The «django» feature adds the django framework to your project.

"""

import os
import random

import medikit
from medikit.events import subscribe

from . import SUPPORT_PRIORITY, Feature

random = random.SystemRandom()


def generate_secret_key():
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*(-_=+)"
    return "".join(random.choice(chars) for i in range(64))


class DjangoConfig(Feature.Config):
    """ Configuration class for the “django” feature. """

    version = "~=2.0,<2.2"
    """Which django version requirement do you want?"""

    __usage__ = """
    
    This will add a few items to your Makefile, and ensure a minimalistic django project structure is available.
    
    By default, it will use Django {version}, but you can tune that:
    
    .. code-block:: python
    
        django.version = '~=2.0.3'
        
    This feature will also add or extend a "prod" python extra, that will install gunicorn.
    
    """.format(
        version=version
    )

    def __init__(self):
        self._static_dir = None
        self.version = self.version

    @property
    def static_dir(self):
        """
        The django global static directory (property).
        """
        return self._static_dir

    @static_dir.setter
    def static_dir(self, value):
        self._static_dir = value


class DjangoFeature(Feature):
    requires = {"python"}

    Config = DjangoConfig

    @subscribe("medikit.feature.python.on_generate")
    def on_python_generate(self, event):
        event.config["python"].add_requirements("django " + event.config["django"].version, prod=["gunicorn ==19.7.1"])

    @subscribe("medikit.feature.make.on_generate", priority=SUPPORT_PRIORITY)
    def on_make_generate(self, event):
        makefile = event.makefile
        makefile["DJANGO"] = "$(PYTHON) manage.py"
        makefile.add_target("runserver", """$(DJANGO) runserver""", deps=("install-dev",), phony=True)

    @subscribe(medikit.on_start)
    def on_start(self, event):
        django_config = event.config["django"]
        python_config = event.config["python"]

        context = {**python_config.get_setup(), "config_package": "config", "secret_key": generate_secret_key()}

        # Create configuration
        config_path = "config"
        if not os.path.exists(config_path):
            os.makedirs(config_path)

        self.render_file("manage.py", "django/manage.py.j2", context, executable=True, force_python=True)
        self.render_file(os.path.join(config_path, "settings.py"), "django/settings.py.j2", context, force_python=True)
        self.render_file(os.path.join(config_path, "urls.py"), "django/urls.py.j2", context, force_python=True)
        self.render_file(os.path.join(config_path, "wsgi.py"), "django/wsgi.py.j2", context, force_python=True)

        self.dispatcher.dispatch("medikit.feature.django.on_configure")

        static_dir = django_config.static_dir or os.path.join(python_config.package_dir, "static")
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)
        self.render_empty_files(os.path.join(static_dir, "favicon.ico"))
