
import socket
s=socket.socket()

port=12345

s.connect(('127.0.0.1', port))
msg=s.recv(1024).decode()

text = [int(i) for i in msg[:8]]
key_1 = [int(i) for i in msg[8:-8]]
key_2 = [int(i) for i in msg[-8:]]

ip = [2, 6, 3, 1, 4, 8, 5, 7]
ep = [4, 1, 2, 3, 2, 3, 4, 1]
s0 = [[1,0,3,2],
    [3,2,1,0],
    [0,2,1,3],
    [3,1,3,2]]
s1=  [[0,1,2,3],
    [2,0,1,3],
    [3,0,1,0],
    [2,1,0,3]]
p4= [2,4,3,1]

def initialPermutation(text, ip):
    k1=[]
    for i in ip:
        k1.append(text[i-1])
    print('post ip: ',k1)
    return k1


def inversePermutation(ip, text):
    inv_P = [0]*len(ip) 
    for i in range(len(ip)):
        inv_P[i] = ip.index(i+1)+1
    
    k1=[]
    for i in inv_P:
        k1.append(text[i-1])
    return k1

def dataDecryptionCipher(text, ep, p4, s0, s1, key):
    l=text[:4]
    r=text[4:]
    print('text: ', text)
    postEP=[]
    for i in ep:
        postEP.append(r[i-1])
    print('post ep: ',postEP)
   
    postXOR=[]
    for i in range(len(postEP)):
        postXOR.append(postEP[i]^key[i])
    print('post XOR: ',postXOR)


    l1 = postXOR[:4]
    r1 = postXOR[4:]
    row_l1=[l1[0], l1[3]]
    col_l1=[l1[1], l1[2]]
    row_r1=[r1[0], r1[3]]
    col_r1=[r1[1], r1[2]]
    sbox_combined = sBOX(row_l1, col_l1, s0)[2:4] + sBOX(row_r1, col_r1, s1)[2:4]
    print('sbox: ', sbox_combined)
    
    post_p4=[]
    for i in p4:
        post_p4.append(int(sbox_combined[i-1]))
    print('post p4: ', post_p4)
   
    postXOR=[]
    for i in range(len(l)):
        postXOR.append(l[i]^post_p4[i])
    print('post XOR: ',postXOR)
   
    new = postXOR + r
    
    return new
    
def sBOX(row, col, s):
    row = int(''.join([str(x) for x in row]),2)
    col = int(''.join([str(x) for x in col]),2)
    return bin(s[row][col])+'0'


while True:
    print("message received: ", text)
    print("key 1: ", key_1)
    print("key 2: ", key_2)
    postIP = initialPermutation(text, ip)

    print('----------round 1-----------------')
    
    a = dataDecryptionCipher(postIP,ep, p4,s0, s1, key_2)
    print('after round 1: ', a)

    print('----------round 2-----------------')

    b = dataDecryptionCipher(a[4:]+a[:4],ep, p4,s0, s1, key_1)
    print('after round 2: ', b)

    print('Decrypted message (after inverse permutation): ', inversePermutation(ip, b))
    s.close()
    break