
import importlib
import pkgutil

"""
importing engines and plugins and store it as key value pair in the dictionary object

eg:
    discovered_plugins["HttpTeClPlugin"] = HttpTeClPlugin <class>
"""
discovered_engines = {
    name: importlib.import_module(f"core.engines.{name}") for finder, name, ispkg in pkgutil.iter_modules(["core/engines"])
    if name.endswith("Engine")
}

discovered_plugins = {
    name: importlib.import_module(f"core.plugins.{name}") for finder, name, ispkg in pkgutil.iter_modules(["core/plugins"])
    if name.endswith("Plugin")
}
