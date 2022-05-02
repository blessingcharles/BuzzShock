from flask import request
from core.types.abnfToken import ABNFToken
from core.types.httpBuzzTokens import DefaultGadgets, MandatoryGadgetTokens, GadgetTokens

class HttpRequestPrototype:
    def __init__(self, gadgets: None, method: str = "GET", request_target: str = "/", http_version: str = "1.1" , add_default_cl : bool = True) -> None:
        """
            A class used to generate Http Request by manipulating various fuzzing places
            ...

            Attributes
            ---------------
            request_line : str
                default request line for <= http/1.1 protocol
            body : str
                http body
            gadgets : dict
                random replacers for crlf , spaces , shocking insertion
            add_default_cl : bool
                will the class need to add content length header for body while __str__ conversion

            Methods
            -------------
            addHeader(key , val)
                add headers to the request object
                
        """
        self.header = ""
        self.request_line = f"{method}{GadgetTokens.__SP__}{request_target}{GadgetTokens.__SP__}HTTP{GadgetTokens.__SHOCKER__}/{http_version}{GadgetTokens.__CRLF__}"
        self.body = None
        self.gadgets = gadgets or DefaultGadgets
        self.add_default_cl = add_default_cl

    def addHeader(self, key : str , val : str ):
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
        if self.body and self.add_default_cl:
            self.addHeader("Content-Length", str(len(self.body)))

        request += self.request_line + self.header + GadgetTokens.__CRLF__ + self.body

        for g_key, g_value in self.gadgets.items():
            request = request.replace(g_key, g_value)
    
        return request
