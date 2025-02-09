# RSA Bummer

## Challenge :
`chal.py`
```py
from Crypto.Util.number import *
from Secrets import FLAG

def lmao(n,k,x):  #Better function needed
    pseudo_p = 1 
    for i in range(2,k*n-x):
        try:
            if (GCD(i,n-1)^(n-1)!=0):
                pseudo_p = (pseudo_p*inverse(i,n))%n
        except:
            continue
    return inverse(pseudo_p,n)

e = 27525540

while True:
    p = getPrime(1024)
    if (((15-GCD(e,(p-1)))>>(31))==0):
        break
q = getPrime(1024)
r = getPrime(1024)

modulo = p*r
pseudo_n = r*(pow(e,p,q))
multiplier = getPrime(4)

flag = bytes(FLAG)

print("Pseudo_n = ", pseudo_n)
print("e = ", e)

for i in range(3):
    pt = flag [ i*len(flag)//3 : (i+1)*len(flag)//3 ]
    ct = pow(bytes_to_long(pt),e,(p*q))
    print(f"Ciphertext {i+1} =", ct)


for i in range(5):
    x = input("Enter your lucky number : ")
    try:
        x = int(x)

    except:
        print("Not an integer")
        continue

    if((x<=23)&(x>=3)):
        print("Your lucky output : ", lmao(modulo,multiplier,x))
    else:
        print("Not your lucky day, sad.")
    print("--------------------------------------")

print("Bye!!")
```

## Solution :

After a bunch of trial and error and testing, discovered this about the `lmao` func :

$$ lmao(a) = lmao(a+1) * (k*n - a - 1) $$

i.e 

$$ lmao(a) = lmao(a+1) * k n - lmao(a+1) (a+1) $$

$$ lmao(a) + lmao(a+1) (a+1) = k n $$

$$ lmao(a) + lmao(a+1) (a+1) \equiv 0 \pmod{n} $$

so get two such values i.e 2 pairs of consecutive outputs of `lmao` \
rearragnge them according to the above, and GCD both to get n

$$ n \eq p r $$

and we have `pseudo_n` of the form `r * pow(e, p, q)` \
GCD(pseudo_n, n) to get `r`
`p = n // r`

now since we have p, we try reducing to ring p and decrypting \
but that wasnt working because in the prime generation `((15-GCD(e,(p-1)))>>(31))==0` was asserted. \
i.e. only for values 0 <= GCD(e, p-1) <= 15 does the condition hold \
because of which the chance of e being coprime to phi(p) i.e. GCD(e, phi(p)) == 1\
was 1 / 15. \
Keeping this in mind I did write this to brute to get an invertible e, but it wasn't working for some reason. flag > p somehow ??? 
```py
from pwn import *
from Crypto.Util.number import *

ct = [0, 0, 0]
lmao = [0, 0, 0, 0]
while True:
    r = remote('chals.bitskrieg.in', 7001, level='DEBUG')
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
        continue

    if GCD(e, p-1) == 1:
        flag = ''
        for c in ct:
            d = inverse(e, p - 1)
            flag += long_to_bytes(pow(c, d, p)).decode()
        print(flag)
        break
    else:
        r.close()
        continue
```

then I had flashbacks to when I was bullied by crypto titans \
![image](https://github.com/user-attachments/assets/62ad589e-1ecb-4bbc-bee4-9537aa886dcd)

so i then tried to compute nth root mod p \
but my sage kept dying, was not able to do so.. Ultimately a teammate came by, did the same stuff \
his sage worked, found the eth root mod p 

***

Post CTF i ran his script and realised, my sage.nth_root was indeed broken for whatever reason.  \
![image](https://github.com/user-attachments/assets/cafe192a-dc59-4bc8-bd5e-f103cb32acc4)


I then found implementation to compute nth roots mod prime on https://vixra.org/pdf/2205.0155v1.pdf
and that worked. 

`solve.py`
```py
from pwn import *
from Crypto.Util.number import *
from gmpy2 import iroot

ct = [0, 0, 0]
lmao = [0, 0, 0, 0]
while True:
    r = remote('chals.bitskrieg.in', 7001, level='DEBUG')
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
        r.close()
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

        print(flag)
        break
```
## `s0_fun_7o_50lv3_5ef78a03`
