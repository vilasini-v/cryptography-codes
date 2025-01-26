import socket

k1=[1, 1, 0, 0, 0, 1, 1, 1, 1, 0]

def left_circular_shift(arr, x):
    if(x==1):
        a = arr[0]
        for i in range(1,len(arr)):
            arr[i-1]=arr[i]
        arr[-1]=a
    elif(x==2):
        a = arr[0]
        b=arr[1]
        for i in range(2,len(arr)):
            arr[i-2]=arr[i]
        arr[-2]=a
        arr[-1]=b
    return arr

def perm_10(k1, p10):
    new_key=[k1[i-1] for i in p10]
    return new_key

def generate_key(k, p8, x):
    l=k[:5]
    r=k[5:]
    l=left_circular_shift(l, x)
    r=left_circular_shift(r, x)
    new_key=l+r
    k1=[]
    for i in p8:
        k1.append(new_key[i-1])
    return l+r, k1


p10= [3,5,2,7,4,10,1,9,8,6]
p8= [6, 3, 7, 4, 8, 5, 10, 9]
new_key = perm_10(k1, p10)
generated_k1, r1_key = generate_key(new_key, p8, 1)
a, r2_key = generate_key(generated_k1, p8, 2)

plaintext = [ 0, 0, 1, 0, 1, 0, 0, 0]
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

postIP = initialPermutation(plaintext, ip)

def inversePermutation(ip, text):
    inv_P = [0]*len(ip) 
    for i in range(len(ip)):
        inv_P[i] = ip.index(i+1)+1
    
    k1=[]
    for i in inv_P:
        k1.append(text[i-1])
    return k1

def dataEncryptionCipher(text, ep, p4, s0, s1, key):
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

s=socket.socket()
port=12345
s.bind(('127.0.0.1',port))
s.listen(5)

while True:
    #create server side socket
    c, addr= s.accept()
    print(f"Connected to:  {addr}")     
    print('key 1 : ',r1_key)
    print('key 2: ',r2_key)
    print('plaintext: ', plaintext)
    print('----------round 1-----------------')
    a = dataEncryptionCipher(postIP,ep, p4,s0, s1, r1_key)
    print('after round 1: ', a)

    print('----------round 2-----------------')
    b = dataEncryptionCipher(a[4:]+a[:4],ep, p4,s0, s1, r2_key)
    print('after round 2: ', b)

    print('Encrypted message (Inverse Permutation): ', inversePermutation(ip, b))

    encrypted=inversePermutation(ip, b)+r1_key+r2_key
    c.send(''.join(list(map(str, encrypted))).encode())
    s.close()
    break

