
from urllib.parse import ParseResult, urlparse

from numpy import add
from core.types.httpRequestPrototype import HttpRequestPrototype

# RFC 7230 : https://datatracker.ietf.org/doc/html/rfc7230#section-3.3.3
class HttpLaxClPlugin:
    def __init__(self, endpoint: str = "", gadget_dict: dict = None, verbose: bool = False) -> None:
        """
            Fuzzing for the Lax Content Length Header 
            Content-Length = 1*DIGIT (decimal 0-9)

        """
        self.url = endpoint
        self.host, self.port, self.netloc, self.uri = self.urlParser(endpoint)
        self.gadget_dict: dict[str, str] = gadget_dict
        self.mutants_list: dict[str, HttpRequestPrototype] = {}
        self.verbose = verbose

    def generate(self) -> "dict[str, HttpRequestPrototype]":
        self.__normal_req()
        self.__multiple_cl()
        return self.mutants_list

    def httpTemplate(self, cl_name: str = None, cl_value: str = None,
                     http_body: str = "2\r\nyy\r\n0\r\n\r\n", http_version="1.1",
                     http_name: str = "HTTP", add_content_length: bool = True,
                     mutation_type: str = None) -> HttpRequestPrototype:

        mutant = HttpRequestPrototype(
            gadgets=self.gadget_dict,
            add_default_cl=add_content_length,
            http_version=http_version,
            http_name=http_name
        )

        mutant.addHeader("Host", self.host)
        mutant.addHeader("Connection", "Close")

        if mutation_type:
            mutant.addHeader("X-type", mutation_type)
        if cl_name and cl_name:
            mutant.addHeader(cl_name, cl_value)

        mutant.body = http_body
        return mutant

    def __normal_req(self):
        self.mutants_list["1-cl-normal"] = self.httpTemplate(http_body="aaa",
                                                             mutation_type="1-cl-normal"
                                                             )

    def __multiple_cl(self):
        # 2 cl with same value
        self.mutants_list["2-cl-equal"] = self.httpTemplate(http_body="aaa",
                                                            cl_name="Content-Length", cl_value="3",
                                                            mutation_type="2-cl-equal")

        # 2 cl with different value
        self.mutants_list["2-cl-diff"] = self.httpTemplate(http_body="aaa",
                                                           cl_name="Content-Length", cl_value="2",
                                                           mutation_type="2-cl-diff")

        # 1 cl with hexadecimal
        self.mutants_list["1-cl-hex"] = self.httpTemplate(http_body="aaa",
                                                          cl_name="Content-Length", cl_value="0x3",
                                                          add_content_length=False,
                                                          mutation_type="1-cl-hex",
                                                          )

        # 1 cl with dec and other with hex
        self.mutants_list["1-cl-1-hex"] = self.httpTemplate(http_body="aaa",
                                                            cl_name="Content-Length", cl_value="0x3",
                                                            mutation_type="1-cl-1-hex")

        # adding random prefix and suffix before cl value
        for shocker in range(0x00, 0xff):

            # single content length
            self.mutants_list["cl-value-prefix-%02x" % shocker] = self.httpTemplate(http_body="aaa",
                                                                                    add_content_length=False,
                                                                                    cl_name="Content-Length",
                                                                                    cl_value="%c3" % shocker ,
                                                                                    mutation_type="cl-value-prefix-%02x" % shocker
                                                                                    )

            self.mutants_list["cl-value-suffix-%02x" % shocker] = self.httpTemplate(http_body="aaa",
                                                                                    add_content_length=False,
                                                                                    cl_name="Content-Length",
                                                                                    cl_value="3%c" % shocker,
                                                                                    mutation_type="cl-value-suffix-%02x" % shocker
                                                                                    )
            # double content length with 1 correct and other fuzzed
            self.mutants_list["1-cl-value-prefix-%02x" % shocker] = self.httpTemplate(http_body="aaa",
                                                                                      cl_name="Content-Length",
                                                                                      cl_value="%c3" % shocker,
                                                                                      mutation_type="1-cl-value-prefix-%02x" % shocker
                                                                                      )

            self.mutants_list["1-cl-value-suffix-%02x" % shocker] = self.httpTemplate(http_body="aaa",
                                                                                      cl_name="Content-Length",
                                                                                      cl_value="3%c" % shocker,
                                                                                      mutation_type="1-cl-value-suffix-%02x" % shocker
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
