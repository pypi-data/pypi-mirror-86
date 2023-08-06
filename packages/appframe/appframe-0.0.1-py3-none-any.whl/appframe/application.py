from pathlib import Path
from eprint import eprint
from eprint.str import info
import importlib
from . import singleton
from .log import verbose


class Application:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def run(self):
        eprint.info("Starting application from {}", singleton.app_dir)
        features_dir = Path(singleton.app_dir, "features").resolve()
        for file_path in Path(features_dir).glob("*.py"):
            feature_name = file_path.stem
            verbose(1, info("Loading feature from {}", file_path))
            #  feature_module = import_module()
            spec = importlib.util.spec_from_file_location(
                f"webplane.app_features.{feature_name}", file_path
            )
            feature_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(feature_module)
            #  print(feature_module.webplane)
            feature_module.activate(*self.args, **self.kwargs)
