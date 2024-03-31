/*
Author: Mellanie Martin
Class: CS 427 - Cryptography & Network Security
Date: 2/17/24
*/

# include <stdio.h>
# include <stdlib.h>
# include <string.h>
#include <time.h>
#include <math.h>

int millerRabin(unsigned long long a, unsigned long long n, unsigned long long u, char *binary);
unsigned long long modExpo(unsigned long long b, unsigned long long e, unsigned long long n, char *binary);

/*
Input: witness, input number, and number of witnesses
Output: prints if n is composite or likely prime
*/
int millerRabin(unsigned long long a, unsigned long long n, unsigned long long u, char *binary) {

    unsigned long long x = modExpo(a, u, n, binary);
    unsigned long long xOne = (x*x)%n;
    if (xOne == 1 && x != 1 && x != (n-1)) {
        return 1;
    }
    if (xOne != 1) {
        return 1;
    }
    return 0;
}

/*
Input: base, exponent, modulus
Output: returns b^e mod n
*/
unsigned long long modExpo(unsigned long long b, unsigned long long e, unsigned long long n, char *binary) {
    unsigned long long c = 0, d = 1;

    for (int i = 0; binary[i] != '2'; i++) {
            c = 2*c;
            d = (d*d)%n;
            if (binary[i] == '1') {
                c = c + 1;
                d = (d*b)%n;
            }
    }
    return d;

}