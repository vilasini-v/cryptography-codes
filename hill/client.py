import socket
import math as m

def get_det(mat, n):
    if n == 1:
        return mat[0][0]
    if n == 2:
        return mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]
   
    det = 0
    for col in range(n):
        sub = [[0] * (n - 1) for _ in range(n - 1)]
        for i in range(1, n):
            subcol = 0
            for j in range(n):
                if j == col:
                    continue
                sub[i - 1][subcol] = mat[i][j]
                subcol += 1
        sign = 1 if col % 2 == 0 else -1
        det += sign * mat[0][col] * get_det(sub, n - 1)
    return det

def extended_euclidean(a, b):
    if b == 0:
        return 1, 0
    else:
        x, y = extended_euclidean(b, a % b)
        return y, x - (a // b) * y

def get_modular_multiplicative_inverse(a, m):
    x, y = extended_euclidean(a, m)
    return x % m

def get_cof(mat, cof, p, q, n):
    i = 0
    j = 0
    for row in range(n):
        for col in range(n):
            if row != p and col != q:
                cof[i][j] = mat[row][col]
                j += 1
                if j == n - 1:
                    j = 0
                    i += 1

def adjoint(mat, adj):
    n = len(mat)
    if n == 1:
        adj[0][0] = 1
        return
   
    cof = [[0] * (n-1) for _ in range(n-1)]
    for i in range(n):
        for j in range(n):
            get_cof(mat, cof, i, j, n)
            sign = 1 if (i + j) % 2 == 0 else -1
            adj[j][i] = (sign * get_det(cof, n - 1)) % 26

def k_inverse(key, det_inv):
    n = len(key)
    k_inv = [[0] * n for _ in range(n)]
    adj = [[0] * n for _ in range(n)]
    adjoint(key, adj)
    for i in range(n):
        for j in range(n):
            k_inv[i][j] = (adj[i][j] * det_inv) % 26
    
    return k_inv

def decrypt(k_inv, cipher_text):
    n = len(k_inv)
    c = [ord(char) - ord('A') for char in cipher_text]
    if len(c) != n:
        raise ValueError(f"Cipher text block length must be {n}")
    
    result = [0] * n
    for i in range(n):
        for j in range(n):
            result[i] = (result[i] + k_inv[i][j] * c[j]) % 26
    
    return ''.join(chr(x + ord('A')) for x in result)

s = socket.socket()
port = 12345
key = [[10, 23, 12],
       [21, 10, 22],
       [24, 17, 13]]

try:
    s.connect(('127.0.0.1', port))
    msg = s.recv(1024).decode()
    
    det = get_det(key, len(key)) % 26
    det_inv = get_modular_multiplicative_inverse(det, 26)
    k_inv = k_inverse(key, det_inv)
    
    decrypted = ""
    for i in range(0, len(msg), 3):
        block = msg[i:i+3]
        if len(block) == 3:  
            decrypted += decrypt(k_inv, block)
    
    print("Received encrypted message:", msg)
    print("Decrypted message:", decrypted)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    s.close()