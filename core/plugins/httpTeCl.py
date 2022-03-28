from urllib.parse import ParseResult, urlparse

from core.types.httpRequestPrototype import HttpRequestPrototype


class HttpTeCl:
    def __init__(self, url, gadget_dict: dict = None) -> None:

        self.url = url
        self.host, self.port, self.netloc, self.uri = self.urlParser(url)
        self.gadget_dict = gadget_dict
        self.mutants_list = {}

    def generate(self) -> None:
        print(self.template("Transfer-Encoding" , "chunked"))

    def template(self, tecl_name: str, tecl_value: str, http_body: str = "0\r\n\r\nX"):

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
