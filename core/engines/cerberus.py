from concurrent.futures import ThreadPoolExecutor
import importlib
from optparse import Values
import os
import pkgutil
from pprint import pprint
from time import sleep
from requests import request

from core.engines.coreEngine import CoreEngine
from core.engines.httpBuzzEngine import BytesIOSocket
from utils.logger import Bzlogger, Logger


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


class Cerberus(CoreEngine):
    def __init__(self, protocol: str, host: str, port: int, output_dir: str, threads: int, endpoint: str = "",
                 engines_list: list = [], plugins_list=[], gadgets_dict: dict = None,
                 verbose: bool = False, timeout: int = 5, buffsize: int = 8192, reuse_socket: bool = False, is_ssl: bool = False,
                 sleepingtime: int = 0.5, log_file: str = None) -> None:
        """
            Steering to run various plugins and engines to fuzz protocols

            Attributes
            -------------
            protocol : str
            host : str
            port : int
            output_dir : str
            threads : int
            endpoint : str
            engines_list : list
            plugins_list : list
            gadgets_dict : list
            verbose : bool
            timeout : int
            buffsize : int
            reuse_socket : bool
            sleepingtime : int
            log_file : str

            Methods
            ----------
            run:
                run plugins and engines based on the arguments passed

        """
        super().__init__(host, port, timeout, buffsize,
                         reuse_socket, is_ssl, sleepingtime, log_file)

        self.protocol = protocol
        self.endpoint = endpoint
        self.threads = threads

        self.engine_list = engines_list
        self.plugins_list = plugins_list
        self.gadget_dict = gadgets_dict

        self.output_dir = output_dir
        self.verbose = verbose

    def run(self):
        # run the given plugins
        for plugin_name in self.plugins_list:

            print("Running Plugin : ", plugin_name)

            output_file = self.output_dir + \
                f"/{plugin_name}__port{self.port}.txt"

            self.lg = Logger(filename=output_file)

            Bzlogger.info(output_file)

            plugin_module = discovered_plugins[plugin_name]
            plugin_class = getattr(plugin_module, plugin_name)

            # creating an instance of the plugin class
            plugin = plugin_class(
                self.endpoint, self.gadget_dict, self.verbose)
            payload_set = plugin.generate()

            # payload set will contains all

            with ThreadPoolExecutor(max_workers=self.threads) as exec:
                for key, value in payload_set.items():
                    exec.submit(self.__buzz_jobs, key, value)

    def __buzz_jobs(self, key, value):
        Bzlogger.info("payload type : " + key)
        if self.verbose:
            result = self.launchCustomPayload(value)
            resp = BytesIOSocket.response_from_bytes(result)
            Bzlogger.success("Request")
            Bzlogger.printer(str(value))
            Bzlogger.success(f"Response : {resp.status}")
            Bzlogger.info(
                f"{self.__extractHeaders(resp.getheaders())}\n\n{resp.data}")

        self.lg.logTofile(
            f"\n---PayloadType : {key}----\nRequest\n{str(value)}\nResponse: {resp.status}\n{self.__extractHeaders(resp.getheaders())}{resp.data}")

    def __extractHeaders(self, headerDict):
        obj = {}
        for key, value in headerDict.items():
            obj[key] = value
        return obj
