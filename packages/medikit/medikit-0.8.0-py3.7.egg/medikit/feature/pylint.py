"""
Lint your python code with pylint.

This feature may be outdated.

"""
from medikit.events import subscribe

from . import SUPPORT_PRIORITY, Feature


class PylintFeature(Feature):
    requires = {"python"}

    @subscribe("medikit.feature.python.on_generate")
    def on_python_generate(self, event):
        event.config["python"].add_requirements(dev=["pylint ~=1.8"])

    @subscribe("medikit.feature.make.on_generate", priority=SUPPORT_PRIORITY)
    def on_make_generate(self, event):
        makefile = event.makefile
        makefile.add_target(
            "lint",
            """
            $(PYTHON_DIRNAME)/pylint --py3k $(PACKAGE) -f html > pylint.html
        """.format(
                name=event.package_name
            ),
            deps=("install-dev",),
            phony=True,
        )
