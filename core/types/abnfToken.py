class ABNFToken:

    def __init__(self, type : str, value :str ,lin_no , column_no : int , info : dict = {}):
        
        self._type : str = type
        self._value : str  = value

        self.lin_no : int = lin_no
        self.column_no : int = column_no 
        self.info : dict = info

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._value 

    def __hash__(self) -> int:
        return hash((self._type , self._value))

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o , ABNFToken):
            return False

        return self._type == __o._type and self._value == __o._value
        
    def __repr__(self) -> str:

        return f"[type : {self.type} , value : {self.value}] \
                INFO : {self.info}"

    def __str__(self) -> str:

        return f"[type : {self.type} , value : {self.value}]"

"""
    Token Types for the ABNF grammar

    1. SPACE TOKEN
    2. EQUAL SIGN
    3. NEWLINE TOKEN
    4. SPECIAL OPERATORS
    5. GROUPING OPERATORS
"""

SPACE_TOKEN = " \t"
EQUAL_SIGN = "="
NEWLINE_TOKEN = "\n"
SPECIAL_OPERATORS = "*+"
GROUPING_OPERATORS = "([)]"
