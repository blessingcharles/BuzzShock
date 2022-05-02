import importlib
import pkgutil
from pprint import pprint
from time import sleep
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
    def __init__(self, protocol: str, host: str, port: int,endpoint: str = "",
                 engines_list: list = [], plugins_list=[], gadgets_dict: dict = None,
                 verbose: bool = False, timeout: int = 5, buffsize: int = 8192, reuse_socket: bool = False, is_ssl: bool = False,
                 sleepingtime: int = 0.5, log_file: str = None) -> None:
        
        super().__init__(host, port , timeout, buffsize, reuse_socket, is_ssl, sleepingtime, log_file)

        self.protocol = protocol
        self.endpoint = endpoint
        self.engine_list = engines_list
        self.plugins_list = plugins_list
        self.gadget_dict = gadgets_dict
        self.verbose = verbose

    def run(self):
        # run the given plugins
        print(self.plugins_list)
        for plugin_name in self.plugins_list:

            print("Running Plugin : ", plugin_name)
            
            plugin_module = discovered_plugins[plugin_name]
            plugin_class = getattr(plugin_module , plugin_name) 

            # creating an instance of the plugin class
            plugin = plugin_class(self.endpoint, self.gadget_dict, self.verbose)
            payload_set = plugin.generate()

            # payload set will contains all
            for key, value in payload_set.items():
                # if self.verbose:
                print("[+] Payload type : " , key)
                pprint(repr(value))
                result = self.launchCustomPayload(value)
                print(result)
                sleep(2)

