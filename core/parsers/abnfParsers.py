
from pprint import pprint
from core.parsers.abnfTokenizer import Tokenizer


class ABNFParser:
    def __init__(self , source_file : str) -> None:
        """ 
            Args:
                source_file: file path to the ABNF grammar
            Return:
                ABNF parser object
        """
        self.src = source_file
        self.abnf_obj = {}
        self.abnf_keys_idx = []
        
    def __find_key_idx(self ,tokens_list):
        """
            Find the keys index (ie find previous index of = sign)
            Args:
                tokens_list: list of grammar tokens
            Return:
                None 
        """
        pass

    def parse(self):
        """
            Parse the given ABNF grammar file into python grammar object
            Args:
                None
            Return:
                None
        """  
        tt = Tokenizer(self.src)
        tt.tokenize()
        pprint(tt.abnf_tokens)
        pprint(tt.field_seperators_idx)
    