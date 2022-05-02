import os
from tabnanny import verbose
from urllib.parse import urlparse

from core.engines.cerberus import Cerberus
from utils.args import buzzShockArgs
from utils.utils import dir_create


def getHostPort(protocol: str, endpoint: str):
    if protocol == "http" or protocol == "https":
        parsed_obj = urlparse(endpoint)
        ll = parsed_obj.netloc.split(":")
        return ll[0], int(ll[1])


if __name__ == "__main__":

    endpoint, protocol, engines_list, plugins_list, output_dir, threads, verbose = buzzShockArgs()

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
    cb = Cerberus(protocol=protocol, host=host, port=port, output_dir=output_dir, endpoint=endpoint,
                  engines_list=engines_list, plugins_list=plugins_list, threads=threads, verbose=verbose)

    cb.run()

