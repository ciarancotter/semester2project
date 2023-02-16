import socket
import json
import sys

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

data = {"HandInfront": False}
json_data = json.dumps(data).encode('utf-8')

print(len(json_data))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        while True:
            print(f"Sent {data}")
            conn.sendall(json_data)