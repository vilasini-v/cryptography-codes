# This file contains the functions to generate the subkeys from the given key
def left_circular_shift(arr, x):
    if(x==1):
        a = arr[0]
        for i in range(1,len(arr)):
            arr[i-1]=arr[i]
        arr[-1]=a
    elif(x==2):
        a = arr[0]
        b=arr[1]
        for i in range(2,len(arr)):
            arr[i-2]=arr[i]
        arr[-2]=a
        arr[-1]=b
    return arr

def permute_56(k1, p56):
    k=[]
    for i in p56:
        k.append(k1[i-1])
    return k[:28], k[28:]

def generate_key_halves(k2, x):
    l=k2[:28]
    r=k2[28:]
    l=left_circular_shift(l, x)
    r=left_circular_shift(r, x)
    return l,r

p10= [3,5,2,7,4,10,1,9,8,6]
p56=[57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36, 63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]
pc48 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]
left_shifts = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]
    
def generateKey(c, d, pc48):
    k=[]
    KEY = c+d
    for i in pc48:
        k.append(KEY[i-1])
    return k

def generateAllKeys(k1):
    c0,d0 = permute_56(k1, p56)
    print('Key 0: ', c0+d0)
    c=[]
    d=[]
    c.append(c0)
    d.append(d0)

    #the left halves of the keys are in a 2-d array c and the right halves are in d
    for i in range(1,len(left_shifts)+1):
        a,b=generate_key_halves(c[i-1]+d[i-1], left_shifts[i-1])
        print(f'Key {i}: ', a+b)
        c.append(a)
        d.append(b)
    
    allKEYS = []
    for i in range(1,len(c)):
        allKEYS.append(generateKey(c[i], d[i], pc48))
    return allKEYS

#finally all subkeys are generated! 