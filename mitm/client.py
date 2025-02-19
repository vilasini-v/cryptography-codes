'''user bob'''
'''select Xa
calaculate Ya = a**Xa mod q
'''
p = 19
g = 10

b = 8

pub = g**b % p

import socket

server_address = ('localhost', 65433)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(server_address)
    s.listen(5)
    
    connection, client_address = s.accept()
    with connection:        
        data = connection.recv(1024).decode()
        key = int(data)**b % p
        print("Key computed for Attacker by Bob: ", key)

        msg4 = pub
        print(f"Sending Bob's public key to Attacker: {msg4}")
        connection.sendall(str(msg4).encode())
