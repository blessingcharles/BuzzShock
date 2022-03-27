
"""
    Token Types for the ABNF grammar

    1. SPACE TOKEN
    2. EQUAL SIGN
    3. NEWLINE TOKEN
    4. SPECIAL OPERATORS
    5. GROUPING OPERATORS
    6. STRING START
    7. COMMENT
    8. BUZZSHOCK
"""


from tokenize import Token
from typing import List
import typing


class ABNFToken:

    SPACE_TOKEN = " \t"
    SEPERATOR = "/"
    DELIMETER = "="
    NEWLINE_TOKEN = "\n"
    QUANTIFIERS = "*+"
    GROUPING_OPERATORS = "([)]"
    STRING_START = "\"\'"
    COMMENT = ";"
    BUZZSHOCK = "`"

    def __init__(self, type: str, value: str, lin_no: int = -1, column_no: int = -1, isTerminal: bool = False, info: dict = {}):
        self._id: str = f"{type}-{value}"
        self._type: str = type
        self._value: str = value

        self.lin_no: int = lin_no
        self.column_no: int = column_no
        self.info: dict = info
        self.children: List[ABNFToken] = []
        self.isTerminal: bool = isTerminal

    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._value

    def __hash__(self) -> int:
        return hash((self._type, self._value))

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, ABNFToken):
            return False

        return self._type == __o._type and self._value == __o._value

    def __repr__(self) -> str:

        if self.info:
            return "{"+f"type : {self.type} , value : {self.value}] INFO : {self.info}"+"}"

        return "{" + f" type : {self.type} , value : {self.value} " + "}"

    def __str__(self) -> str:

        return f"[type : {self.type} , value : {self.value}]"


class ABNFTokenType:
    SPACE_TOKEN = "space token"
    DELIMETER = "abnf delimeter"
    NEWLINE_TOKEN = "newline"
    QUANTIFIERS = "quantiers"
    GROUPING_OPERATORS = "grouping operators"
    TERMINAL = "terminal"
    NON_TERMINAL = "non terminal"
    SEPERATOR = "seperator"
    COMMENT = "abnf comments"
    BUZZSHOCK = "buzz shock"

ABNFTokenDict = typing.Dict[ABNFToken , List[ABNFToken]]