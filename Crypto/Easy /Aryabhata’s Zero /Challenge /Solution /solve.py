#!/usr/bin/env python3
# solve.py
# Usage: python3 solve.py challenge.txt
# It parses N, e, c, masked and tries all ways to insert exactly 3 zeros.

import sys
import itertools

def parse_challenge(fn):
    with open(fn) as f:
        txt = f.read()
    # crude parse
    def extract(name):
        for line in txt.splitlines():
            if line.strip().startswith(name + " ="):
                return line.split('=',1)[1].strip()
    N = int(extract('N'))
    e = int(extract('e'))
    c = int(extract('c'))
    masked = extract('masked')
    return N, e, c, masked

def int_to_bytes(n):
    if n == 0:
        return b'\x00'
    blen = (n.bit_length() + 7)//8
    return n.to_bytes(blen, 'big')

def try_insert_zeros(masked, zeros_to_insert=3):
    # positions are between digits; we can insert zeros anywhere including start/end
    L = len(masked)
    # We will create combinations with repetition of positions (monotonic)
    # Equivalent to distributing zeros into L+1 slots
    slots = L + 1
    # generate integer partitions of zeros_to_insert into 'slots' parts (compositions)
    # using stars and bars: combinations with repetition of choosing zeros_to_insert positions among slots
    # iterate all weak compositions via nested loops / itertools.combinations_with_replacement
    for positions in itertools.combinations_with_replacement(range(slots), zeros_to_insert):
        # build list of counts per slot
        counts = [0]*slots
        for pos in positions:
            counts[pos] += 1
        # construct candidate decimal by injecting counts[i] zeros before masked[i] (i from 0..L, with masked[L] after)
        out = []
        for i in range(slots):
            if counts[i]:
                out.append('0'*counts[i])
            if i < L:
                out.append(masked[i])
        cand = ''.join(out)
        yield cand

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 solve.py challenge.txt")
        sys.exit(1)
    N,e,c,masked = parse_challenge(sys.argv[1])
    print("[*] N={}, e={}, c={}".format(N,e,c))
    print("[*] masked=", masked)
    tried = 0
    for cand in try_insert_zeros(masked, zeros_to_insert=3):
        tried += 1
        m_candidate = int(cand)
        if pow(m_candidate, e, N) == c:
            print("[+] Found candidate m (decimal):", cand)
            try:
                b = int_to_bytes(m_candidate)
                flag = b.decode()
            except Exception as ex:
                print("[!] Could not decode as UTF-8:", ex)
                flag = None
            print("[+] Recovered flag:", flag)
            return
    print("[-] No candidate matched after trying", tried, "variants.")

if __name__ == '__main__':
    main()
