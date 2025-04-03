import socket
import data
import algorithm

s=socket.socket()

port=12345

s.connect(('127.0.0.1', port))
msg=s.recv(1024).decode()
msg=msg.split(' ')

r = int(msg[0])
s=int(msg[1])



while True:

    p, q, h, g, y = data.client_data()

    print("y = ", y)
    print("r = " , r, "\ns = ", s)
    if(algorithm.verify(r, s, p, q, h, g, y)):
        print("VERIFIED SIGNATURE")
    break