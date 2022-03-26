
from pprint import pprint
from core.parsers.abnfTokenizer import Tokenizer
from core.types.abnfToken import ABNFToken, ABNFTokenType


class ABNFParser:
    def __init__(self, source_file: str) -> None:
        """ 
            Args:
                source_file: file path to the ABNF grammar
            Return:
                ABNF parser object
        """
        self.src = source_file
        self.abnf_obj = {}
        self.tokens_count = 0

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
        self.tokens_count = len(tt.abnf_tokens)

        for idx in tt.field_seperators_idx:
            cur_key = tt.abnf_tokens[idx-1]
            self.abnf_obj[cur_key] = []

            token_vals_idx = idx+1
            """
                Untill next key occur collect all the token and map it to the key
            """
            while token_vals_idx+1 < self.tokens_count and tt.abnf_tokens[token_vals_idx+1].value not in ABNFToken.DELIMETER:
                self.abnf_obj[cur_key].append(tt.abnf_tokens[token_vals_idx])
                token_vals_idx += 1

        nxt_one = self.abnf_obj[ABNFToken(ABNFTokenType.NON_TERMINAL, "start")]

        print(self.abnf_obj[nxt_one[0]])
