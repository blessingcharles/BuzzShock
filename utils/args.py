import argparse
from ast import arg
from isort import file

from yaml import parse

from utils.banner import banner


def buzzShockArgs() -> tuple:

    parser = argparse.ArgumentParser(
        description="Buzz Shocker - Protocol Analyzer")

    parser.add_argument("-e", "--endpoint", dest="endpoint",
                        help="provide the endpoint for the protocol", required=True)
    parser.add_argument("-pt", "--protocol", dest="protocol",
                        help="provide the endpoint for the protocol", required=True)
    parser.add_argument("-el", "--engines-list",
                        dest="engines_list", help="engines-list", nargs="?")
    parser.add_argument("-pl", "--plugins-list",
                        dest="plugins_list", help="plugins list", nargs="?")
    parser.add_argument("-v", "--verbose", action="store_true",
                        dest="verbose", help="set verbose level", default=False)
    parser.add_argument("-od", "--output-dir", dest="output_dir",
                        help="specify the output directory name", default="output")
    parser.add_argument("-t", "--threads", dest="threads",
                        default=8, type=int, help="specify the number of threads")

    parser.add_argument("-g", "--grammar-file", dest="grammar_file",
                        default=None, help="specify the http abnf grammar file")

    args = parser.parse_args()

    return (args.endpoint, args.protocol, args.engines_list,
            args.plugins_list, args.output_dir, args.threads, args.verbose, args.grammar_file
            )
