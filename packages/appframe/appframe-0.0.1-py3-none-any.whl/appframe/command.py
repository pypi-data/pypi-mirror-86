from cleo import Command as CleoCommand
from . import singleton


class Command(CleoCommand):
    def wrap_handle(self, args, io, command):
        self._args = args
        self._io = io
        self._command = command
        singleton.verbosity = io.verbosity

        return self.handle()
