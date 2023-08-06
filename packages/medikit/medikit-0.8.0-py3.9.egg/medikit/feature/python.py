"""
The “python” feature is the base feature required for all python projects.

Medikit only supports python 3.5+ projects, which we believe is a future proof choice.

Overview
::::::::

.. code-block:: python

    from medikit import require

    # load python feature (idempotent).
    python = require('python')

    # configure our package.
    python.setup(
        name = 'awesome-library',
        author = 'Chuck Norris',
    )

    # add base and extras requirements, with "loose" versionning (the frozen version fits better in requirements*.txt)
    python.add_requirements(
        'django',
        dev=[
            'pytest',
        ],
    )

"""

import itertools
import os
import tempfile
from getpass import getuser

from pip._vendor.distlib.util import parse_requirement
from piptools._compat import parse_requirements
from piptools.cache import DependencyCache
from piptools.locations import CACHE_DIR
from piptools.repositories import PyPIRepository
from piptools.resolver import Resolver
from piptools.utils import format_requirement

import medikit
from medikit.events import subscribe
from medikit.feature import ABSOLUTE_PRIORITY, Feature
from medikit.feature.make import InstallScript, which
from medikit.globals import PIP_VERSION
from medikit.resources.configparser import ConfigParserResource
from medikit.utils import get_override_warning_banner


def _normalize_requirement(req):
    bits = req.requirement.split()
    if req.extras:
        bits = [bits[0] + "[{}]".format(",".join(req.extras))] + bits[1:]
    return " ".join(bits)


class PythonConfig(Feature.Config):
    """ Configuration API for the «python» feature. """

    on_generate = __name__ + ".on_generate"

    def __init__(self):
        self._setup = {}
        self._requirements = {None: {}, "dev": {}}
        self._constraints = {}
        self._inline_requirements = {}
        self._vendors = {}
        self._version_file = None
        self._create_packages = True
        self.override_requirements = False
        self.use_wheelhouse = False

    @property
    def package_dir(self):
        return "/".join(self.get("name").split("."))

    @property
    def version_file(self):
        return self._version_file or os.path.join(self.package_dir, "_version.py")

    @version_file.setter
    def version_file(self, value):
        self._version_file = value

    @property
    def create_packages(self):
        return self._create_packages

    @create_packages.setter
    def create_packages(self, value):
        self._create_packages = bool(value)

    def get(self, item):
        if item == "install_requires":
            return list(self.get_requirements(with_constraints=True))
        if item == "extras_require":
            return {
                extra: list(self.get_requirements(extra=extra, with_constraints=True)) for extra in self.get_extras()
            }
        return self._setup.get(item)

    def get_init_files(self):
        # Explode package name so we know which python packages are namespaced and
        # which are not.
        package_bits = self.get("name").split(".")
        if len(package_bits) > 1:
            # XXX SIDE EFFECT !!!
            self["namespace_packages"] = []
            for i in range(1, len(package_bits)):
                self["namespace_packages"].append(".".join(package_bits[0:i]))

        for i in range(1, len(package_bits) + 1):
            _bits = package_bits[0:i]
            package_dir = os.path.join(*_bits)
            package_init_file = os.path.join(package_dir, "__init__.py")
            is_namespace = i < len(package_bits)
            yield package_dir, package_init_file, {"is_namespace": is_namespace}

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        self.setup(**{key: value})

    def __contains__(self, item):
        return bool(self.get(item))

    def add_constraints(self, *reqs, **kwargs):
        self.__add_constraints(reqs)
        for extra, reqs in kwargs.items():
            extra = extra.replace("_", "-")
            self.__add_constraints(reqs, extra=extra)
        return self

    def add_requirements(self, *reqs, **kwargs):
        self.__add_requirements(reqs)
        for extra, reqs in kwargs.items():
            extra = extra.replace("_", "-")
            self.__add_requirements(reqs, extra=extra)
        return self

    def add_inline_requirements(self, *reqs, **kwargs):
        self.__add_inline_requirements(reqs)
        for extra, reqs in kwargs.items():
            extra = extra.replace("_", "-")
            self.__add_inline_requirements(reqs, extra=extra)
        return self

    def add_vendors(self, *reqs, **kwargs):
        self.__add_vendors(reqs)
        for extra, reqs in kwargs.items():
            extra = extra.replace("_", "-")
            self.__add_vendors(reqs, extra=extra)
        return self

    def get_extras(self):
        return sorted(filter(None, self._requirements.keys()))

    def get_constraints(self, extra=None):
        for name, req in sorted(self._constraints.get(extra, {}).items()):
            yield _normalize_requirement(req)

    def get_requirements(self, extra=None, with_constraints=False):
        if with_constraints:
            yield from self.get_constraints(extra=extra)
        for name, req in sorted(self._requirements[extra].items()):
            yield _normalize_requirement(req)

    def get_inline_requirements(self, extra=None):
        return self._inline_requirements.get(extra, [])

    def get_vendors(self, extra=None):
        return self._vendors.get(extra, [])

    def setup(self, **kwargs):
        self._setup.update(kwargs)
        return self

    def get_setup(self):
        return self._setup

    def __add_constraints(self, reqs, extra=None):
        if len(reqs):
            if extra not in self._constraints:
                self._constraints[extra] = {}
        for req in reqs:
            req = parse_requirement(req)
            if req.name in self._constraints[extra]:
                raise ValueError("Duplicate constraint for {}.".format(req.name))
            self._constraints[extra][req.name] = req

    def __add_requirements(self, reqs, extra=None):
        if len(reqs):
            if extra not in self._requirements:
                self._requirements[extra] = {}
        for req in reqs:
            req = parse_requirement(req)
            if req.name in self._requirements[extra]:
                raise ValueError("Duplicate requirement for {}.".format(req.name))
            self._requirements[extra][req.name] = req

    def __add_inline_requirements(self, reqs, extra=None):
        if len(reqs):
            if extra not in self._inline_requirements:
                self._inline_requirements[extra] = []
        for req in reqs:
            self._inline_requirements[extra].append(req)

    def __add_vendors(self, reqs, extra=None):
        if len(reqs):
            if extra not in self._vendors:
                self._vendors[extra] = []
        for req in reqs:
            self._vendors[extra].append(req)


class PythonFeature(Feature):
    """
    Adds the requirements/requirements-dev logic, virtualenv support, setup.py generation, a few metadata files used by
    setuptools...

    """

    requires = {"make"}

    Config = PythonConfig

    @subscribe("medikit.feature.make.on_generate", priority=ABSOLUTE_PRIORITY)
    def on_make_generate(self, event):
        """
        **Environment variables**

        - ``PACKAGE``
        - ``PYTHON``
        - ``PYTHON_BASENAME``
        - ``PYTHON_DIR``
        - ``PYTHON_REQUIREMENTS_FILE``
        - ``PYTHON_REQUIREMENTS_DEV_FILE``

        **Shortcuts**
        - ``PIP``
        - ``PIP_INSTALL_OPTIONS``

        **Make targets**

        - ``install``
        - ``install-dev``

        :param MakefileEvent event:

        """

        python_config = event.config["python"]  # type: PythonConfig

        def _get_reqs_file_varname(extra=None):
            if extra:
                return "PYTHON_REQUIREMENTS_" + extra.upper().replace("-", "_") + "_FILE"
            return "PYTHON_REQUIREMENTS_FILE"

        def _get_reqs_inline_varname(extra=None):
            if extra:
                return "PYTHON_REQUIREMENTS_" + extra.upper().replace("-", "_") + "_INLINE"
            return "PYTHON_REQUIREMENTS_INLINE"

        extra_variables = []
        for extra in event.config["python"].get_extras():
            extra_variables += [
                (_get_reqs_file_varname(extra=extra), "requirements-" + extra + ".txt"),
                (_get_reqs_inline_varname(extra=extra), " ".join(python_config.get_inline_requirements(extra=extra))),
            ]

        # Python related environment
        event.makefile.updateleft(
            ("PACKAGE", event.config.package_name),
            ("PYTHON", which("python")),
            ("PYTHON_BASENAME", "$(shell basename $(PYTHON))"),
            ("PYTHON_DIRNAME", "$(shell dirname $(PYTHON))"),
            (_get_reqs_file_varname(), "requirements.txt"),
            (_get_reqs_inline_varname(), " ".join(python_config.get_inline_requirements())),
            *extra_variables,
        )

        event.makefile["PIP"] = "$(PYTHON) -m pip"
        event.makefile["PIP_INSTALL_OPTIONS"] = ""

        if python_config.use_wheelhouse:

            def _get_wheelhouse(extra=None):
                if extra:
                    return ".wheelhouse-" + extra
                return ".wheelhouse"

            def _get_wheelhouse_options(extra=None):
                return "--no-index --find-links=" + _get_wheelhouse(extra=extra)

            def _get_install_commands(extra=None):
                return [
                    "$(PIP) install $(PIP_INSTALL_OPTIONS) "
                    + _get_wheelhouse_options(extra=extra)
                    + ' -U "pip '
                    + PIP_VERSION
                    + '" wheel',
                    "$(PIP) install $(PIP_INSTALL_OPTIONS) "
                    + _get_wheelhouse_options(extra=extra)
                    + " -U $("
                    + _get_reqs_inline_varname(extra=extra)
                    + ") -r $("
                    + _get_reqs_file_varname(extra=extra)
                    + ")",
                ]

            def _get_install_deps(extra=None):
                # TODO add inline requirements without -e/-r ?
                return [
                    ".medikit/" + _get_wheelhouse(extra=extra),
                    "$(" + _get_reqs_file_varname(extra=extra) + ")",
                    "setup.py",
                ]

            for extra in (None, *python_config.get_extras()):
                target = _get_wheelhouse(extra=extra)

                if not event.makefile.has_target(target):
                    event.makefile.add_target(target, InstallScript(), phony=True)

                clean_target = event.makefile.get_clean_target()
                marker = ".medikit/" + target
                if not marker in clean_target.remove:
                    clean_target.remove.append(marker)

                event.makefile.get_target(target).install += [
                    "$(PIP) wheel -w "
                    + _get_wheelhouse(extra=extra)
                    + " $("
                    + _get_reqs_inline_varname(extra=extra)
                    + ") -r $("
                    + _get_reqs_file_varname(extra=extra)
                    + ")"
                ]

        else:

            def _get_install_commands(extra=None):
                return [
                    '$(PIP) install $(PIP_INSTALL_OPTIONS) -U "pip ' + PIP_VERSION + '" wheel',
                    "$(PIP) install $(PIP_INSTALL_OPTIONS) -U $("
                    + _get_reqs_inline_varname(extra=extra)
                    + ") -r $("
                    + _get_reqs_file_varname(extra=extra)
                    + ")",
                ]

            def _get_install_deps(extra=None):
                # TODO add inline requirements without -e/-r ?
                return ["$(" + _get_reqs_file_varname(extra=extra) + ")", "setup.py"]

        for extra in (None, *python_config.get_extras()):
            target = event.makefile.add_install_target(extra)
            target.install += _get_install_commands(extra=extra)
            target.deps += _get_install_deps(extra=extra)

    @subscribe(medikit.on_start, priority=ABSOLUTE_PRIORITY)
    def on_start(self, event):
        """
        **Events**

        - ``medikit.feature.python.on_generate`` (with the same ``ProjectEvent`` we got, todo: why not deprecate
          it in favor of higher priority medikit.on_start?)

        **Files**

        - ``<yourpackage>/__init__.py``
        - ``MANIFEST.in``
        - ``README.rst``
        - ``classifiers.txt``
        - ``requirements-dev.txt``
        - ``requirements.txt``
        - ``setup.cfg``
        - ``setup.py`` (overwritten)

        :param ProjectEvent event:
        """
        self.dispatcher.dispatch(__name__ + ".on_generate", event)

        # Our config object
        python_config = event.config["python"]

        # Some metadata that will prove useful.
        self.render_empty_files("classifiers.txt", "README.rst")
        self.render_file_inline("MANIFEST.in", "include *.txt")
        with event.config.define_resource(ConfigParserResource, "setup.cfg") as setup_cfg:
            setup_cfg.set_initial_values(
                {"bdist_wheel": {"universal": "1"}, "metadata": {"description-file": "README.rst"}}
            )

        # XXX there is an important side effect in get_init_files that defines namespace packages for later use in
        # setup.py rendering. Even if we do not want to create the packages here, it is important to make the call
        # anyway.
        for dirname, filename, context in python_config.get_init_files():
            if python_config.create_packages:
                if not os.path.exists(dirname):
                    os.makedirs(dirname)
                self.render_file(filename, "python/package_init.py.j2", context)

        # render version file, try to import version from version.txt if available.
        try:
            with open("version.txt") as f:
                version = f.read().strip()
        except IOError:
            version = "0.0.0"
        self.render_file_inline(python_config.version_file, "__version__ = '{}'".format(version))

        setup = python_config.get_setup()

        context = {
            "url": setup.pop("url", "http://example.com/"),
            "download_url": setup.pop("download_url", "http://example.com/"),
        }

        for k, v in context.items():
            context[k] = context[k].format(name=setup["name"], user=getuser(), version="{version}")

        context.update(
            {
                "entry_points": setup.pop("entry_points", {}),
                "extras_require": python_config.get("extras_require"),
                "install_requires": python_config.get("install_requires"),
                "python": python_config,
                "setup": setup,
                "banner": get_override_warning_banner(),
            }
        )

        # Render (with overwriting) the allmighty setup.py
        self.render_file("setup.py", "python/setup.py.j2", context, override=True)

    @subscribe(medikit.on_end, priority=ABSOLUTE_PRIORITY)
    def on_end(self, event):
        # Our config object
        python_config = event.config["python"]

        # Pip / PyPI
        repository = PyPIRepository([], cache_dir=CACHE_DIR)

        for extra in itertools.chain((None,), python_config.get_extras()):
            requirements_file = "requirements{}.txt".format("-" + extra if extra else "")

            if python_config.override_requirements or not os.path.exists(requirements_file):
                tmpfile = tempfile.NamedTemporaryFile(mode="wt", delete=False)
                if extra:
                    tmpfile.write("\n".join(python_config.get_requirements(extra=extra)))
                else:
                    tmpfile.write("\n".join(python_config.get_requirements()))
                tmpfile.flush()
                constraints = list(
                    parse_requirements(
                        tmpfile.name, finder=repository.finder, session=repository.session, options=repository.options
                    )
                )
                resolver = Resolver(
                    constraints,
                    repository,
                    cache=DependencyCache(CACHE_DIR),
                    prereleases=False,
                    clear_caches=False,
                    allow_unsafe=False,
                )

                self.render_file_inline(
                    requirements_file,
                    "\n".join(
                        (
                            "-e .{}".format("[" + extra + "]" if extra else ""),
                            *(("-r requirements.txt",) if extra else ()),
                            *python_config.get_vendors(extra=extra),
                            *sorted(
                                format_requirement(req)
                                for req in resolver.resolve(max_rounds=10)
                                if req.name != python_config.get("name")
                            ),
                        )
                    ),
                    override=python_config.override_requirements,
                )
