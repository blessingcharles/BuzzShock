from pprint import pprint
from urllib.parse import ParseResult, urlparse
from rich import print

from core.types.httpRequestPrototype import HttpRequestPrototype


class HttpLaxTePlugin:

    def __init__(self, endpoint: str = "", gadget_dict: dict = None, verbose: bool = False) -> None:
        """
            Fuzz For Lax Transfer Encoding Header Parsing

            Methods
            ---------
            case_collapser
            point
        """

        self.url = endpoint
        self.host, self.port, self.netloc, self.uri = self.urlParser(endpoint)
        self.gadget_dict: dict[str, str] = gadget_dict
        self.mutants_list: dict[str, HttpRequestPrototype] = {}
        self.verbose = verbose

    def generate(self) -> "dict[str, HttpRequestPrototype]":

        self.__normal_req()
        # self.__case_collapser()
        self.__bad_chunksize()

        # # Random shocking characters insertion
        # self.__point_mutation()
        # self.__double_point_mutation()
        # self.__x_insertion_point_mutation()

        return self.mutants_list

    def httpTemplate(self, tecl_name: str = None, tecl_value: str=None, http_body: str = "2\r\nyy\r\n0\r\n\r\nX",
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

    def __case_collapser(self):

        self.mutants_list["key-case-collapse"] = self.httpTemplate(
            "TransFer-EncoDing", "chunked",
            mutation_type="key-case-collapse"
        )

        self.mutants_list["value-case-collapse"] = self.httpTemplate(
            "Transfer-Encoding", "cHunKed",
            mutation_type="value-case-collapse"
        )

        self.mutants_list["key-value-case-collapse"] = self.httpTemplate(
            "TransFer-EncoDing", "cHunKed",
            mutation_type="key-value-case-collapse"
        )

        # without content length header
        self.mutants_list["wcl-key-case-collapse"] = self.httpTemplate(
            "TransFer-EncoDing", "chunked",
            mutation_type="wcl-key-case-collapse",
            http_body="2\r\nyy\r\n0",
            add_content_lenght=False
        )

        self.mutants_list["wcl-value-case-collapse"] = self.httpTemplate(
            "Transfer-Encoding", "cHunKed",
            mutation_type="wclvalue-case-collapse",
            http_body="2\r\nyy\r\n0",
            add_content_lenght=False
        )

        self.mutants_list["wcl-key-value-case-collapse"] = self.httpTemplate(
            "TransFer-EncoDing", "cHunKed",
            mutation_type="wcl-key-value-case-collapse",
            http_body="2\r\nyy\r\n0",
            add_content_lenght=False
        )

    def __bad_chunksize(self):

        bad_chunkprefix = ["0x", "0", ".", "0.", ".0", "+", "-", "*"]

        for shocker in bad_chunkprefix:
            self.mutants_list["bad-chunksize-%s2" % shocker] = self.httpTemplate(
                tecl_name="Transfer-Encoding" ,
                tecl_value="chunked" ,
                mutation_type="bad-chunksize-%s2" % shocker,
                http_body="%s2\r\nyy\r\n0\r\n\r\n" % shocker
            )
        bad_terminatingchunks = ["0" , "00" , "+" , "-" , "0." , ".0"]

        for shocker in bad_terminatingchunks:

            # prefix
            self.mutants_list["bad-terminatingchunk-%s0" % shocker] = self.httpTemplate(
                tecl_name="Transfer-Encoding" ,
                tecl_value="chunked" ,
                mutation_type="bad-terminatingchunk-%s0" % shocker,
                add_content_lenght=False,
                http_body="2\r\nyy\r\n%s0\r\n\r\n" % shocker
            )

            # suffix
            self.mutants_list["bad-terminatingchunk-0%s" % shocker] = self.httpTemplate(
                tecl_name="Transfer-Encoding" ,
                tecl_value="chunked" ,
                mutation_type="bad-terminatingchunk-0%s" % shocker,
                add_content_lenght=False,
                http_body="2\r\nyy\r\n0%s\r\n\r\n" % shocker
            )

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
            "Transfer-Encoding", "chunked",
            mutation_type="te-and-cl"
        )

    def __point_mutation(self):
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

            # without contentlength header
            self.mutants_list["wcl-point-key-start-%02x" % shockers] = self.httpTemplate(
                "%cTransfer-Encoding" % shockers, "chunked",
                mutation_type="wcl-point-key-start-%02x" % shockers,
                http_body="2\r\nyy\r\n0",
                add_content_lenght=False)

            self.mutants_list["wcl-point-key-end-%02x" % shockers] = self.httpTemplate(
                "Transfer-Encoding%c" % shockers, "chunked",
                mutation_type="wcl-point-key-end-%02x" % shockers,
                http_body="2\r\nyy\r\n0",
                add_content_lenght=False)

            self.mutants_list["wcl-point-value-start-%02x" % shockers] = self.httpTemplate(
                "Transfer-Encoding", "%cchunked" % shockers,
                mutation_type="wcl-point-value-start-%02x" % shockers,
                http_body="2\r\nyy\r\n0",
                add_content_lenght=False)

            self.mutants_list["wcl-point-value-end-%02x" % shockers] = self.httpTemplate(
                "Transfer-Encoding", "chunked%c" % shockers,
                mutation_type="wcl-point-value-end-%02x" % shockers,
                http_body="2\r\nyy\r\n0",
                add_content_lenght=False)

    def __double_point_mutation(self):

        for shockers in range(0x1, 0xFF):

            self.mutants_list["double-start-start-%02x" % shockers] = self.httpTemplate(
                "%cTransfer-Encoding" % shockers, "%cchunked" % shockers,
                mutation_type="double-start-start-%02x" % shockers)

            self.mutants_list["double-end-end-%02x" % shockers] = self.httpTemplate(
                "Transfer-Encoding%c" % shockers, "chunked%c" % shockers,
                mutation_type="double-end-end-%02x" % shockers
            )

            self.mutants_list["double-start-end-%02x" % shockers] = self.httpTemplate(
                "%cTransfer-Encoding" % shockers, "chunked%c" % shockers,
                mutation_type="double-start-end-%02x" % shockers)

            self.mutants_list["double-end-start-%02x" % shockers] = self.httpTemplate(
                "%cTransfer-Encoding" % shockers, "%cchunked" % shockers,
                mutation_type="double-end-start-%02x"
            )

            # without content length header

            self.mutants_list["wcl-double-start-start-%02x" % shockers] = self.httpTemplate(
                "%cTransfer-Encoding" % shockers, "%cchunked" % shockers,
                mutation_type="wcl-double-start-start-%02x" % shockers,
                http_body="2\r\nyy\r\n0",
                add_content_lenght=False)

            self.mutants_list["wcl-double-end-end-%02x" % shockers] = self.httpTemplate(
                "Transfer-Encoding%c" % shockers, "chunked%c" % shockers,
                mutation_type="wcl-double-end-end-%02x" % shockers,
                http_body="2\r\nyy\r\n0",
                add_content_lenght=False
            )

            self.mutants_list["wcl-double-start-end-%02x" % shockers] = self.httpTemplate(
                "%cTransfer-Encoding" % shockers, "chunked%c" % shockers,
                mutation_type="wcl-double-start-end-%02x" % shockers,
                http_body="2\r\nyy\r\n0",
                add_content_lenght=False)

            self.mutants_list["wcl-double-end-start-%02x" % shockers] = self.httpTemplate(
                "%cTransfer-Encoding" % shockers, "%cchunked" % shockers,
                mutation_type="wcl-double-end-start-%02x",
                http_body="2\r\nyy\r\n0",
                add_content_lenght=False
            )

    def __x_insertion_point_mutation(self):

        # X header insertion
        for shockers in range(0x1, 0xFF):
            self.mutants_list["X-preheaders-end-%02x" % shockers] = self.httpTemplate(
                "X: X%cTransfer-Encoding" % shockers, "chunked",
                mutation_type="X-preheaders-end-%02x" % shockers
            )

            self.mutants_list["X-preheaders-start-%02x-end-%02x" % (shockers, shockers)] = self.httpTemplate(
                "X:%cX%cTransfer-Encoding" % (shockers, shockers), "chunked",
                mutation_type="X-preheaders-start-%02x-end-%02x" % (
                    shockers, shockers)
            )

            self.mutants_list["X-preheaders-after-colon-with-%02x" % shockers] = self.httpTemplate(
                "X:%cTransfer-Encoding" % shockers, "chunked",
                mutation_type="X-preheaders-after-colon-with-%02x" % shockers
            )

            self.mutants_list["X-preheaders-end-cr-%02x" % shockers] = self.httpTemplate(
                "X: X\r%cTransfer-Encoding" % shockers, "chunked",
                mutation_type="X-preheaders-end-cr-%02x" % shockers
            )

            self.mutants_list["X-preheaders-end-lf-%02x" % shockers] = self.httpTemplate(
                "X: X\n%cTransfer-Encoding" % shockers, "chunked",
                mutation_type="X-preheaders-end-lf-%02x" % shockers
            )

            self.mutants_list["X-preheaders-%02x-end-lf" % shockers] = self.httpTemplate(
                "X: X%c\nTransfer-Encoding" % shockers, "chunked",
                mutation_type="X-preheaders-%02x-end-lf" % shockers
            )

            self.mutants_list["X-preheaders-%02x-end-cr" % shockers] = self.httpTemplate(
                "X: X%c\rTransfer-Encoding" % shockers, "chunked",
                mutation_type="X-preheaders-%02x-end-cr" % shockers
            )

            # without content length

            self.mutants_list["wcl-X-preheaders-end-%02x" % shockers] = self.httpTemplate(
                "X: X%cTransfer-Encoding" % shockers, "chunked",
                mutation_type="wcl-X-preheaders-end-%02x" % shockers,
                http_body="2\r\nyy\r\n0",
                add_content_lenght=False
            )

            self.mutants_list["wcl-X-preheaders-start-%02x-end-%02x" % (shockers, shockers)] = self.httpTemplate(
                "X:%cX%cTransfer-Encoding" % (shockers, shockers), "chunked",
                mutation_type="wcl-X-preheaders-start-%02x-end-%02x" % (
                    shockers, shockers),
                http_body="2\r\nyy\r\n0",
                add_content_lenght=False
            )

            self.mutants_list["wcl-X-preheaders-after-colon-with-%02x" % shockers] = self.httpTemplate(
                "X:%cTransfer-Encoding" % shockers, "chunked",
                mutation_type="wcl-X-preheaders-after-colon-with-%02x" % shockers,
                http_body="2\r\nyy\r\n0",
                add_content_lenght=False
            )

            self.mutants_list["wcl-X-preheaders-end-cr-%02x" % shockers] = self.httpTemplate(
                "X: X\r%cTransfer-Encoding" % shockers, "chunked",
                mutation_type="wcl-X-preheaders-end-cr-%02x" % shockers,
                http_body="2\r\nyy\r\n0",
                add_content_lenght=False
            )

            self.mutants_list["wcl-X-preheaders-end-lf-%02x" % shockers] = self.httpTemplate(
                "X: X\n%cTransfer-Encoding" % shockers, "chunked",
                mutation_type="wcl-X-preheaders-end-lf-%02x" % shockers,
                http_body="2\r\nyy\r\n0",
                add_content_lenght=False
            )

            self.mutants_list["wcl-X-preheaders-%02x-end-lf" % shockers] = self.httpTemplate(
                "X: X%c\nTransfer-Encoding" % shockers, "chunked",
                mutation_type="wcl-X-preheaders-%02x-end-lf" % shockers,
                http_body="2\r\nyy\r\n0",
                add_content_lenght=False
            )

            self.mutants_list["wcl-X-preheaders-%02x-end-cr" % shockers] = self.httpTemplate(
                "X: X%c\rTransfer-Encoding" % shockers, "chunked",
                mutation_type="wcl-X-preheaders-%02x-end-cr" % shockers,
                http_body="2\r\nyy\r\n0",
                add_content_lenght=False
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
