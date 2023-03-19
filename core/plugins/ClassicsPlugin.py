
from urllib.parse import ParseResult, urlparse

from core.types.httpRequestPrototype import HttpRequestPrototype

class ClassicsPlugin:
    def __init__(self, endpoint: str = "", gadget_dict: dict = None, verbose: bool = False) -> None:
        """

        """
        self.url = endpoint
        self.host, self.port, self.netloc, self.uri = self.urlParser(endpoint)
        self.gadget_dict: dict[str, str] = gadget_dict
        self.mutants_list: dict[str, HttpRequestPrototype] = {}
        self.verbose = verbose

    def generate(self) -> "dict[str, HttpRequestPrototype]":
        self.__classics_req()
        return self.mutants_list

    def httpTemplate(self, te_name: str = None, te_value: str = None,
                     cl_name: str = None , cl_value: int = None ,
                     http_body: str = "1\r\nA", http_version="1.1",
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
        
        if te_name and te_value:
            mutant.addHeader(te_name, te_value)
        if cl_name and cl_value:
            mutant.addHeader(cl_name , cl_value)

        mutant.body = http_body
        return mutant

    def __classics_req(self):


        self.mutants_list["classics-clte"] = self.httpTemplate(te_name="Transfer-Encoding" ,
                                                               te_value="chunked" ,
                                                               mutation_type="classics-clte")
        self.mutants_list["classics-tecl"] = self.httpTemplate(te_name="Transfer-Encoding" , 
                                                               te_value="chunked" ,
                                                               cl_name="Content-Length" ,
                                                               cl_value=6,
                                                               mutation_type="classics-tecl" ,
                                                               http_body="0\r\n\r\n")
        