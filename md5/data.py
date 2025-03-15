import math

k = [int(2**32 * abs(math.sin(i + 1))) for i in range(64)]

def md5_preprocess(message):
    binary_message = ''.join(format(byte, '08b') for byte in message.encode('utf-8'))
    binary_message += '1'
    while (len(binary_message) + 64) % 512 != 0:
        binary_message += '0'
    original_length = len(message) * 8
    length_bits = format(original_length, '064b')
    binary_message += length_bits
    int_chunks = [int(binary_message[i:i+32], 2) for i in range(0, len(binary_message), 32)]
    return int_chunks

message = "they are deterministic"
m = md5_preprocess(message)

a = int("01234567", 16) 
b = int("89abcdef", 16)  
c = int("fedcba98", 16)  
d = int("76543210", 16) 


s1, s2, s3, s4 = [7, 12, 17, 22], [5, 9, 14, 20], [4, 11, 16, 13], [6, 10, 15, 21]

def data_f():
    return a,b,c,d,k,s1,s2,s3,s4

