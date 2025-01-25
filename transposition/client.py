'''
transposition cipher: railfence and rectangle
'''
import socket
s=socket.socket()

port=12345

s.connect(('127.0.0.1', port))
msg=s.recv(1024).decode()
msg=msg.split(' ')
dec=''
text=msg[0]
key=msg[1]

def decrypt_railfence(message):
    decrypted_str = ""
    for i in range(0,len(message)//2):
        decrypted_str+=message[i]
        decrypted_str+=message[i + len(message)//2]
    return decrypted_str

def decrypt_rectangle(ciphertext, key):
    key = str(key)
    num_cols = len(key)
    num_rows = len(ciphertext) // num_cols
    sorted_key = sorted(list(map(int, key)))
    mat = [["" for _ in range(num_cols)] for _ in range(num_rows)]
    index = 0
    for num in sorted_key:
        col = key.index(str(num))
        for row in range(num_rows):
            mat[row][col] = ciphertext[index]
            index += 1
    
    message = ''.join([''.join(row) for row in mat])
    message = message.rstrip("x")
    return message

while True:
    print("message received: ", text)
    print("decrypted: ", decrypt_rectangle(text, key))
    s.close()
    break