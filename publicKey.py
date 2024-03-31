'''
Name: Mellanie Martin
Course: CS 427
Date: April 6th, 2024
'''

import random
import ctypes

mathLib = ctypes.CDLL('./mathLib.so')

def readFiles(pTxtFile, cTxtName, keyFile):
    pTxt = open(pTxtFile, "r")
    contents = pTxt.read()
    pTxt.close()

    key = open(keyFile, "r")
    pubKey = key.read().split(" ")
    key.close()
    e = int(pubKey[0])
    g = 2
    p = int(pubKey[2])

    contents = contents.encode()
    binary = int.from_bytes(contents, "big")
    binary = bin(binary).lstrip('0b') # string of binary bits of plain text

    if (excess := len(binary) % 31) != 0: # padding necessary
        binary = binary.ljust(len(binary) + (31 - excess), "0")
    
    encryption(binary, cTxtName, e, g, p)
    
def encryption(binary, cTxtName, e, g, p):
    blocks = int(len(binary)/31)
    begIndex = 0
    endIndex = 31
    cTxt = open(cTxtName, "w")
    for i in range(blocks):
        block = "0" + binary[begIndex:endIndex]

        r = random.randrange(1, p - 1)
        C1 = modExpo(g, r, p)
        calc1 = modExpo(int(block), 1, p)
        calc2 = modExpo(e, r, p)
        C2 = calc1*calc2
        cTxt.write(f"{C1} {C2}\n")

        begIndex += 31
        endIndex += 31
    cTxt.close()


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
        while q % 12 != 5:
            q = random.getrandbits(31)
        p = (2*q) - 1
        if millerRabin(p) == 0:
            continue
        else: return p

# n -> number tested
def millerRabin(n):
    if n % 2 == 0 or n < 2: return 0 # if even or 1, composite

    t = 1
    u = ((n-1)/2**t)
    while u % 2 == 0: # ensures u is odd, but n - 1 = 2^t(u) holds
        t += 1
        u = ((n-1)/2**t)

    u = int(u)
    a = random.randrange(0, n - 1)
    binary = str(bin(u).lstrip('0b')) + "2"
    
    mathLib.millerRabin.restype = ctypes.c_int
    mathLib.millerRabin.argtypes = [ctypes.c_ulonglong, ctypes.c_ulonglong, ctypes.c_ulonglong, ctypes.c_wchar_p]
    for i in range(21):
        primality = mathLib.millerRabin(a, n, u, binary)
    if primality == 1: return 1
    else: return 0

# b -> base, e -> exponent, n -> modulus
def modExpo(b, e, n):
    binary = str(bin(e).lstrip('0b')) + "2"

    mathLib.modExpo.restype = ctypes.c_ulonglong
    mathLib.modExpo.argtypes = [ctypes.c_ulonglong, ctypes.c_ulonglong, ctypes.c_ulonglong, ctypes.c_wchar_p]
    return mathLib.modExpo(b, e, n, binary)