"""
Name: Mellanie Martin
Course: CS 427
Date: April 6th, 2024
"""

import publicKey
import sys

if sys.argv[1] == "-e" and len(sys.argv) == 8:
    keyFile = sys.argv[3]
    plaintext = sys.argv[5]
    ciphertext = sys.argv[7]
    publicKey.readFilesEnc(plaintext, ciphertext, keyFile)
elif sys.argv[1] == "-d" and len(sys.argv) == 8:
    keyFile = sys.argv[3]
    plaintext = sys.argv[7]
    ciphertext = sys.argv[5]
    publicKey.readFilesDec(ciphertext, plaintext, keyFile)
elif sys.argv[1] == "-genkey" and len(sys.argv) == 2:
    publicKey.keyGeneration()
else: print("Incorrect usage. Run using:\npython ./main.py -genkey\npython ./main.py -e -k pubkey.txt -in plaintext.txt -out ciphertext.txt\npython ./main.py -d -k priket.txt -in ciphertext.txt -out plaintext.txt")

# For personal testing. Grader can run these if they'd like. No difference except it removes the requirement of command line arguments
#publicKey.keyGeneration()
#publicKey.readFilesEnc("plaintext.txt", "ciphertext.txt", "pubkey.txt")
#publicKey.readFilesDec("ciphertext.txt", "decrypted.txt", "prikey.txt")