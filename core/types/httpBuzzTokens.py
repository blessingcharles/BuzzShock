
class RequiredTokens:
    __URL__ = "__URL__"


class CustomTokens:
    __HOST__ = "__HOST__"
    __REQUEST_TARGET__ = "__REQUEST_TARGET__"
    __BUZZ_ID__ = "__BUZZ_ID__"
    __RANDOM_TEXT__ = "__RANDOM_TEXT__"
    __STANDARD_BODY__ = "__STANDARD_BODY__"
    __HEADERS_CRLF__ = "\r\n\r\n"

# common token values


standarBody = {
    "cl-body": {
        "value": "buzzshock",
        "headers": "Content-Length: 9",
    },
}

# used in httpRequestPrototype
class GadgetTokens:
    __SHOCKER__ = "__SHOCKER__"
    __SP__ = "__SP__"
    __CRLF__ = "__CRLF__"
    
MandatoryGadgetTokens = ["__SHOCKER__", "__SP__", "__CRLF__"]
DefaultGadgets = {
    "__SHOCKER__" :  "",
    "__SP__"      :  " ",
    "__CRLF__"    :  "\r\n",
}
