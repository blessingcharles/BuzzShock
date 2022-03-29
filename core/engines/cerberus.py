import importlib
import pkgutil
from pprint import pprint

discovered_engines = {
    name: importlib.import_module(f"core.engines.{name}") for finder, name, ispkg in pkgutil.iter_modules(["core/engines"])
    if name.endswith("Engine")
}

discovered_plugins = {
    name: importlib.import_module(f"core.plugins.{name}") for finder, name, ispkg in pkgutil.iter_modules(["core/plugins"])
    if name.endswith("Plugin")
}

class Cerberus:
    def __init__(self) -> None:
        """
            Heart of the Tool
        """
        pass
