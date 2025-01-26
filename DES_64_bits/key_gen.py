# This file contains the functions to generate the subkeys from the given key
import data
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

    
def generateKey(c, d, pc48):
    k=[]
    KEY = c+d
    for i in pc48:
        k.append(KEY[i-1])
    return k

def generateAllKeys(k1):
    #retrieve data from data.py
    p10, p56, pc48, left_shifts = data.key_data()
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