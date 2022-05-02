from tabnanny import verbose
from urllib.parse import urlparse

from core.engines.cerberus import Cerberus
from utils.args import buzzShockArgs

def getHostPort(protocol : str , endpoint : str ) :
    if protocol == "http" or protocol == "https":
        parsed_obj = urlparse(endpoint)
        ll = parsed_obj.netloc.split(":") 
        return ll[0] , int(ll[1])

if __name__ == "__main__":

    endpoint , protocol , engines_list , plugins_list , verbose = buzzShockArgs()

    if engines_list:
        engines_list = engines_list.split(",")
    else:
        engines_list = []
    
    if plugins_list:
        plugins_list = plugins_list.split(",")
    else:
        plugins_list = []

    host , port = getHostPort(protocol , endpoint)
    cb = Cerberus(protocol , host , port , endpoint , engines_list , plugins_list , verbose=verbose)

    cb.run()