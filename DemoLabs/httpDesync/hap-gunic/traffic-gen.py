from time import sleep
from rich import print
from conn import BytesIOSocket , ShockerSocket

def normal_user(payload , host , port):
    s = ShockerSocket(host , port)
    s.plug()
    s.send(payload)
    result = s.recv()
    return BytesIOSocket.response_from_bytes(result)
  

"""
printf 'GET / HTTP/1.1\r\n'\
'Host: 127.0.0.1:8081\r\n'\
'Connection: close\r\n'\
'\r\n'
"""

normal_payload = b"GET / HTTP/1.1\r\nHost: 127.0.0.1:8081\r\nConnection: close\r\n\r\n"

while True:
    resp_obj = normal_user(normal_payload , "127.0.0.1" ,8081)

    if resp_obj.status == 200:
        print("[bold green][+] Response Success[/bold green]")
    else:
        print("[bold Red][-] Attacker Modified the Request[/bold red]")
        print("[bold yellow]Headers[/bold yellow]\n" , resp_obj.getheaders())
        print("[bold yellow]Data[/bold yellow]\n" , resp_obj.data)

    sleep(1)

