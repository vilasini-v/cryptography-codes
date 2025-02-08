'''
Encryption: 
C = M**e mod n
'''
import socket
s=socket.socket()
port = 12345
s.bind(('', port))
s.listen(5)

def encrypt(m, e, n):
    c = m**e % n
    return c
while True:
    c, addr = s.accept()
    txt = input('Enter message: ')  
    e = int(input('Enter public exponent (e): ')) 
    n = int(input('Enter the value for n: '))  

    txt = [ord(i) for i in txt]
    encrypted = [hex(encrypt(i, e, n))[2:] for i in txt]
    print('Encrypted message (hex):', ' '.join(encrypted))
    encrypted.append(f"{e} {n}")
    encrypted_message = ' '.join(encrypted)
    c.send(encrypted_message.encode())
    print("Message sent.")
    
    c.close()  
    break
