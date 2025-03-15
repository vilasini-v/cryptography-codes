#a, b, c, d are 32 bit buffers - initial vectors
#plain text is 512 bits

#four rounds - f, g, h, i
#in each round, 128 bits of plaintext is processed

#each round has 16 rounds - each round will 15 constants.
#round 1 will use [01 - 16]
#round 2 will use [17 - 32]
#round 3 will use [33 - 48]
#round 4 will use [49 - 64]

#the final a, b, c, d values after 4 rounds will be XOR'd with the initial initial vector

# a = b (+)  (( a (+) function(b,c,d) (+) mi (+) ki)<<<s)

def F(b, c, d): return (b & c) | (~b & d)
def G(b, c, d): return (b & d) | (c & ~d)
def H(b, c, d): return b ^ c ^ d
def I(b, c, d): return c ^ (b | ~d)

def left_rotate(x, s):
    return ((x << s) | (x >> (32 - s))) & 0xFFFFFFFF

def md5_step(a, b, c, d, mi, ki, s, func):
    temp = (a + func(b, c, d) + mi + ki) & 0xFFFFFFFF  
    temp = left_rotate(temp, s)  
    return (b + temp) & 0xFFFFFFFF

def md5(a, b, c, d, k, m, s1, s2, s3, s4):
    for i in range(16):
        a, b, c, d = d, md5_step(a, b, c, d, m[i % 16], k[i], s1[i % 4], F), b, c
    for i in range(16, 32):
        a, b, c, d = d, md5_step(a, b, c, d, m[i % 16], k[i], s2[i % 4], G), b, c
    for i in range(32, 48):
        a, b, c, d = d, md5_step(a, b, c, d, m[i % 16], k[i], s3[i % 4], H), b, c
    for i in range(48, 64):
        a, b, c, d = d, md5_step(a, b, c, d, m[i % 16], k[i], s4[i % 4], I), b, c

    return a, b, c, d  

        
    
    


