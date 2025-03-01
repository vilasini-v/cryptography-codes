'''attacker'''
p = 19
g = 10

import time

c = 4
d = 12

pua = g**c % p
pub = g**d % p

import socket

server_address = ('localhost', 65432)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(server_address)
    s.listen(5)    
    connection, client_address = s.accept()
    with connection:        
        data = connection.recv(1024).decode()
        data = int(data)
        key = data**c % p
        print("Key computed for Alice: ", key)
        

        print(f"Sending public key by attacker to Alice: {pua}")
        connection.sendall(str(pua).encode())
        
        time.sleep(5)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c_socket:
            c_socket.connect(('localhost', 65433))
            print(f"Sending public key by attacker to Bob: {pub}")
            c_socket.sendall(str(pub).encode())
            
            data = c_socket.recv(1024).decode()
            key = int(data)**d %p
            print(f"Computing shared key with Bob: {key}")
