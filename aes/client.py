import data
invMixer, subInv = data.decrypt()

def xor_16byte_lists(list1, list2):
    return [hex(int(hex1, 16) ^ int(hex2, 16))[2:].zfill(2) for hex1, hex2 in zip(list1, list2)]

def subBytes(state, sbox):
    return [hex(sbox[int(byte, 16)])[2:].zfill(2) for byte in state]

def inverse_shift_rows(state):
    matrix = [[state[i + 4 * j] for j in range(4)] for i in range(4)]
    return [
        matrix[0],  # Row 0: No shift
        [matrix[1][(i - 1) % 4] for i in range(4)],  # Row 1: Shift right by 1
        [matrix[2][(i - 2) % 4] for i in range(4)],  # Row 2: Shift right by 2
        [matrix[3][(i - 3) % 4] for i in range(4)]   # Row 3: Shift right by 3
    ]

def galois_multiply(a, b):
    p = 0
    for i in range(8):
        if b & 1:
            p ^= a
        high_bit = a & 0x80
        a <<= 1
        if high_bit:
            a ^= 0x1b
        b >>= 1
    return p & 0xff

def inverse_mix_columns(state):
    inv_matrix = [
        [0x0E, 0x0B, 0x0D, 0x09],
        [0x09, 0x0E, 0x0B, 0x0D],
        [0x0D, 0x09, 0x0E, 0x0B],
        [0x0B, 0x0D, 0x09, 0x0E]
    ]
    
    result = [[0 for _ in range(4)] for _ in range(4)]
    
    for col in range(4):
        for row in range(4):
            result[row][col] = (
                galois_multiply(inv_matrix[row][0], state[0][col]) ^
                galois_multiply(inv_matrix[row][1], state[1][col]) ^
                galois_multiply(inv_matrix[row][2], state[2][col]) ^
                galois_multiply(inv_matrix[row][3], state[3][col])
            )
    
    return result
def to_matrix_hex(flat_state):
    matrix = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            matrix[j][i] = int(flat_state[i][j], 16)
    return matrix

# Decryption function
def decryption(all_keys, ciphertext, sbox, mixer):
    # Round 0: AddRoundKey
    new_state = xor_16byte_lists(all_keys[10], ciphertext)
    print('Round 10 : ', new_state)

    # Rounds 1 to 9
    for i in range(9, 0, -1):
        new_state = subBytes(new_state, sbox)
        #print('subBytes: ', new_state)
        if(i<9):
            new_state = inverse_shift_rows(new_state)
            #print('inv shift rows: ', new_state)
            new_state = [new_state[i][j] for j in range(4) for i in range(4)]
        new_state = xor_16byte_lists(all_keys[i], new_state)
        #print('after xor with key: ', new_state)
        new_state = [new_state[i:i+4] for i in range(0, 16, 4)]
        
        new_state = to_matrix_hex(new_state)
        new_state = inverse_mix_columns(new_state)
        #print('inv mix columns: ', new_state)
        new_state = [hex(new_state[i][j])[2:] for j in range(4) for i in range(4)]  # Flatten the 2D matrix
        print('Round', i, ': ', new_state)

    # Round 10: Final round (no inverse mix columns)
    new_state = subBytes(new_state, sbox)
    #print('subBytes: ', new_state)
    new_state = inverse_shift_rows(new_state)
    #print('inv shift rows: ', new_state)
    new_state = [new_state[i][j] for j in range(4) for i in range(4)]  # Flatten the 2D matrix
    new_state = xor_16byte_lists(all_keys[0], new_state)
    print('Round 0 : ', new_state)
    return new_state

# Example usage
import key_generation
import socket
s=socket.socket()

port=12345

s.connect(('127.0.0.1', port))
msg=s.recv(1024).decode()
encrypted_list = msg.split(' ')
while True:
    print("Message Received: ", ''.join([chr(int(i,16)) for i in encrypted_list]))
    all_keys = key_generation.send_keys()
    decrypted_list = decryption(all_keys, encrypted_list, subInv, invMixer)
    print('Decrypted message: ', ''.join([chr(int(i,16)) for i in decrypted_list]))
    s.close()
    break