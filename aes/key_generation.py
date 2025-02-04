import data

sbox, sboxInv, key, constants = data.keys()
def cls(word):
    return word[1:] + word[:1]

def round_constant(constant, word):
    res_lst = []
    for c_byte, w_byte in zip(constant, word):
        result_byte = int(c_byte,16) ^ int(w_byte, 16)
        result_byte = result_byte % 256
        res_lst.append(hex(result_byte)[2:].zfill(2))
    return res_lst

def subBytes(state):
    for i in range(len(state)):
        state[i] = sbox[state[i]]
    return state

def subBytesInv(state):
    for i in range(len(state)):
        state[i] = sboxInv[state[i]]
    return state

def key_functions(key, constant):
    key = cls(key)
    state = [int(key[i], 16) for i in range(len(key))]
    s=subBytes(state)
    sub = [hex(i)[2:] for i in s]
    w = round_constant(constant, sub)
    return w

def xor_hex_lists(list1, list2):
    xor_result = []
    for hex1, hex2 in zip(list1, list2):
        int1 = int(hex1, 16)
        int2 = int(hex2, 16)
        xor_int = int1 ^ int2
        xor_result.append(hex(xor_int)[2:]) 
    return xor_result

def key_gen(key, constant):
    w= []
    g = key_functions(key[12:], constant)
    w+= xor_hex_lists(g, key[:4])
    w+= xor_hex_lists(w[:4], key[4:8])
    w+= xor_hex_lists(w[4:8], key[8:12])
    w+= xor_hex_lists(w[8:12], key[12:])
    return w

all_keys = []
def key_rounds(key, constant):
    for i in range(10):
        key = key_gen(key, [constant[i],'00', '00', '00'])
        print(key)
        all_keys.append(key)
key_rounds(key, constants)

def send_keys():
    return all_keys