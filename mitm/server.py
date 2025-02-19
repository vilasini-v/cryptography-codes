'''user alice'''
p = 19
g = 10
#random value
a = 7
pua = g**a % p

import socket

server_address = ('localhost', 65432)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(server_address)
    msg1 = pua
    print(f"Sending public key to attacker: {msg1}")
    s.send(str(pua).encode())
    
    data = s.recv(1024).decode()
    key = int(data)**a % p
    print(f"Key computed with attacker: {key}")
