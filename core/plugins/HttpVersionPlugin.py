from core.types.httpRequestPrototype import HttpRequestPrototype


class HttpVersionPlugin:

    def __init__(self, endpoint: str = "", gadget_dict: dict = None, verbose: bool = False) -> None:
        """
            Fuzzing for the Grammar

            HTTP-version  = HTTP-name "/" DIGIT "." DIGIT
            HTTP-name     = %x48.54.54.50 ; "HTTP", case-sensitive

        """
        self.url = endpoint
        self.host, self.port, self.netloc, self.uri = self.urlParser(endpoint)
        self.gadget_dict: dict[str, str] = gadget_dict
        self.mutants_list: dict[str, HttpRequestPrototype] = {}
        self.verbose = verbose

    def generate(self) -> "dict[str , HttpRequestPrototype]":
        self.__normal_req()
        self.__ambigious_versions()
        self.__ambigious_names()

        return self.mutants_list

    def httpTemplate(self, tecl_name: str = None, tecl_value: str = None,
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
        if tecl_name and tecl_name:
            mutant.addHeader(tecl_name, tecl_value)

        mutant.body = http_body
        return mutant

    def __normal_req(self):
        self.mutants_list["vn-vv"] = self.httpTemplate()
        self.mutants_list["vvn-vv"] = self.httpTemplate(
            http_name="%x48.54.54.50")

    def __ambigious_versions(self):
        """
        Naming Convention used
        ---------------------
            vn = valid http name
            vv = valid http version
            i = invalid
        """

        #  Transfer-Encoding Field Supported only in http/1.1 and after testing it in 0.9 and 1.0

        self.mutants_list["vn-vv-0.9"] = self.httpTemplate(
            http_version="0.9",
            tecl_name="Transfer-Encoding",
            tecl_value="chunked",
            mutation_type="vn-vv-0.9",
            add_content_length=False)

        self.mutants_list["vn-vv-1.0"] = self.httpTemplate(
            http_version="1.0",
            tecl_name="Transfer-Encoding",
            tecl_value="chunked",
            mutation_type="vn-vv-1.0",
            add_content_length=False)

        # Invalid Version type
        invalid_versions = ["0.8", "1.2", "1.10", "1.10000000", "1.100000000",
                            "1.01", "1.00000001", "1.000000001", "1.1010", "1.0101", "01.1",
                            "01.10", "01.01" , "1.1.0" , "1.0.0","1.0.1" , "1.1.1"]

        for version in invalid_versions:
            self.mutants_list[f"vn-ivv-{version}"] = self.httpTemplate(
                http_version=version,
                tecl_name="Transfer-Encoding",
                tecl_value="chunked",
                mutation_type=f"vn-ivv-{version}",
                add_content_length=False)

    def __ambigious_names(self):

        self.mutants_list["ivn-vv-Http"] = self.httpTemplate(
            http_name="Http",
            tecl_name="Transfer-Encoding",
            tecl_value="chunked",
            mutation_type="ivn-vv-Http",
            add_content_length=False)

        self.mutants_list["ivn-vv-http"] = self.httpTemplate(
            http_name="http",
            tecl_name="Transfer-Encoding",
            tecl_value="chunked",
            mutation_type="ivn-vv-http",
            add_content_length=False)
