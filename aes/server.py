import socket
s=socket.socket()
port=12345
s.bind(('',port))
s.listen(5)

#encryption part
import data
plaintext, sbox, mixer, key = data.text()

def xor_16byte_lists(list1, list2):
    xor_result = []
    for hex1, hex2 in zip(list1, list2):
        int1 = int(hex1, 16)
        int2 = int(hex2, 16)
        xor_int = int1 ^ int2
        xor_result.append(hex(xor_int)[2:]) 
    return xor_result

def subBytes(state,sbox):
    state = [int(state[i], 16) for i in range(len(state))]
    for i in range(len(state)):
        state[i] = sbox[state[i]]
    s = [hex(i)[2:].upper() for i in state]
    return s

def shift_rows(state):
    matrix = [state[i:i+4] for i in range(0, len(state), 4)]
    transposed_matrix = [[matrix[j][i] for j in range(4)] for i in range(4)]
    b= transposed_matrix[1][1:]+transposed_matrix[1][:1]
    c= transposed_matrix[2][2:]+transposed_matrix[2][:2]
    d= transposed_matrix[3][3:]+transposed_matrix[3][:3]
    state = [transposed_matrix[0],b,c,d]
    state = [[state[j][i] for j in range(4)] for i in range(4)]
    state = state[0]+state[1]+state[2]+state[3]
    return state

def mix_01(a):
    return int(a,16)

def mix_02(a):
    binary_value = bin(int(a, 16))[2:].zfill(8)  
    msb = int(binary_value[0])
    shifted_value = str(binary_value[1:])+'0'
    if msb==1:
        binary_constant = '00011011'
        res = int(shifted_value,2) ^ int(binary_constant,2)
    else:
        res=int(shifted_value,2)
    return res

def mix_03(a):
    res = mix_01(a) ^ mix_02(a)
    return res    

def mixColumns(state, mixer):
    state = [state[i:i+4] for i in range(0, len(state), 4)]
    mixer = [[mixer[j][i] for j in range(4)] for i in range(4)]
    result = [[0, 0, 0, 0] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            for k in range(4):
                if(mixer[k][j]==1):
                    res = mix_01(state[i][k])
                elif(mixer[k][j]==2):
                    res = mix_02(state[i][k])
                else:
                    res = mix_03(state[i][k])
                result[i][j] ^= res
            result[i][j] = hex(result[i][j])[2:].upper()
    return result[0]+result[1]+result[2]+result[3]

import key_generation

all_keys = key_generation.send_keys()
#finally - the actual rounds:
def encryption(all_keys, plaintext, sbox, mixer):
    #round 0:
    new_state = xor_16byte_lists(all_keys[0], plaintext)
    print('Round 0 : ', new_state)

    #round 1 to to 9

    for i in range(1,10):
        new_state = subBytes(new_state, sbox)
        new_state = shift_rows(new_state)
        new_state = mixColumns(new_state, mixer)
        new_state = xor_16byte_lists(all_keys[i], new_state)
        print('Round',i, ': ', new_state)
    
    new_state = subBytes(new_state, sbox)
    new_state = shift_rows(new_state)
    new_state = xor_16byte_lists(all_keys[10], new_state)
    print('Round 10 : ', new_state)
    return new_state

encrypted_list = encryption(all_keys, plaintext, sbox, mixer)

while True:
    c,addr = s.accept()
    c.send(' '.join(encrypted_list).encode())
    s.close()
    break
