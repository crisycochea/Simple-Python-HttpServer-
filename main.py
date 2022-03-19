# echo-server.py

import socket
from datetime import datetime
from email.utils import formatdate
from time import mktime
from typing import List

HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind((HOST, PORT))
    s.listen()
    print(f"Listening on {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            data = conn.recv(1024)
            if not data:
                conn.close()
                break
            request = data.decode('utf-8')
            request_info, *headers, _, request_body = request.splitlines()
            headers = dict(line.split(':', maxsplit=1) for line in headers)
            verb, route, version = request_info.split(' ')
            status_code = 400 if route == "/error" else 200
            
            body = f"""
            <ul>
            <li>Route: {route}</li>
            <li>Verb: {verb}</li>
            <li>Version: {version}</li>
            <li>headers: {headers}</li>
            <li>body: {request_body}</li>
            </ul>
            """
            response = f"""HTTP/1.0 {status_code} OK
Server: Custom Python Server
Content-Length: {len(body)}
Content-Type: text/html

{body}
"""
            conn.sendall(response.encode('utf-8'))
            conn.close()
