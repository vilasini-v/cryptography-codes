'''
The message digest is computed using the final padded message. The computation uses two buffers, each consisting of five 32-bit words, and a sequence of eighty 32-bit words. The words of the first 5-word buffer are labeled A,B,C,D,E. The words of the second 5-word buffer are labeled H0, H1, H2, H3, H4. The words of the 80-word sequence are labeled W0, W1,..., W79. A single word buffer TEMP is also employed.

To generate the message digest, the 16-word blocks M1, M2,..., Mn defined in Section 4 are processed in order. The processing of each Mi involves 80 steps.

Before processing any blocks, the {Hi} are initialized as follows: in hex,

    H0 = 67452301

    H1 = EFCDAB89

    H2 = 98BADCFE

    H3 = 10325476

    H4 = C3D2E1F0. 


Now M1, M2, ... , Mn are processed. To process Mi, we proceed as follows:

    a. Divide Mi into 16 words W0, W1, ... , W15, where W0 is the left-most word.

    b. For t = 16 to 79 let Wt = S1(Wt-3 XOR Wt-8 XOR Wt- 14 XOR Wt-16).

    c. Let A = H0, B = H1, C = H2, D = H3, E = H4.

    d. For t = 0 to 79 do

        TEMP = S5(A) + ft(B,C,D) + E + Wt + Kt;

        E = D; D = C; C = S30(B); B = A; A = TEMP; 


    e. Let H0 = H0 + A, H1 = H1 + B, H2 = H2 + C, H3 = H3 + D, H4 = H4 + E. 


After processing Mn, the message digest is the 160-bit string represented by the 5 words

    H0 H1 H2 H3 H4. 

'''


def f0(b,c,d):
    return (b&c)|(~b & d)
def f1(b,c,d):
    return b^c^d
def f2(b,c,d):
    return (b&c) | (b&d) | (c&d)
def f3(b,c,d):
    return b^c^d

def sha_preprocess(message):
    binary_message = ''.join(format(byte, '08b') for byte in message.encode('utf-8'))
    binary_message += '1'
   
    while (len(binary_message) + 64) % 512 != 0:
        binary_message += '0'
   
    original_length = len(message) * 8
    length_bits = format(original_length, '064b')
    binary_message += length_bits
    words = [int(binary_message[i:i+32], 2) for i in range(0, len(binary_message), 32)]
    return words

def sha(m, k1, k2, k3, k4, h0, h1, h2, h3, h4):
    words = sha_preprocess(m)
    
    for j in range(0, len(words), 16):
        block = words[j:j+16]
        w = block.copy()
        
        for t in range(16, 80):
            w.append(((w[t-3] ^ w[t-8] ^ w[t-14] ^ w[t-16]) << 1 | 
                      (w[t-3] ^ w[t-8] ^ w[t-14] ^ w[t-16]) >> 31) & 0xFFFFFFFF)
        
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        
        for t in range(80):
            if t < 20:
                f = f0(b,c,d)
                k = k1
            elif t < 40:
                f = f1(b,c,d)
                k = k2
            elif t < 60:
                f = f2(b,c,d)
                k = k3
            else:
                f = f3(b,c,d)
                k = k4
            
            temp = ((a << 5) | (a >> 27)) & 0xFFFFFFFF
            temp = (temp + f + e + w[t] + k) & 0xFFFFFFFF
            
            e = d
            d = c
            c = ((b << 30) | (b >> 2)) & 0xFFFFFFFF
            b = a
            a = temp
        
        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF
    
    return ''.join(f'{h:08x}' for h in [h0, h1, h2, h3, h4])
