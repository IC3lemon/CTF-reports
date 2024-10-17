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
