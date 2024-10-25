# TCP51Prime
> `UNSOLVED`
> learnt a bunch though

```python
from secret import a,b,p,flag
from hashlib import sha512
from pwn import xor
from Crypto.Util.number import isPrime

assert p == a**51 + 51*b**51 and isPrime(p) and a > 0 and b > 0
print(hex(p)[2:])
print(xor(flag,sha512((str(a)+str(b)).encode()).digest()).hex())

# 1cec7c3ff93ca538e71f334e83d905eabd894729a1b515b89dc2392036bc7e5d59fad2c35dbb0a8903c8bb2e9cd5e4779a92d3f361eb1ce9fa2530c47881a8719763f828360138373ffa2ce627f8ccad08e9b5ead178c614f7899adc6a14fa33aa2216c463a04041e78cffa2c68963c6ff422a076bedd32236282eb3bd1b7ba870a3b1c8f639cd536cba329b10a6cf7b4ef78bd11052ff8a0d432fb6d3b221742aa1da6914876e94aca5abdaeef30acdfc90cbc621245ad288a634e8bdf4152ea8ed0062c872ace7b4011dc5743fa9c424413f4e3e8fa5c5513fd4a711141f2ef68c01177f78945db623ac6cc762a6813f11cc278a143ea657bf309e281ef59048a29f279c9ad8b37f221ac06242f577bba985a2aaec051d95391a9681f905472f4e7d1322da492639ee4a5ac776a476cece55f9dfb782c1ef869deed2226691d3157fbb6b131968ebfb1fe5bc1e44a158f1e2321c001355cc9cb3344f6b09b78d965a807cd60d58a9efbab8c6d4f75c8e5ac7c9cf0e5409b55bb2133129272685913be02166c6bffe3747ccd186b6c26fc9f09
# 43edcf6275293ce97d716f49875c4bdba37f6ab30f15a53f09b72bf3816edf6b92618fb56d569d911b2f6fe7a36d4a854022dddf671dc89b4800bc1605822aab72d3
```


learnt a lot in this one \
in a nutshell 
```
p = a**51 + 51*b**51
p is prime and given
a > 0
b > 0

find a b

xor hash(str(a) + str(b)) with given hex, flag mil gaya
```

so clearly, we have a formula `p = a**51 + 51*b**51` \
from which we have to find a,b 

## Approach -

now if we do mod 51 both sides 
```
p = a**51 (mod 51)
```
then find the 51th root of p mod 51. \
that would find a % 51 \
got that via this script 
```python
from sympy import mod_inverse
from Crypto.Util.number import *
import gmpy2

def mod_pow(base, exponent, modulus):
    result = 1
    while exponent > 0:
        if exponent & 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result

def find_cube_root_mod_17(y):
    y = y % 17
    for x in range(17):
        if mod_pow(x, 3, 17) == y:
            return x
    return None

def find_51st_root_mod_51(y):
    y = y % 51
    
    x_mod_3 = y % 3
    
    x_mod_17 = find_cube_root_mod_17(y)
    
    if x_mod_17 is None:
        return None
    
    # Use Chinese Remainder Theorem to combine solutions
    m1, m2 = 3, 17
    M = m1 * m2
    y1 = mod_inverse(M // m1, m1)
    y2 = mod_inverse(M // m2, m2)
    
    x = (x_mod_3 * (M // m1) * y1 + x_mod_17 * (M // m2) * y2) % M
    return x
```

right so this gave 
```
a % 51 = 11
```
I tried bruteforcing k for `a = 11 + 51*k` and find a \
but that took very very very long. \
tired, I went to the tickets where this happened \
![image](https://github.com/user-attachments/assets/b9d00282-60f8-46f8-a4ec-cef64153c74c)
![image](https://github.com/user-attachments/assets/cb2bc180-c660-460c-80f2-374dc2c33bd4)

I was stuck most of the ctf trying to figure out what he meant \
turns out... 
*IT WAS LLL YAAAAAAAAAAY*
## Solve -
```sage
p = ...
x = int(GF(p)(-51).nth_root(51))
M = Matrix([[p,0],[x,1]])
a, b = -M.LLL()[0]
assert p == a**51 + 51*b**51
```

## Takeaways -
Im starting to hate LLL \
like i said, doing the CryptoHack module, once that is done, \
will start grinding as many lattice challenges i can find. \
There's a bunch from the past ctf's so i think im good.

## SOLVED LATER 

right i learnt LLL \
ok so given is \
```
p == a**51 + 51*b**51 and isPrime(p) and a > 0 and b > 0
```

pretty clear, find `a`, `b` \
Ight so consider 
```
a**51 = A
b**51 = B
```

now 
```
p = A + 51B
```
taking `mod p` both sides
```
0 = A + 51B (mod p)
A = 51B     (mod p)
```
taking 51ist root mod p on both sides
```
a = 51**(1/51) * b
```
let `51**(1/51) = x` then 
```
a = xb  (mod p)
```

In this statement, a,b are unknowns, x can be calculated and found, p is known \
for constructing the lattice : \
```
a + pk = bx
bx - kp = a
```
converting this to vectors 
```
b[x, 1] - k[p, 0] = [bx-kp, b]
b[x, 1] - k[p, 0] = [a , b]
```
THEREFORE we have linearly expressed a combination using the basis vectors `[x,1],[p,0]` to find `[a,b]` \
we thus reduce the lattice `[x,1] [p,0]` to find a, b \
script : 
```python
"""
p = a**51 + 51*b**51
p is prime
a > 0
b > 0

A = a**51 
B = b**51

A + 51B = p
A + 51B = 0 (mod p)
A = -51B (mod p)

51st root both sides
a =     (-51)**(-51)           *  b  + kp
    { calling above x }

a =        xb                        + kp

b[x, 1] + k[p, 0] = [x*b + kp, b]
b[x, 1] + k[p, 0] = [a, b]
"""
from Crypto.Util.number import *
from pwn import xor
from hashlib import sha512

p = 0x1cec7c3ff93ca538e71f334e83d905eabd894729a1b515b89dc2392036bc7e5d59fad2c35dbb0a8903c8bb2e9cd5e4779a92d3f361eb1ce9fa2530c47881a8719763f828360138373ffa2ce627f8ccad08e9b5ead178c614f7899adc6a14fa33aa2216c463a04041e78cffa2c68963c6ff422a076bedd32236282eb3bd1b7ba870a3b1c8f639cd536cba329b10a6cf7b4ef78bd11052ff8a0d432fb6d3b221742aa1da6914876e94aca5abdaeef30acdfc90cbc621245ad288a634e8bdf4152ea8ed0062c872ace7b4011dc5743fa9c424413f4e3e8fa5c5513fd4a711141f2ef68c01177f78945db623ac6cc762a6813f11cc278a143ea657bf309e281ef59048a29f279c9ad8b37f221ac06242f577bba985a2aaec051d95391a9681f905472f4e7d1322da492639ee4a5ac776a476cece55f9dfb782c1ef869deed2226691d3157fbb6b131968ebfb1fe5bc1e44a158f1e2321c001355cc9cb3344f6b09b78d965a807cd60d58a9efbab8c6d4f75c8e5ac7c9cf0e5409b55bb2133129272685913be02166c6bffe3747ccd186b6c26fc9f09
# find x
from math import gcd

def extended_gcd(a, b):
    """
    Extended Euclidean Algorithm
    Returns (gcd, x, y) such that a * x + b * y = gcd
    """
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    """
    Returns the modular multiplicative inverse of a modulo m
    """
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise Exception('Modular inverse does not exist')
    return x % m

def find_51st_root(p):
    """
    Find the 51st root of -51 in field mod p
    Returns a value x where x^51 ≡ -51 (mod p)
    """
    n = 51
    target = (-51) % p
    
    # Check if p-1 and n are coprime (required for unique solution)
    if gcd(n, p-1) != 1:
        return None
    
    # Find modular multiplicative inverse of n modulo p-1
    n_inv = mod_inverse(n, p-1)
    
    # Use Euler's theorem: a^((p-1)/2) ≡ ±1 (mod p)
    # Then root = target^(n_inv) mod p
    result = pow(target, n_inv, p)
    
    # Verify the result
    if pow(result, n, p) == target:
        return result
    return None

x = find_51st_root(p)

bad_basis = [[x,1], [p,0]]

def mag(vector):
    return vector[0]**2 + vector[1]**2

def dot(a, b):
    if len(a) < len(b):
        a += [0] * (len(b) - len(a))
    elif len(b) < len(a):
        b += [0] * (len(a) - len(b))
    
    dot_product = sum(x * y for x, y in zip(a, b))
    return dot_product

def scalar(a: float, b: list) -> list:
    return [a * i for i in b]

def sub(a: list, b: list) -> list:
    if len(a) < len(b):
        a += [0] * (len(b) - len(a))
    elif len(b) < len(a):
        b += [0] * (len(a) - len(b))
    return [A - B for A, B in zip(a, b)]

def Gaussian_Lattice_Reduction(basis):
    v1 = basis[0]
    v2 = basis[1]
    while True:
        if mag(v1) > mag(v2):
            v1, v2 = v2, v1
        m = int(dot(v1,v2) // dot(v1, v1))
        if m == 0:
            return [v1, v2]
        v2 = sub(v2 ,scalar(m,v1))
good_basis = Gaussian_Lattice_Reduction(bad_basis)
svp = good_basis[0]
a,b = svp[0], svp[1]
print(f"{a=}\n{b=}")

enc_flag = 0x43edcf6275293ce97d716f49875c4bdba37f6ab30f15a53f09b72bf3816edf6b92618fb56d569d911b2f6fe7a36d4a854022dddf671dc89b4800bc1605822aab72d3
key = sha512((str(a)+str(b)).encode()).digest()
flag = xor(long_to_bytes(enc_flag), key)
print(flag.decode())

```
***

# Talking Phase
> `SOLVED` by Harshith

basically, you are a man in the middle \
therefore mitm. \
the server checks if `giv me the flag u damn donut` has been communicated anywhere \
if it has, it gives you the flag. You are able to tamper the public keys, and messages of both entities \
So u can see the publickeys \
now `A`'s message is going to be recieved by `B` \
THEREFORE, encrypt `A`'s message with `B`s pubkey 
```
encrypt " giv me the flag u damn donut " using B's key
change A's message to this
```
and then `B` sends you back the flag in b64
