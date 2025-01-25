import socket
import random
s=socket.socket()
port=12345
s.bind(('',port))
s.listen(5)
key = random.randint(1,25)
message="VILASINI"
enc=''
for i in message:
    enc+=chr((ord(i)+key - 65)%26 + 65)
print(enc)
l=enc+' '+str(key)
while True:
    c,addr = s.accept()
    print ('Got connection from', addr )
    
    c.send(l.encode()) 
    s.close()
    break

