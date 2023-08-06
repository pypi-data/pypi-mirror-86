import shlex
import subprocess
from logging import getLogger

from medikit.utils import run_command


class Step:
    @property
    def logger(self):
        try:
            return self._logger
        except AttributeError:
            self._logger = getLogger(self.__class__.__module__)
            return self._logger

    @property
    def complete(self):
        return self._state.get("complete", False)

    def set_complete(self, value=True):
        self._state["complete"] = bool(value)

    def __init__(self):
        self._state = {}
        self.__args__ = ()
        self.config = None

    def __str__(self):
        return "{}({})".format(type(self).__name__, ", ".join(map(repr, self.__args__)))

    def get_state(self):
        return self._state

    def set_state(self, state):
        self._state = state

    def init(self):
        pass

    def run(self, meta):
        self.set_complete()

    def abort(self):
        pass

    def exec(self, command):
        return run_command(command, logger=self.logger)
