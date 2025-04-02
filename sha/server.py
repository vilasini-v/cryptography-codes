import socket
import algorithm
import data 

server = socket.socket()
server.bind(("0.0.0.0", 12345))
server.listen(1)
print("Server listening on port 12345...")

conn, addr = server.accept()
print(f"Connection from {addr}")

msg = conn.recv(1024).decode()
if msg:
    k1, k2, k3, k4, h0, h1, h2, h3, h4 = data.constants()
    md5_hash = algorithm.sha(msg, k1, k2, k3, k4, h0, h1, h2, h3, h4)
    print(f"Received: {msg}")
    print(f"SHA Hash: {md5_hash}")

conn.close()
server.close()