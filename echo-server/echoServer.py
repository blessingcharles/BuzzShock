from concurrent.futures import ThreadPoolExecutor
import socket
from click import echo


def handle_client(conn : socket.socket):
    recievied_bytes = conn.recv(1000000)
    request = recievied_bytes.decode()

    content_len = len(request)
    # log the request to a file
    response = f"HTTP/1.1 200 OK\r\nContent-Length: {content_len}\r\nConnection: close\r\n\r\n{request}"
    conn.sendall(response.encode())

def run_server(port: int = 5000 , threads : int = 28):
    host = "0.0.0.0"
    with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as s:
        with ThreadPoolExecutor(max_workers=threads) as exec:
            s.bind((host , port))
            s.listen()
            print("[+]Server Started at port : " , port)
            while True:
                conn , addr = s.accept()
                exec.submit(handle_client , conn)

run_server()
