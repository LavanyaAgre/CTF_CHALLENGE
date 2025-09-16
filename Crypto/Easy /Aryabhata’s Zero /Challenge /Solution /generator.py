#!/usr/bin/env python3
# generator.py
# Produces challenge.txt containing N, e, c, and masked decimal string (zeros removed)
# For CTF authors: change FLAG variable or set environment CTF_FLAG

import os
import random
from hashlib import sha256

def small_prime_candidate(nbits=16):
    # simple prime generation for small size (for CTF)
    import sympy
    return sympy.randprime(2**(nbits-1), 2**nbits - 1)

def int_from_flag(flag):
    # convert flag string to integer via hex
    return int(flag.encode().hex(), 16)

def remove_exact_zero_digits_decimal(m_int, remove_count=3):
    dec = str(m_int)
    # remove exactly remove_count characters that are '0'
    # ensure there are at least remove_count zeros
    zeros = dec.count('0')
    if zeros < remove_count:
        raise ValueError("Not enough zero digits in decimal representation to remove.")
    # greedily remove first remove_count zeros for deterministic instance
    removed = 0
    out = []
    for ch in dec:
        if ch == '0' and removed < remove_count:
            removed += 1
            continue
        out.append(ch)
    return ''.join(out)

def main():
    FLAG = os.environ.get('CTF_FLAG', 'FLAG{ARYABHATA_ZERO}')
    remove_count = 3

    # small RSA key for CTF convenience (NOT secure)
    p = small_prime_candidate(16)
    q = small_prime_candidate(16)
    while p == q:
        q = small_prime_candidate(16)
    N = p * q
    e = 65537
    # ensure gcd(e, phi(N)) == 1
    phi = (p-1)*(q-1)
    if __import__('math').gcd(e, phi) != 1:
        # pick alternate small e
        e = 3
        if __import__('math').gcd(e, phi) != 1:
            e = 17

    m = int_from_flag(FLAG)
    # check decimal has enough zeros; if not, modify flag by appending zeros in ascii
    dec = str(m)
    if dec.count('0') < remove_count:
        # append a zero-byte at end by adding '\x00' to flag (non-printing)
        # but we prefer printable flag; simplest: pad flag with '0' char (ASCII 48)
        FLAG = FLAG + '0'
        m = int_from_flag(FLAG)
        dec = str(m)
        if dec.count('0') < remove_count:
            raise SystemExit("Flag's decimal representation still doesn't have enough zero digits; modify FLAG.")

    masked = remove_exact_zero_digits_decimal(m, remove_count)

    # compute ciphertext: c = m^e mod N
    c = pow(m, e, N)

    with open('challenge.txt', 'w') as f:
        f.write("Title: Aryabhata's Zero\n\n")
        f.write("N = {}\n".format(N))
        f.write("e = {}\n".format(e))
        f.write("c = {}\n".format(c))
        f.write("\n# masked decimal representation (zeros removed):\n")
        f.write("masked = {}\n".format(masked))
        f.write("\n# note: exactly {} zero digits were removed from original decimal of m.\n".format(remove_count))
        f.write("# Your job: insert the three zeros (in the right places) to reconstruct m, then convert m -> bytes -> flag.\n")
        f.write("# Format of flag: FLAG{...}\n")
    print("Generated challenge.txt. Hand this file to players.")
    print("FLAG used (author):", FLAG)

if __name__ == '__main__':
    main()
