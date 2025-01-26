import data
import key_gen
import socket
s=socket.socket()

port=12345

s.connect(('127.0.0.1', port))
msg=s.recv(1024).decode()

text = [int(i) for i in msg[:64]]
k1, ip, ep, p32, sBOXES = data.data()
#generate all keys from key_gen.py
allKEYS = key_gen.generateAllKeys(k1)

def initialPermutation(text, ip):
    k1=[text[i-1] for i in ip]    
    print('post ip: ',k1)
    return k1


def inversePermutation(ip, text):
    inv_P = [0]*len(ip) 
    for i in range(len(ip)):
        inv_P[i] = ip.index(i+1)+1
    
    k1=[text[i-1] for i in inv_P ]
    return k1

def dataDecryptionCipher(text, ep, p32, sBOXES, key):
    # Split input into left and right halves
    l = text[:32]
    r = text[32:]
    
    # Expand right half to 48 bits using expansion permutation
    expanded_r = [r[i-1] for i in ep]
    
    # XOR expanded right half with subkey
    xor_result = [x ^ y for x, y in zip(expanded_r, key)]
    
    # Split XOR result into 8 groups of 6 bits for S-box substitution
    s_box_input = [xor_result[i:i+6] for i in range(0, len(xor_result), 6)]
    
    # Apply S-box substitution
    s_box_output = []
    for i in range(8):
        binary_result = sBOX(s_box_input[i], sBOXES[i])
        s_box_output.extend([int(x) for x in binary_result])
    
    # Permute S-box output
    permuted_output = [s_box_output[i-1] for i in p32]
    
    # XOR permuted output with left half
    new_r = [x ^ y for x, y in zip(permuted_output, l)]
    
    # Return new right half and original right half
    return r+new_r

def sBOX(b, s):
    row = [b[0], b[-1]]
    col = b[1:-1]

    row = int(''.join([str(x) for x in row]), 2)
    col = int(''.join([str(x) for x in col]), 2)

    # Convert to binary and add '0's to the front if the length is less than 4
    binary_result = bin(s[row][col])[2:]
    while len(binary_result) < 4:
        binary_result = '0' + binary_result

    return binary_result

while True:
    print("message received: ", text)
    postIP = initialPermutation(text, ip)
    newString= dataDecryptionCipher(postIP, ep, p32, sBOXES, allKEYS[15]) 
    print('after round 1: ', newString)

    for i in range (1,16):
        newString = dataDecryptionCipher(newString, ep, p32, sBOXES,allKEYS[16-i-1])
        print('after round ', i+1,': ', newString)

    lastString = newString[32:]+newString[:32]
    print('Decrypted message (Inverse Permutation): ', inversePermutation(ip, lastString))

    s.close()
    break