from logging import error
import os 
import signal
import sys

def dir_create(dirname):

    pwd = os.getcwd()

    new_dir_path = os.path.join(pwd,dirname)
    print(new_dir_path)
    if not os.path.exists(new_dir_path):
        try:
            os.mkdir(new_dir_path)
            return new_dir_path
        except error as e:
            print(e)
            pass

    return new_dir_path

def signal_handler(sig, frame):
    print('You pressed [Ctrl+C] : ( ')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

