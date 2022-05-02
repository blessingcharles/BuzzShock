from flask import request
from core.types.abnfToken import ABNFToken
from core.types.httpBuzzTokens import DefaultGadgets, MandatoryGadgetTokens, GadgetTokens

class HttpRequestPrototype:
    def __init__(self, gadgets: None, method: str = "GET", request_target: str = "/", http_version: str = "1.1") -> None:
        """
            Http Request Prototype
        """
        self.header = ""
        self.request_line = f"{method}{GadgetTokens.__SP__}{request_target}{GadgetTokens.__SP__}HTTP{GadgetTokens.__SHOCKER__}/{http_version}{GadgetTokens.__CRLF__}"
        self.body = None
        self.gadgets = gadgets or DefaultGadgets

    def addHeader(self, key, val):
        """
            Gadgets :
                {GadgetTokens.__SHOCKER__} = shocking to the server parsers
                {GadgetTokens.__SP__}      =  space char
                {GadgetTokens.__CRLF__}    = \r\n
        """

        # we can insert a random char in shocker
        self.header += f"{key}{GadgetTokens.__SHOCKER__}:{GadgetTokens.__SP__}{val}{GadgetTokens.__CRLF__}"

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        for g in MandatoryGadgetTokens:
            if g not in self.gadgets:
                raise AttributeError(f"Mandatory Gadget {g} not present")

        request: str = ""
        if self.body:
            self.addHeader("Content-Length", str(len(self.body)))

        request += self.request_line + self.header + GadgetTokens.__CRLF__ + self.body

        for g_key, g_value in self.gadgets.items():
            request = request.replace(g_key, g_value)
    
        return request
