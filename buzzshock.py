import copy
import os
from tabnanny import verbose
from time import sleep
from urllib.parse import urlparse

from core.engines import discovered_engines, discovered_plugins
from core.engines.cerberus import Cerberus
from core.engines.grammarEngine import GrammarEngine
from core.mutators.httpMutator import HttpMutator
from core.parsers.abnfParsers import ABNFParser
from utils.args import buzzShockArgs
from utils.logger import Bzlogger
from utils.utils import dir_create
from config import CONFIG


def getHostPort(protocol: str, endpoint: str):
    if protocol == "http" or protocol == "https":
        parsed_obj = urlparse(endpoint)
        ll = parsed_obj.netloc.split(":")
        return ll[0], int(ll[1])


if __name__ == "__main__":

    endpoint, protocol, engines_list, plugins_list, output_dir, \
        threads, verbose, grammar_file, mutants_count = buzzShockArgs()

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
    Bzlogger.printer("Output directory : " + output_dir)
    Bzlogger.info("Worker Threads : " + str(threads))
    Bzlogger.info("Verbose : " + str(verbose))

    Bzlogger.success("Loaded Plugins : " + str(len(discovered_plugins)))
    Bzlogger.success("Loaded Engines : " + str(len(discovered_engines)))

    if grammar_file:
        Bzlogger.info("Grammar File Path: " + grammar_file)
        if os.path.exists(grammar_file):
            Bzlogger.printer("File Exists")
        Bzlogger.info("Mutants Count: " + str(mutants_count))

    sleep(CONFIG['sleeping-time'])

    if plugins_list or engines_list:
        # Running the plugins and engines
        cb = Cerberus(protocol=protocol, host=host, port=port, output_dir=output_dir, endpoint=endpoint,
                      engines_list=engines_list, plugins_list=plugins_list, threads=threads, verbose=verbose)

        cb.run()

    sleep(CONFIG['sleeping-time'])

    # mutate the given abnf request
    if grammar_file:
        g_engine = GrammarEngine(
            grammar_file=grammar_file, mutants_count=mutants_count, host=host, port=port, verbose=verbose)
        g_engine.run()
