from Crypto.Util.number import *
from sage.all import *
from pwn import *

def get_values(b, _b, nbit):
    return [b[:i] or "L" for i in range(nbit) if b[i] == _b]

nbit = 256
r = remote('5.75.193.99', 33337)

def get_hashes(conn):
   _X = []
   _Y = []
   while True:
       line = conn.recvline().decode()
       if "greater" in line:
           break
           
       if "Info: _X" in line:
           hash_val = line.split("= ")[1].strip()
           _X.append(hash_val)
       elif "Info: _Y" in line:
           hash_val = line.split("= ")[1].strip()
           _Y.append(hash_val)
       
   conn.sendline(b"n")
   return _X, _Y


if __name__ == "__main__":
   iteration = 0
   starter = bin(0)[2:].zfill(nbit)
   
   _n = starter
   while True:
    print(f'[+] iteration {iteration}')
    if iteration == 171:
        print(f"n : {_n}")
        break
    iteration += 1
    print(f"current n : {_n}")
    r.sendline(str(int(_n, 2)).encode())
    r.recvuntil(b"[Y]es or [N]o?")
    r.sendline(b"y")
    _X, _Y = get_hashes(r)
    
    # print(f"{_X= }")
    # print(f"{_Y= }")
        
    _yB = bin(int(_n, 2))[2:].zfill(nbit)
    Y = get_values(_yB, '0', nbit)
    found = 0
    for shit in _X:
        if shit in _Y:
            found = 1
            print(_Y[_Y.index(shit)], shit)
            match = Y[_Y.index(shit)]
            if match == 'L':
                _n = "1" + _n[len('1'):]
            else:
                _n = match + '1' + _n[len(match)+1:]
            print(f"match : {Y[_Y.index(shit)]}")

    if found == 0 :
        print('no more matches')
        print(f'n = {_n}')
        if(_n[-1] == '0') or (_n[0] == '0'):
            print('bad n recovered, run again...')
            exit(0)
    
   ct = int(r.recvline().decode().strip('┃ [+] Congratulation! But you just got the encrypted flag:'))
   print(f"ct : {ct}")
   print("factoring n...")
   factors = factor(int(_n, 2))
   assert len(factors) == 2, f"SADGE, N HAS {len(factors)} FACTORS, RECOVERY GONE WRONG SOMEWHERE."
   p, q = [int(f[0]) for f in factors]
   n = p*q
   e = 0x10001
   d = inverse(e, (p-1)*(q-1))
   print(f"flag : ASIS{{{long_to_bytes(pow(ct, d, n)).decode()}}}") # ASIS{MPC_1n_4c7!0n_iZ_3Asy?!}
