"""
YAPF support, to automatically reformat all your (python) source code.

.. code-block:: shell-session

    $ make format

"""

import os
import warnings

import medikit
from medikit import settings
from medikit.events import subscribe
from medikit.feature import ABSOLUTE_PRIORITY, SUPPORT_PRIORITY, Feature
from medikit.structs import Script


class YapfFeature(Feature):
    requires = {"python"}
    conflicts = {"format"}

    def __init__(self, dispatcher):
        super().__init__(dispatcher)
        warnings.warn(
            'The "yapf" feature is deprecated, please switch to "format" feature and call .using("yapf") on its configuration object.',
            DeprecationWarning,
        )

    @subscribe("medikit.feature.python.on_generate")
    def on_python_generate(self, event):
        event.config["python"].add_requirements(dev=["yapf"])

    @subscribe("medikit.feature.make.on_generate", priority=SUPPORT_PRIORITY)
    def on_make_generate(self, event):
        makefile = event.makefile
        makefile["YAPF"] = "$(PYTHON) -m yapf"
        makefile["YAPF_OPTIONS"] = "-rip"
        makefile.add_target(
            "format",
            Script("\n".join(["$(YAPF) $(YAPF_OPTIONS) .", "$(YAPF) $(YAPF_OPTIONS) Projectfile"])),
            deps=("install-dev",),
            phony=True,
            doc="Reformats the whole python codebase using yapf.",
        )

    @subscribe(medikit.on_start, priority=SUPPORT_PRIORITY)
    def on_start(self, event):
        self.render_file(".style.yapf", "yapf/style.yapf.j2")

    @subscribe(medikit.on_start, priority=ABSOLUTE_PRIORITY - 1)
    def on_before_start(self, event):
        style_config = os.path.join(os.getcwd(), ".style.yapf")
        if os.path.exists(style_config):
            self.dispatcher.info("YAPF_STYLE_CONFIG = " + style_config)
            settings.YAPF_STYLE_CONFIG = style_config
