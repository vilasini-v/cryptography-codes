import socket
s=socket.socket()
port=12345
s.bind(('',port))
s.listen(5)

#message and key
message="VILASINI"
key="CRYPTO"

def generate_key(message, key):
    i=0
    while(len(message)!=len(key)):
        key+=key[i]
        i+=1
    if(len(message)==len(key)):
        return key
    
def encrypt(message, key):
    key=generate_key(message, key)
    en=''
    for i in range(len(message)):
        en+=chr(((ord(message[i])+ord(key[i]) - 2*65)%26) + 65)
    return {en,key}

while True:
    c,addr = s.accept()
    print ('Got connection from', addr )
    en, key=encrypt(message, key)
    en=en+' '+key
    print("original message: ", message)
    c.send(en.encode()) 
    s.close()
    break

