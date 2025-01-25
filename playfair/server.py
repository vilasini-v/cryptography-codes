'''
playfair cipher
'''


import socket
s=socket.socket()
port=12345
s.bind(('',port))
s.listen(5)
# #message and key
message="balloon"
key="monarchy"


al=[chr(ord('a')+i) for i in range(26)]
al.remove('j')

#genrate key matrix
def generate_matrix(key):
   key= key + "".join(al)
   key= "".join(dict.fromkeys(key))
   mat=[[k for k in key[i:i+5]] for i in range(0,25,5)]
   return mat
mat = generate_matrix(key)

#convert plaintext to pairs of diagrams
diagrams =[]
def plaintext_diagrams(message):
   l=[]
   for i in range(0, len(message),2):
       l.append(message[i])
       if(message[i+1]==message[i]):
           msg = [i for i  in message]
           msg.insert(i+1, 'x')
           message = "".join(msg)
       l.append(message[i+1])
       diagrams.append(l)
       l=[]


plaintext_diagrams(message)


#replace plaintext wrt to key matrix
new_list = []
def find_pos(diagrams, mat):
   for i in diagrams:
       p=[]
       for j in i:
           for col, row in enumerate(mat):
               if j in row:
                   rowth = row.index(j)  # Column index
                   p.append([col,rowth])
                   break
       new_list.append(p)


find_pos(diagrams, mat)


def row_equal(row):
   l=[]
   l.append(mat[row[0][0]][(row[0][1]+1)%5])
   l.append(mat[row[1][0]][(row[1][1]+1)%5])
   return l
def col_equal(col):
   l=[]
   l.append(mat[(col[0][0]+1)%5][col[0][1]])
   l.append(mat[(col[1][0]+1)%5][col[1][1]])
   return l

def not_same(elem):
    l=[]
    l.append(mat[elem[0][0]][elem[1][1]])
    l.append(mat[elem[1][0]][elem[0][1]])
    return l


encrypted_list=[]
def encrypt(position):
    for j in position:
        if(j[0][0]==j[1][0]):
            encrypted_list.append("".join(row_equal(j)))
        elif(j[0][1]==j[1][1]):
            encrypted_list.append("".join(col_equal(j)))
        else:
            encrypted_list.append("".join(not_same(j)))  
    return "".join(encrypted_list)

while True:
    c,addr = s.accept()
    print ('Got connection from', addr )
    en=encrypt(new_list)
    eng=en+' '+key
    print("original message: ", message)
    print("encrypted message: ", en)
    c.send(eng.encode())
    s.close()
    break
