from cleo import Application
from simple_plugin_loader import Loader
from pathlib import Path
from . import singleton
from .command import Command


def main(name, file, app_name=None, appvesion=None):

    if name != "__main__":
        return

    app_dir = Path(file).parent
    singleton.app_dir = app_dir
    application = Application(app_name, appvesion)
    loader = Loader()

    # Load command classes found in the "commands" dir
    commands_dir = Path(app_dir, "commands")
    command_modules = loader.load_plugins(commands_dir, Command)
    cmds = [x() for x in command_modules.values()]
    application.add_commands(*cmds)
    application.run()
