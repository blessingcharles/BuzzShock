import argparse
from ast import arg

from yaml import parse

from utils.banner import banner

def buzzShockArgs() -> tuple:

    parser = argparse.ArgumentParser(description="Buzz Shocker - Protocol Analyzer")

    parser.add_argument("-e" , "--endpoint" , dest="endpoint" , help="provide the endpoint for the protocol" , required=True)
    parser.add_argument("-pt" , "--protocol" , dest="protocol" , help="provide the endpoint for the protocol" , required=True)
    parser.add_argument("-el" , "--engines-list" ,dest="engines_list" , help="engines-list" , nargs="?")
    parser.add_argument("-pl" , "--plugins-list" ,dest="plugins_list" , help="plugins list" , nargs="?" )
    parser.add_argument("-v" , "--verbose" , action="store_true" , dest="verbose" , help="set verbose level" , default=False) 
    args = parser.parse_args()

    return (args.endpoint , args.protocol , args.engines_list , args.plugins_list , args.verbose )