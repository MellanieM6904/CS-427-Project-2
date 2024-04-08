'''
Name: Mellanie Martin
Course: CS 427
Date: April 6th, 2024
'''

import random
import ctypes

mathLib = ctypes.CDLL('./mathLib.so') # Library containing miller rabin and modular exponentiation algorithms

'''
Input: name of the plaintext file, name of the ciphertext file, name of file for keys
Output: N/A
Purpose: Reads in keys and plaintext file. Passes this data to encryption()
'''
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

    contents = contents.encode('ascii')
    binary = int.from_bytes(contents, "big")
    binary = bin(binary).lstrip('0b') # string of binary bits of plain text

    if (excess := len(binary) % 31) != 0: # padding necessary
        binary = binary.ljust(len(binary) + (31 - excess), "0")
    
    encryption(binary, cTxtName, e, g, p)

'''
Input: Binary rep of plaintext file with padding, name of ciphertext file, public key
Output: N/A. Writes to ciphertext file
Purpose: Encrypts plaintext bits into ints C1 and C2, and writes C1 C2 to ciphertext file
'''
def encryption(binary, cTxtName, e, g, p):
    blocks = int(len(binary)/31)
    begIndex = 0
    endIndex = 31
    cTxt = open(cTxtName, "w")
    for i in range(blocks):
        block = binary[begIndex:endIndex]
        r = random.randrange(1, p - 1)
        C1 = modExpo(g, r, p)
        C2 = modExpo(modExpo(e, r, p) * int(block, 2), 1, p)
        cTxt.write(f"{C1} {C2}\n")

        begIndex += 31
        endIndex += 31
    cTxt.close()

'''
Input: Ciphertext file name, plaintext file name, file containing key
Output: N/A
Purpose: Reads in private key and ciphertext
'''
def readFilesDec(cTxtFile, pTxtName, keyFile):
    cTxt = open(cTxtFile, "r")
    contents = cTxt.read().split("\n")
    contents = contents[:-1] # remove final new line
    cTxt.close()

    key = open(keyFile, "r")
    priKey = key.read().split(" ")
    key.close()
    d = int(priKey[0])
    p = int(priKey[1])
    
    decryption(contents, pTxtName, d, p)

'''
Input: Array of strings, each containing a line from ciphertext (C1 C2), plaintext file name, private key
Output: N/A. Writes to plaintext
Purpose: Decrypts C1 C2 of each line to binary, converts the full binary string to ASCII
'''
def decryption(contents, pTxtName, d, p):
    print("\nDecrypted Text:")
    binary = '0' # Ensure high bit is 0
    pTxt = open(pTxtName, "w")
    for item in contents:
        blocks = item.split(" ")
        C1 = int(blocks[0])
        C2 = int(blocks[1])
        e = p - 1 - d
        P = modExpo(modExpo(C1, e, p) * C2, 1, p)
        block = bin(P).lstrip('0b')
        block = block.zfill(31) # ensure every block is 31 bits
        binary += block
    if binary.endswith('0'): binary = binary.rstrip('0') # remove padding
    binary = ' '.join(binary[i:i+8] for i in range(0, len(binary), 8)) # split into octets
    binary = binary.split(" ")
    decrypted = ''.join([chr(int(i, 2)) for i in binary]) # convert octets to ascii
    pTxt.write(decrypted)
    print(decrypted)
    pTxt.close()

'''
Input: N/A
Output: N/A. Writes to key files
Purpose: Generates private and public key
'''
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

'''
Input: N/A
Output: prime modulus, p
Purpose: Generates prime modulus p that is 32 bits and has generator 2
'''
def primeGeneration():
    while (1):
        q = random.getrandbits(31) # q should be k - 1 bits, where p is k bits
        while q % 12 != 5: q = random.getrandbits(31)
        p = (2*q) + 1
        if millerRabin(p) == 0 or len(bin(p).lstrip('0b')) != 32: # ensure p is both prime and 32 bits
            continue
        else:
            return p

'''
Input: Number to be tested, n
Output: 0 if n is composite, 1 if n is prime
Purpose: Tests the primality of a number
'''
def millerRabin(n):
    if n % 2 == 0 or n < 2: return 0 # if even or 1, composite

    t = 1
    u = ((n-1)/2**t)
    while u % 2 == 0: # ensures u is odd, but n - 1 = 2^t(u) holds
        t += 1
        u = ((n-1)/2**t)

    u = int(u)
    binary = str(bin(u).lstrip('0b')) + "2"
    
    # lines 121 + 122: Assignes the ctypes equivalent of what the c functions return and take as arguments
    mathLib.millerRabin.restype = ctypes.c_int
    mathLib.millerRabin.argtypes = [ctypes.c_ulonglong, ctypes.c_ulonglong, ctypes.c_ulonglong, ctypes.c_int, ctypes.c_wchar_p]
    for i in range(20): # run check 20 times
        a = random.randrange(1, n - 1)
        primality = mathLib.millerRabin(a, n, u, t, binary) # call miller rabin from C library
        if primality == 0: return 0
    return 1

'''
Input: base, b, exponent, e, modulus, n
Output: b^e mod n
Purpose: Performs fast modular exponentiation
'''
def modExpo(b, e, n):
    binary = str(bin(e).lstrip('0b')) + "2" # append 2 as an easy way to detect end of string on C side. \0 does not work the same in python strings as in C

    mathLib.modExpo.restype = ctypes.c_ulonglong
    mathLib.modExpo.argtypes = [ctypes.c_ulonglong, ctypes.c_ulonglong, ctypes.c_ulonglong, ctypes.c_wchar_p]
    val = mathLib.modExpo(b, e, n, binary) # call modular exponentiation from C library
    return val