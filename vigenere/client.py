'''
vigenere cipher: 
ei = pi + ki mod 26
di = pi-ki mod 26
'''
import socket
s=socket.socket()

port=12345

s.connect(('127.0.0.1', port))
msg=s.recv(1024).decode()
msg= msg.split(' ')
message = msg[1]
key = msg[0]
def decyrpt(msg, key):
    dec=''
    for i in range(len(msg)):
        dec+=chr(((ord(msg[i]) - ord(key[i]) - 26)%26) + 65)
    return dec

while True:
    print("encrypted message received: ", msg)
    dec=decyrpt(message, key)
    print("decrypted message is: ", dec)
    s.close()
    break