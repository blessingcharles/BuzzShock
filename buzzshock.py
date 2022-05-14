import os
from tabnanny import verbose
from time import sleep
from urllib.parse import urlparse

from core.engines import discovered_engines, discovered_plugins
from core.engines.cerberus import Cerberus
from core.parsers.abnfParsers import ABNFParser
from utils.args import buzzShockArgs
from utils.logger import Bzlogger
from utils.utils import dir_create


def getHostPort(protocol: str, endpoint: str):
    if protocol == "http" or protocol == "https":
        parsed_obj = urlparse(endpoint)
        ll = parsed_obj.netloc.split(":")
        return ll[0], int(ll[1])


if __name__ == "__main__":

    endpoint, protocol, engines_list, plugins_list, output_dir, threads, verbose, grammar_file = buzzShockArgs()

    if engines_list:
        engines_list = engines_list.split(",")
    else:
        engines_list = []

    if plugins_list:
        plugins_list = plugins_list.split(",")
    else:
        plugins_list = []

    host, port = getHostPort(protocol, endpoint)

    output_dir = os.getcwd() + "/" + output_dir

    dir_create(output_dir)
    Bzlogger.success("Output directory : " + output_dir)
    Bzlogger.info("Worker Thread : " + str(threads))
    Bzlogger.info("Verbose : " + str(verbose))

    if grammar_file:
        Bzlogger.info("Grammar File Path: " + grammar_file)
        if os.path.exists(grammar_file):
            Bzlogger.success("File Exists")
    
    Bzlogger.success("Loaded Plugins : " + str(len(discovered_plugins)))
    Bzlogger.success("Loaded Engines : " + str(len(discovered_engines)))
    
    sleep(2)

    if plugins_list or engines_list:
        # Running the plugins and engines
        cb = Cerberus(protocol=protocol, host=host, port=port, output_dir=output_dir, endpoint=endpoint,
                    engines_list=engines_list, plugins_list=plugins_list, threads=threads, verbose=verbose)

        cb.run()

    # mutate the given abnf request
    if grammar_file:
        
        p = ABNFParser(grammar_file)
        p.parse()

        
