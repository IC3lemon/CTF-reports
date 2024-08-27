# Some Trick

we are given below script 
```python
import random
from secrets import randbelow, randbits
from flag import FLAG

CIPHER_SUITE = randbelow(2**256)
print(f"oPUN_SASS_SASS_l version 4.0.{CIPHER_SUITE}")
random.seed(CIPHER_SUITE)

GSIZE = 8209
GNUM = 79

LIM = GSIZE**GNUM


def gen(n):
    p, i = [0] * n, 0
    for j in random.sample(range(1, n), n - 1):
        p[i], i = j, j
    return tuple(p)


def gexp(g, e):
    res = tuple(g)
    while e:
        if e & 1:
            res = tuple(res[i] for i in g)
        e >>= 1
        g = tuple(g[i] for i in g)
    return res


def enc(k, m, G):
    if not G:
        return m
    mod = len(G[0])
    return gexp(G[0], k % mod)[m % mod] + enc(k // mod, m // mod, G[1:]) * mod


def inverse(perm):
    res = list(perm)
    for i, v in enumerate(perm):
        res[v] = i
    return res


G = [gen(GSIZE) for i in range(GNUM)]


FLAG = int.from_bytes(FLAG, 'big')
left_pad = randbits(randbelow(LIM.bit_length() - FLAG.bit_length()))
FLAG = (FLAG << left_pad.bit_length()) + left_pad
FLAG = (randbits(randbelow(LIM.bit_length() - FLAG.bit_length()))
        << FLAG.bit_length()) + FLAG

bob_key = randbelow(LIM)
bob_encr = enc(FLAG, bob_key, G)
print("bob says", bob_encr)
alice_key = randbelow(LIM)
alice_encr = enc(bob_encr, alice_key, G)
print("alice says", alice_encr)
bob_decr = enc(alice_encr, bob_key, [inverse(i) for i in G])
print("bob says", bob_decr)

```

In a nutshell, \
The gen function creates random permutations, gexp and inverse manipulate these permutations, and enc uses them to encrypt a message. \
Is what I believed.

and turns out I was right as well. Now what I thought the challenge was. was to reverse the random. \
Because I thought, "oh, G is being randomly generated. Have to reverse python's random to predict a correct G". \
NO. THE SEED FOR THE RANDOM WAS GIVEN. \
![image](https://github.com/user-attachments/assets/4e52a064-aeac-4ae7-9782-c8ff8fb11c9c)

:sob::sob::sob::sob::sob: \
Now once we know seed. We can get the correct G by just copying and mimicking the functions in chall script with the correct seed. \
Then we can see some operations happening to the flag which we get around to later.
```python
FLAG = int.from_bytes(FLAG, 'big')
left_pad = randbits(randbelow(LIM.bit_length() - FLAG.bit_length()))
FLAG = (FLAG << left_pad.bit_length()) + left_pad
FLAG = (randbits(randbelow(LIM.bit_length() - FLAG.bit_length()))
        << FLAG.bit_length()) + FLAG
```

and we also got these three things. \
![image](https://github.com/user-attachments/assets/ade91c9d-8169-434d-9e42-4a9912c1c65f)

so bob says  is `bob_encr` i.e. the weird FLAG encrypted with bob's key. \
alice says is `alice_encr` i.e. bob_encr encrypted with alice's key. \
the next bob says is `bob_decr` which is alice_encr encrypted with bob's key. I think is an example for the decryption using the given functions \
using the `inverse` function like so :
```python
bob_decr = enc(alice_encr, bob_key, [inverse(i) for i in G])
```

now using this, we can decrypt to get bob's key and alice's key like so : 
```python
bob_key_rec = enc(alice_encr, bob_decr, G)
alice_key_rec = enc(bob_encr, alice_encr, [inverse(i) for i in G])
```
now we got bob's key. We got bob's encrypted message. Now to extract bob's message i.e. the messed up FLAG. \
we have to reverse the enc (and gexp) function entirely. We can't directly do that. But since the modulus of the operations `GSIZE` is `8209` \
which is a small enough prime. We can bruteforce this process. \

```python
GSIZE = 8209
flag = []
b_k = bob_key
b_e = bob_encr
for g in G:
    mm = b_k % GSIZE
    for k in range(GSIZE):
        if mm == b_e % GSIZE:
            flag.append(k - 1)
            break
        mm = g[mm]
    b_k //= GSIZE
    b_e //= GSIZE

flag_rec = sum(x * GSIZE**i for i, x in enumerate(flag_rec))
```

once that done now we have the weird FLAG \
need to just reverse the weird bit shifts. That was just 16 bit shifts.\
```python
flag = b''.join(long_to_bytes(flag << i) for i in range(16))
ind = flag.index(b'EKAI{')  # the flag was padded  
flag = b'S' + flag[ind:]
ind = flag.index(b'}')
flag = flag[:ind + 1]
print(flag)
```

![image](https://github.com/user-attachments/assets/f0439c6e-19fd-4b08-8f10-efc07942a395)


## takeaways : 
- honestly this was well solvable. I fell down the rabbit hole of reversing python's system random.
- do not be intimidated by random. Read the script better.
