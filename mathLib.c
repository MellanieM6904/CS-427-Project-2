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

int millerRabin(unsigned long long a, unsigned long long n, unsigned long long u, int t, char *binary);
unsigned long long modExpo(unsigned long long b, unsigned long long e, unsigned long long n, char *binary);

/*
Input: witness, input number, and number of witnesses
Output: prints if n is composite or likely prime
*/
int millerRabin(unsigned long long a, unsigned long long n, unsigned long long u, int t, char *binary) {
    unsigned long long x0, x1;
    x0 = modExpo(a, u, n, binary);
    for (int i = 0; i <= t; i++) {
        x1 = (x0*x0)%n;
        if ((x1 == 1) && (x0 != 1) && (x0 != n - 1)) {
            return 0;
        }
        x0 = x1;
    }
    if (x1 != 1) return 0;
    return 1;
}

/*
Input: base, exponent, modulus
Output: returns b^e mod n
*/
unsigned long long modExpo(unsigned long long b, unsigned long long e, unsigned long long n, char *binary) {
    unsigned long long c = 0, d = 1;
    int i = 0;
    for (i = 0; binary[i] != '2'; i++);

    for (int k = 0; k <= i - 1; k++) {
            if (binary[k] == '\0') continue;
            c = 2*c;
            d = (d*d)%n;
            if (binary[k] == '1') {
                c = c + 1;
                d = (d*b)%n;
            }
    }
    return d;
}