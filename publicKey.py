'''
Name: Mellanie Martin
Course: CS 427
Date: April 6th, 2024
'''

import random
import ctypes
import base64

mathLib = ctypes.CDLL('./mathLib.so')

def readFilesEnc(pTxtFile, cTxtName, keyFile):
    pTxt = open(pTxtFile, "r")
    contents = pTxt.read()
    pTxt.close()

    key = open(keyFile, "r")
    pubKey = key.read().split(" ")
    key.close()
    e = int(pubKey[0])
    g = 2
    p = int(pubKey[2])
    print(f"Public key: {e} {g} {p}")

    contents = contents.encode()
    binary = int.from_bytes(contents, "big")
    binary = bin(binary).lstrip('0b') # string of binary bits of plain text

    if (excess := len(binary) % 31) != 0: # padding necessary
        binary = binary.rjust(len(binary) + (31 - excess), "0") 
    
    encryption(binary, cTxtName, e, g, p)
    
def encryption(binary, cTxtName, e, g, p):
    blocks = int(len(binary)/31)
    begIndex = 0
    endIndex = 31
    cTxt = open(cTxtName, "w")
    for i in range(blocks):
        block = "0" + binary[begIndex:endIndex] # high bit set to 0
        print(f"Block: {block}\nBits in block: {len(block)}\nint rep of block: {int(block, 2)}")

        r = random.randrange(1, p - 1)
        C1 = modExpo(g, r, p)
        calc1 = int(block, 2) % p
        calc2 = modExpo(e, r, p)
        C2 = calc1*calc2
        print(f"r: {r}\ncalc1: {calc1}\ncalc2: {calc2}\nC1: {C1}\nC2: {C2}")
        cTxt.write(f"{C1} {C2}\n")

        begIndex += 31
        endIndex += 31
    cTxt.close()

def readFilesDec(cTxtFile, pTxtName, keyFile):
    cTxt = open(cTxtFile, "r")
    contents = cTxt.read().split("\n")
    contents = contents[:-1]
    cTxt.close()

    key = open(keyFile, "r")
    priKey = key.read().split(" ")
    key.close()
    d = int(priKey[0])
    p = int(priKey[1])
    print(f"d: {d}\np: {p}")
    
    decryption(contents, pTxtName, d, p)

def decryption(contents, pTxtName, d, p):
    print("\nDecrypted Text:")
    pTxt = open(pTxtName, "w")
    for item in contents:
        blocks = item.split(" ")
        C1 = int(blocks[0])
        C2 = int(blocks[1])
        e = p - 1 - d
        print(f"BEFORE DECRYPTION: C1: {C1}, C2: {C2}, e: {e}")
        C2 = modExpo(C2, 1, p)
        C1 = modExpo(C1, e, p)
        P = C2*C1
        print(f"AFTER DECRYPTION: C1: {C1}, C2: {C2}, P: {P}")
        binary = int(bin(P).lstrip('0b'))
        print(binary)
        #pTxt.write(P)
        #print(P)
    pTxt.close()


def keyGeneration():
    g = 2
    p = primeGeneration()
    d = random.randrange(1, p - 1)
    e = modExpo(2, d, p)
    print(f"PUBLIC KEY: {e} {g} {p}")
    print(f"PRIVATE KEY: {d} {p}")
    pub = open("pubkey.txt", "w")
    priv = open("prikey.txt", "w")
    pub.write(f"{e} {g} {p}")
    priv.write(f"{d} {p}")
    pub.close()
    priv.close()

def primeGeneration():
    while (1):
        q = random.getrandbits(31) # q should be k - 1 bits, where p is k bits
        while q % 12 != 5: q = random.getrandbits(31)
        p = (2*q) + 1
        if millerRabin(p) == 0 or len(bin(p).lstrip('0b')) != 32:
            continue
        else:
            return p

# n -> number tested
def millerRabin(n):
    if n % 2 == 0 or n < 2: return 0 # if even or 1, composite

    t = 1
    u = ((n-1)/2**t)
    while u % 2 == 0: # ensures u is odd, but n - 1 = 2^t(u) holds
        t += 1
        u = ((n-1)/2**t)

    u = int(u)
    binary = str(bin(u).lstrip('0b')) + "2"
    
    mathLib.millerRabin.restype = ctypes.c_int
    mathLib.millerRabin.argtypes = [ctypes.c_ulonglong, ctypes.c_ulonglong, ctypes.c_ulonglong, ctypes.c_int, ctypes.c_wchar_p]
    for i in range(1):
        a = random.randrange(1, n - 1)
        primality = mathLib.millerRabin(a, n, u, t, binary)
        print(f"primality: {primality}")
        if primality == 0: return 0
    return 1

# b -> base, e -> exponent, n -> modulus
def modExpo(b, e, n):
    binary = str(bin(e).lstrip('0b')) + "2"

    mathLib.modExpo.restype = ctypes.c_ulonglong
    mathLib.modExpo.argtypes = [ctypes.c_ulonglong, ctypes.c_ulonglong, ctypes.c_ulonglong, ctypes.c_wchar_p]
    val = mathLib.modExpo(b, e, n, binary)
    return val