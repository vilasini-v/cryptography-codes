import socket
import algorithm
import data

s=socket.socket()
port=12345
s.bind(('',port))
s.listen(5)

while True:
    c,addr = s.accept()
    print ('Got connection from', addr )
    
    g, k, p, q, h, x = data.server_data()
    print("g = " , g, "\nk = " , k, "\np = " , p, "\tq = " , q, "\nx = " , x,"\nH(m) = " , h)

    r,s = algorithm.sign(g, k, p, q, h, x)
    l = str(r) + " " + str(s)

    c.send(l.encode()) 
    break
