import socket
import functions
import data 

server = socket.socket()
server.bind(("0.0.0.0", 12345))
server.listen(1)
print("Server listening on port 12345...")

conn, addr = server.accept()
print(f"Connection from {addr}")

msg = conn.recv(1024).decode()
if msg:
    a, b, c, d, k, s1, s2, s3, s4 = data.data_f()
    m = data.md5_preprocess(msg)
    md5_hash = functions.md5(a, b, c, d, k, m, s1, s2, s3, s4)
    print(f"Received: {msg}")
    print(f"MD5 Hash: {md5_hash}")

conn.close()
server.close()
