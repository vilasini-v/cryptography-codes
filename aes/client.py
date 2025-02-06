import socket
s=socket.socket()

port=12345

s.connect(('127.0.0.1', port))
msg=s.recv(1024).decode()
print(msg)

while True:
    s.close()
    break