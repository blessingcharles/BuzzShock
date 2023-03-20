from logging import error
import os
import signal
import sys
from utils.logger import Bzlogger


def dir_create(dirname):

    pwd = os.getcwd()

    new_dir_path = os.path.join(pwd, dirname)
    if not os.path.exists(new_dir_path):
        try:
            os.mkdir(new_dir_path)
            return new_dir_path
        except error as e:
            Bzlogger.error(e)
    return new_dir_path


def signal_handler(sig, frame):
    Bzlogger.warning('You pressed [Ctrl+C] : ( . Have a nice day . ')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def userinput_continuation(message):
    inp = input("[?] Do you want to continue for more checks?[Y/n] :")
    if inp.lower()[0] == "n":
        exit(0)
