import socket

def encrypt(key, msg_vector):
    result = [0] * 3
    for i in range(3):
        for j in range(3):
            result[i] = (result[i] + key[i][j] * msg_vector[j]) % 26
    return ''.join(chr(x + 65) for x in result)

s = socket.socket()
port = 12345
s.bind(('', port))
s.listen(5)

key = [[10, 23, 12],
       [21, 10, 22],
       [24, 17, 13]]

message = "GFG"
msg_vector = [ord(char) - 65 for char in message]

while True:
    c, addr = s.accept()
    print('Got connection from', addr)
    encrypted = encrypt(key, msg_vector)
    print("Original message:", message)
    print("Encrypted message:", encrypted)
    c.send(encrypted.encode())
    c.close()
    break