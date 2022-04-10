import importlib
import pkgutil
from pprint import pprint
from typing import List

from core.engines.coreEngine import CoreEngine

discovered_engines = {
    name: importlib.import_module(f"core.engines.{name}") for finder, name, ispkg in pkgutil.iter_modules(["core/engines"])
    if name.endswith("Engine")
}

discovered_plugins = {
    name: importlib.import_module(f"core.plugins.{name}") for finder, name, ispkg in pkgutil.iter_modules(["core/plugins"])
    if name.endswith("Plugin")
}

class Cerberus(CoreEngine):
    def __init__(self ,protocol : str ,config_obj , engines_list : list , plugins_list = []) -> None:
        """
            Heart of the Tool
        """
        self.protocol = protocol
        self.engine_list = engines_list
        self.plugins_list = plugins_list

