import socket
s=socket.socket()
port = 12345
s.connect(('127.0.0.1', port))
msg = s.recv(1024).decode()
msg = msg.split()



def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)

def get_pq(n):
    m = 0
    l = [0]
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: 
            if gcd(i, n // i) == 1:
                if i > m:
                    m = i
                    l.append([i, n // i])
    return l[-1][0], l[-1][1]
'''
 m = c**d mod n
 d = e^-1 mod phi(n)
'''

def inverse(a, b):
    a1 = 1
    a2 = 0
    a3 = a
    b1 = 0
    b2 = 1
    b3 = b
    while(b3>1):
        q = a3//b3
        t1 , t2, t3 = a1 - q*b1, a2 - q*b2, a3 - q*b3
        a1, a2, a3 = b1, b2, b3
        b1, b2, b3 = t1, t2, t3
    if(b3==0):
        return a3
    if(b3==1 and b1<0):
        return b1+b
    if(b3==1):
        return b1
    return None


def get_privateKey(e, n):
    p, q = get_pq(n)
    phi = (p - 1)*(q - 1)
    d = inverse(e, phi)
    return d

def decrypt(c, d, n):
    m = c**d % n
    return m

while True:
    e, n = map(int, msg[-2:])  
    msg = msg[:-2] 
    print("Message recvd: ", msg)
    d = get_privateKey(e, n) 
    print("Private key (d):", d)
    decrypted_list = [decrypt(int(i, 16), d, n) for i in msg]  
    decrypted_message = ''.join(chr(i) for i in decrypted_list)
    print('Decrypted message:', decrypted_message)

    s.close()
    break
