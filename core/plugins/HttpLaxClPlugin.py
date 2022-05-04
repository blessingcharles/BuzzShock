

from urllib.parse import ParseResult, urlparse
from core.types.httpRequestPrototype import HttpRequestPrototype


class HttpLaxClPlugin:
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