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
            self.filehandler = open(filename , "w")

    def log(self , msg : str , symbol : str = "+"):
        plaintext = self.ansi_chars.sub('', msg)
        if self.is_color:
            msg = colorama.Style.BRIGHT + colorama.Fore.MAGENTA + "[%s] %s"%(colorama.Fore.CYAN+symbol+colorama.Fore.MAGENTA, msg) + colorama.Style.RESET_ALL
            print(msg)
        else:
            print(plaintext)

        if self.filename is not None:
            self.filehandler.write(plaintext+"\n")

    def logWithTime(self , msg : str , symbol : str = "+"):
        t = datetime.now().strftime("%H:%M:%S")
        msg = f"{colorama.Fore.GREEN}({t}){colorama.Style.RESET_ALL} {msg}"
        self.log(msg,symbol)

# general logger
printer = Logger()
