from . import singleton


def verbose(level: int, message: str):
    if singleton.verbosity >= level:
        print(message)
