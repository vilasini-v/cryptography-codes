'''
caesar cipher: shifts the character by key
'''
import socket
s=socket.socket()

port=12345

s.connect(('127.0.0.1', port))
msg=s.recv(1024).decode()
msg=msg.split(' ')
dec=''
text=msg[0]
key=int(msg[1])

for i in text:
    dec += chr((ord(i) - key - 65) % 26 + 65)

while True:
    print("message received: ", msg)
    print("decrypted: ",dec)
    s.close()
    break