from pwn import *
from Crypto.Util.number import *
from gmpy2 import iroot

ct = [0, 0, 0]
lmao = [0, 0, 0, 0]
while True:
    r = remote('chals.bitskrieg.in', 7001)
    r.recvuntil(b'Pseudo_n = ')
    pseudo_n = int(r.recvline().decode().strip())
    r.recvuntil(b'e = ')
    e = int(r.recvline().decode().strip())

    for i in range(3):
        r.recvuntil(b'Ciphertext ' + str(i+1).encode() +b' = ' )
        ct[i] = int(r.recvline().decode().strip())

    j=0
    for i in range(3, 7):
        r.sendlineafter(b'Enter your lucky number : ', str(i).encode())
        r.recvuntil(b'Your lucky output :')
        lmao[j] = int(r.recvline().decode().strip())
        j += 1

    # L(x) + L(x+1)*(x+1) = 0 (mod n)
    n = GCD(lmao[2] + lmao[3]*6, lmao[0] + lmao[1]*4)
    R = GCD(n, pseudo_n)
    if not isPrime(R):
        print("R NOT PRIME")
        continue
    e = 27525540
    p = n // R
    if not isPrime(p):
        print("P NOT PRIME")
        r.close()
        continue

    else:
        flag = ''
        g = GCD(e, p-1)
        e_prime = e // g
        t = (p - 1) // g
        d_prime = inverse(e_prime, t)
        for c in ct:
            X = pow(c, d_prime, p)
            root, exact = iroot(X, g)
            if exact:
                flag += long_to_bytes(root).decode()    
            else:
                print("NO ROOTS")

        print(f" flag : {flag}")
        break

# s0_fun_7o_50lv3_5ef78a03
