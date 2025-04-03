import random as rand

def mod_inverse(k, q):
    def extended_gcd(a, b):
        if b == 0:
            return a, 1, 0
        gcd, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return gcd, x, y
    
    gcd, x, _ = extended_gcd(k, q)
    if gcd != 1:
        return 0
    return x % q

def sign(g, k, p, q, h, x):
    r = (g**k) % p % q
    while r==0:
        k = rand.randint(1, q-1)
        r = (g**k) % p % q

    k_inv = mod_inverse(k, q)
    s = k_inv*(h + (x*r))%q
    while s==0:
        k = rand.randint(1, q-1)
        r = (g**k) % p % q
        while r==0:
            k = rand.randint(1, q-1)
            r = (g**k) % p % q
        s = k_inv*(h + (x*r))%q
    print("Calculated: r = ", r, "\ts = ", s)
    return r,s

def verify(r, s, p, q, h, g, y):
    w = mod_inverse(s, q)
    u1 = h*w % q
    u2 = r*w % q
    v = (g**u1 * y**u2) % p % q 
    print("CALCULATED-------------")
    print("v = ", v)
    print("r = ", r)

    return v==r


    
    

