import socket
import random
s=socket.socket()
port=12345
s.bind(('',port))
s.listen(5)

message="VILASINI"

def encrypt_railfence(message):
    encrypted_str = ""
    for i in range(0,len(message), 2):
        encrypted_str+=message[i]
    for i in range(1,len(message), 2):
        encrypted_str+=message[i]
    return encrypted_str
def encrypt_rectangle(message, key):
    key = str(key)  # Ensure key is a string
    while len(message) % len(key) != 0:  # Fix modulus condition
        message += "x"
    
    # Create the matrix row by row
    mat = [[k for k in message[i:i + len(key)]] for i in range(0, len(message), len(key))]
    
    # Sort the key for columnar transposition
    key_lst = sorted(key)
    
    # Initialize ciphertext
    c = ""
    for j in range(len(key)):
        # Find the index of the sorted key in the original key
        i = key.index(key_lst[j])
        # Append the column to the ciphertext
        c += ''.join([row[i] for row in mat])
    
    return c

key = 312

while True:
    c,addr = s.accept()
    print ('Got connection from', addr )
    print('Sending encrypted rectangle cipher: ')
    msg = encrypt_rectangle(message, key)
    print(msg)
    msg = msg + ' ' + str(key)
    c.send(msg.encode()) 
    s.close()
    break

