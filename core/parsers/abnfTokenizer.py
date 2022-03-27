from distutils.command.build import build
from typing import List
from isort import file
from pyparsing import Char

from core.types.abnfToken import ABNFToken, ABNFTokenType


class Tokenizer:
    def __init__(self, file_name: str) -> None:
        """
            tokenize ABNF grammar
        """
        self.__file_name: str = file_name
        self.__file_contents: str = self.__get_contents()
        self.field_seperators_idx: List[int] = []
        self.abnf_tokens: List[ABNFToken] = []
        self.pos: int = 0
        self.col: int = 0
        self.line_no: int = 1
        self.cur_char: str = self.__file_contents[0]

    def step_ahead(self):
        prev_char = ""
        if self.pos > 0:
            prev_char = self.__file_contents[self.pos-1]

        self.pos += 1
        self.col += 1

        if prev_char == "\n":
            self.col = 0

        self.cur_char = self.__file_contents[self.pos] if self.pos < len(self.__file_contents) else None

    def build_terminal(self) -> ABNFToken:
        cur_character = self.cur_char
        terminal_val = ""
        self.step_ahead()

        while self.cur_char != cur_character:
            terminal_val += self.cur_char
            self.step_ahead()
        self.step_ahead()
        return ABNFToken(ABNFTokenType.TERMINAL, terminal_val, self.line_no, self.col, isTerminal=True)

    def build_nonterminal(self) -> ABNFToken:
        nonterminal_val = ""
        breakers = ABNFToken.SPACE_TOKEN + ABNFToken.DELIMETER + ABNFToken.NEWLINE_TOKEN + ABNFToken.SEPERATOR

        while self.cur_char not in breakers:
            nonterminal_val += self.cur_char
            self.step_ahead()

        return ABNFToken(ABNFTokenType.NON_TERMINAL , nonterminal_val , self.line_no , self.col)

    def build_comments(self) -> ABNFToken:
        comment_val = ""

        self.step_ahead()
        while self.cur_char is not None and self.cur_char not in ABNFToken.NEWLINE_TOKEN:
            comment_val += self.cur_char
            self.step_ahead()
        
        return ABNFToken(ABNFTokenType.COMMENT , comment_val , self.line_no , self.col)

    def build_buzzshock(self) -> ABNFToken:
        token_val = ""
        self.step_ahead()

        while self.cur_char not in ABNFToken.BUZZSHOCK:
            token_val += self.cur_char
            self.step_ahead()

        self.step_ahead()
        return ABNFToken(ABNFTokenType.BUZZSHOCK , token_val , self.line_no , self.col)
        
    def tokenize(self, include_comments : bool = False):

        while self.cur_char != None:

            if self.cur_char in ABNFToken.SPACE_TOKEN or self.cur_char in ABNFToken.SEPERATOR:
                self.step_ahead()
            elif self.cur_char in ABNFToken.NEWLINE_TOKEN:
                self.line_no += 1
                self.step_ahead()

            elif self.cur_char in ABNFToken.DELIMETER:
                """
                    For ABNF equal sign is delimeter between key value pair so store its
                    index to make parsing easier 
                """
                idx = len(self.abnf_tokens)
                self.field_seperators_idx.append(idx)

                t = ABNFToken(ABNFTokenType.DELIMETER,
                              ABNFToken.DELIMETER, self.line_no, self.col)
                self.abnf_tokens.append(t)
                self.step_ahead()
            
            elif self.cur_char in ABNFToken.COMMENT:
                """
                    ; is the start of comment which ends at newline
                """
                t = self.build_comments()
                if include_comments:
                    self.abnf_tokens.append(t)

            elif self.cur_char in ABNFToken.STRING_START:
                """
                    Parse the given terminal token eg : "value"
                """
                t = self.build_terminal()
                self.abnf_tokens.append(t)
            elif self.cur_char in ABNFToken.BUZZSHOCK:
                """
                    Parse the given Fuzzing keyword
                """
                t = self.build_buzzshock()
                self.abnf_tokens.append(t)

            elif self.cur_char in ABNFToken.GROUPING_OPERATORS:
                """
                    TODO: grouping and sequence characters
                """
                pass
            elif self.cur_char in ABNFToken.QUANTIFIERS:
                """
                    TODO: Quantifiers charaters
                """
                pass
            else:
                """
                    non terminal tokens split it untill newline or space or tab or / or = occurs
                """
                t = self.build_nonterminal()
                self.abnf_tokens.append(t)

    def __get_contents(self) -> str:
        try:
            with open(self.__file_name, "r") as f:
                file_contents = f.read()
            return file_contents
        except:
            print("Failed to open file ", self.__file_name)
