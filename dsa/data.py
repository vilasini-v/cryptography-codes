p = 293
q = 73
x = 29
h = 53
k = 17
g = 60

y = g**x % p

def server_data():
    return g, k, p, q, h, x

def client_data():
    return p, q, h, g, y
