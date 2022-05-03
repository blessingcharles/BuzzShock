from pprint import pprint
from urllib.parse import ParseResult, urlparse
from rich import print

from core.types.httpRequestPrototype import HttpRequestPrototype

"""

    Fuzz For Lax Transfer Encoding Parsing

    [ TeCl Template ] 

    GET / HTTP/1.1
    Host: example.com
    Transfer-Encoding: chunked
    Content-Length: 6
    \r\n
    0\r\n
    \r\n
    X
"""


class HttpTeClPlugin:

    def __init__(self, endpoint: str = "", gadget_dict: dict = None, verbose: bool = False) -> None:
        self.url = endpoint
        self.host, self.port, self.netloc, self.uri = self.urlParser(endpoint)
        self.gadget_dict: dict[str, str] = gadget_dict
        self.mutants_list: dict[str, HttpRequestPrototype] = {}
        self.verbose = verbose

    def generate(self) -> None:

        self.__normal_req()
        # Random shocking characters insertion
        self.__pointMutation()
        self.__doublePointMutation()
        self.__xInsertionPointMutation()

        return self.mutants_list

    def httpTemplate(self, tecl_name: str, tecl_value: str, http_body: str = "2\r\nyy\r\n0\r\n\r\nX",
                     add_content_lenght: bool = True, mutation_type: str = None) -> HttpRequestPrototype:

        mutant = HttpRequestPrototype(
            self.gadget_dict, add_default_cl=add_content_lenght)
        mutant.addHeader("Host", self.host)
        mutant.addHeader("Connection", "Close")
        # mutant.addHeader(
        #     "User-Agent", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0")
        # mutant.addHeader(
        #     "Content-type", "application/x-www-form-urlencoded; charset=UTF-8")


        if mutation_type:
            mutant.addHeader("X-type", mutation_type)
        if tecl_name and tecl_name:
            mutant.addHeader(tecl_name, tecl_value)

        mutant.body = http_body
        return mutant

    def __normal_req(self):
        self.mutants_list["normal-req-cl"] = self.httpTemplate(
            None, None, mutation_type="normal-req-cl")
        self.mutants_list["normal-req-te"] = self.httpTemplate(
            "Transfer-Encoding", "chunked",
            add_content_lenght=False,
            http_body="2\r\naa\r\n0\r\n\r\n",
            mutation_type="normal-req-te"
        )
        self.mutants_list["te-and-cl"] = self.httpTemplate(
            "Transfer-Encoding" , "chunked" ,
            mutation_type="te-and-cl"
        )
        
    def __pointMutation(self):
        # Random shocking characters insertion
        for shockers in range(0x1, 0xFF):
            # single mutations
            self.mutants_list["point-key-start-%02x" % shockers] = self.httpTemplate(
                "%cTransfer-Encoding" % shockers, "chunked",
                mutation_type="point-key-start-%02x" % shockers)

            self.mutants_list["point-key-end-%02x" % shockers] = self.httpTemplate(
                "Transfer-Encoding%c" % shockers, "chunked",
                mutation_type="point-key-end-%02x" % shockers)

            self.mutants_list["point-value-start-%02x" % shockers] = self.httpTemplate(
                "Transfer-Encoding", "%cchunked" % shockers,
                mutation_type="point-value-start-%02x" % shockers)

            self.mutants_list["point-value-end-%02x" % shockers] = self.httpTemplate(
                "Transfer-Encoding", "chunked%c" % shockers,
                mutation_type="point-value-end-%02x" % shockers)

    def __doublePointMutation(self):

        for shockers in range(0x1, 0xFF):

            self.mutants_list["double-start-start-%02x" % shockers] = self.httpTemplate(
                "%cTransfer-Encoding" % shockers, "%cchunked" % shockers , 
                mutation_type="double-start-start-%02x" % shockers)

            self.mutants_list["double-end-end-%02x" % shockers] = self.httpTemplate(
                "Transfer-Encoding%c" % shockers, "chunked%c" % shockers ,
                mutation_type="double-end-end-%02x" % shockers
            )

            self.mutants_list["double-start-end-%02x" % shockers] = self.httpTemplate(
                "%cTransfer-Encoding" % shockers, "chunked%c" % shockers , 
                mutation_type="double-start-end-%02x" % shockers)

            self.mutants_list["double-end-start-%02x" % shockers] = self.httpTemplate(
                "%cTransfer-Encoding" % shockers, "%cchunked" % shockers ,
                mutation_type="double-end-start-%02x"
            )

    def __xInsertionPointMutation(self):

        # X header insertion
        for shockers in range(0x1, 0xFF):
            self.mutants_list["X-preheaders-end-%c" % shockers] = self.httpTemplate(
                "X: X%cTransfer-Encoding" % shockers, "chunked" , 
                mutation_type="X-preheaders-end-%c" % shockers
            )

            self.mutants_list["X-preheaders-start-%c-end-%c" % (shockers, shockers)] = self.httpTemplate(
                "X:%cX%cTransfer-Encoding" % (shockers, shockers), "chunked" ,
                mutation_type="X-preheaders-start-%c-end-%c" % (shockers, shockers)
            )

            self.mutants_list["X-preheaders-after-colon-with-%c" % shockers] = self.httpTemplate(
                "X:%cTransfer-Encoding" % shockers, "chunked" ,
                mutation_type="X-preheaders-after-colon-with-%c" % shockers
            )

            self.mutants_list["X-preheaders-end-cr-%c" % shockers] = self.httpTemplate(
                "X: X\r%cTransfer-Encoding" % shockers, "chunked" ,
                mutation_type="X-preheaders-end-cr-%c" % shockers
            )

            self.mutants_list["X-preheaders-end-lf-%c" % shockers] = self.httpTemplate(
                "X: X\n%cTransfer-Encoding" % shockers, "chunked" ,
                mutation_type="X-preheaders-end-lf-%c" % shockers
            )

            self.mutants_list["X-preheaders-%c-end-lf" % shockers] = self.httpTemplate(
                "X: X%c\nTransfer-Encoding" % shockers, "chunked" ,
                mutation_type="X-preheaders-%c-end-lf" % shockers
            )

            self.mutants_list["X-preheaders-%c-end-lf" % shockers] = self.httpTemplate(
                "X: X%c\rTransfer-Encoding" % shockers, "chunked" ,
                mutation_type="X-preheaders-%c-end-lf" % shockers
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

    def generateRequestToFile(self, filename: str):
        with open(filename, "w") as f:
            for key, value in self.mutants_list.items():
                obj = f"\n\n------------{key}-------------------\n{value}"
                f.write(obj)
