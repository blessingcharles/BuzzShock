from datetime import datetime
import colorama
import re


class Logger:
    def __init__(self , to_stdout : bool = True ,is_color : bool = True ,filename : str = None ) -> None:
        self.to_stdout = to_stdout
        self.filename = filename
        self.is_color = is_color
        self.ansi_chars = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
        if filename:
            self.filehandler = open(filename , "w+")

    def log(self , msg : str , symbol : str = "+"):
        plaintext = self.ansi_chars.sub('', msg)
        if self.is_color:
            msg = colorama.Style.BRIGHT + colorama.Fore.MAGENTA + "[%s] %s"%(colorama.Fore.CYAN+symbol+colorama.Fore.MAGENTA, msg) + colorama.Style.RESET_ALL
            print(msg)
        else:
            print(plaintext)

        if self.filename is not None:
            self.filehandler.write(plaintext+"\n")

    def logTofile(self , msg : str):

        plaintext = self.ansi_chars.sub('', msg)
        self.filehandler.write(plaintext+"\n")

    def logWithTime(self , msg : str , symbol : str = "+"):
        t = datetime.now().strftime("%H:%M:%S")
        msg = f"{colorama.Fore.GREEN}({t}){colorama.Style.RESET_ALL} {msg}"
        self.log(msg,symbol)

    def close(self):
        self.filehandler.close()
        
# general logger
printer = Logger()

class Bzlogger:

    @staticmethod
    def print_general(color , message : str , tag : str = "[.] ", *args):
        message = color + f"{tag}{message} "
        for arg in args:
            message =  message + " " + arg

        message += colorama.Style.RESET_ALL
        print(message)

    @staticmethod
    def info(message : str , *args):
        Bzlogger.print_general(color=colorama.Fore.BLUE , tag="[*] " , message=message , *args)

    @staticmethod
    def error(message : str , *args):
        Bzlogger.print_general(color=colorama.Fore.RED , tag="[-] " , message=message , *args)

    @staticmethod
    def success(message : str , *args):
        Bzlogger.print_general(color=colorama.Fore.GREEN , tag="[+] " , message=message , *args)

    @staticmethod
    def warning(message : str , *args):
        Bzlogger.print_general(color=colorama.Fore.YELLOW , tag="[#] " , message=message , *args)
    
    @staticmethod
    def printer(message : str , *args):
        Bzlogger.print_general(color=colorama.Fore.LIGHTBLUE_EX , tag="" , message=message , *args)

    @staticmethod
    def crprinter(message : str , left_justify : int = 580):
        message = colorama.Fore.LIGHTCYAN_EX + f"{message}"+" "*100

        message += colorama.Style.RESET_ALL
        message.rjust(left_justify)
        print(message , end="\r")