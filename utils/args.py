import argparse

from utils.banner import banner

def buzzShockArgs() -> tuple:

    parser = argparse.ArgumentParser(description="Buzz Shocker - Protocol Analyzer")

    args = parser.parse_args()

    return ()