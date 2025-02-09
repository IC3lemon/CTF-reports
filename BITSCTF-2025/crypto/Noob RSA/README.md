# Noob RSA Returns

## Challenge :
`chal.py`
```py
from Crypto.Util.number import getPrime, bytes_to_long

def GenerateKeys(p, q):
    e = 65537
    n = p * q
    phi = (p-1)*(q-1)
    d = pow(e, -1, phi)
    C = 0xbaaaaaad
    D = 0xdeadbeef
    A= 0xbaadf00d
    K = (A*p**2 - C*p + D)*d
    return (e, n, K)

def Encrypt():
    flag = b"REDACTED" # HEHEHEHEHE
    p = getPrime(512)
    q = getPrime(512)
    e, n, K = GenerateKeys(p, q)
    pt = bytes_to_long(flag)
    ct = pow(pt, e, n)
    
    print(f"e = {e}")
    print(f"n = {n}")
    print(f"ct = {ct}")
    print(f"K = {K}")

Encrypt()
```

`chall.txt`
```
e = 65537
n = 94391578028846794543970306963076155289398888845132329034244336898352288130614402434536624297683695128972774452047972797577299176726976054101512298009248486464357336027594075427866979990479026404794249095503495046303993475122649145761379383861274918580282133794104162177538259963029805672413580517485119968223
ct = 39104570513649572073989733086496155533723794051858605899505397827989625611665929344072330992965609070817627613891751881019486310635360263164859429539044097039969287153948226763672953863052936937079161030077852648023719781006057880499973169570114083902285555659303311508836688226455433255342509705736365222119
K = 20846957286553798859449981607534380028938425515469447720112802165918184044375264023823946177012518880630631981155207307372567493851397122661053548491580627249805353321445391571601385814438186661146844697737274273249806871709168307518276727937806212329164651501381607714573451433576078813716191884613278097774416977870414769368668977000867137595804897175325233583378535207450965916514442776136840826269286229146556626874736082105623962789881101475873449157946816513513532838149452759771630220014344325387486921028690085783785067988074331005737389865053848981113695310344572311901555735038842261745556925398852334383830822697851
```

## Description :
break it this time

## Solve :
We have  
$$ K = (A p^2 - C p + D) d $$

$$ K e = (A p^2 - C p + D) d e $$

$$ K e = (A p^2 - C p + D) (1 + k \varphi(n)) $$

$$ K e = (A p^2 - C p + D) (1 + k (p-1)(q-1)) $$

Taking mod $p-1$ on both sides:

$$ K e \equiv A p^2 - C p + D \pmod{p-1} $$

Since ${p \equiv 0 \pmod{p-1}}$:

$$ K e \equiv A - C + D \pmod{p-1} $$

$$ K e - A + C - D \equiv 0 \pmod{p-1} $$

Thus:

$$ K e - A + C - D = k (p-1) \quad \text{----- eqn (x)} $$

This is where I was stuck on for a while, until my teammate swinged by and solved the rest

by **Fermat's Little Theorem**:

$$ a^{p-1} \equiv 1 \pmod{p} $$

$$ a^{k (p-1)} \equiv 1 \pmod{p} $$

$$ a^{k (p-1)} - 1 \equiv 0 \pmod{p} $$

From eqn $\text{(x)}$:

$$ a^x - 1 \equiv 0 \pmod{p} $$

Thus,  $p \mid a^x - 1$, meaning:

$$ \gcd(a^x - 1, n) = p $$

n factored, RSA broken yay.

`solve.py`
```py
from Crypto.Util.number import *

C = 0xbaaaaaad
D = 0xdeadbeef
A= 0xbaadf00d
e = 65537
n = ...
ct = ...
K = ...
x = K*e - A + C - D
p = GCD(pow(2, x, n) -1, n)

print(long_to_bytes(pow(ct, inverse(e, p-1), p)).decode()) 
# BITSCTF{I_H0P3_Y0UR3_H4V1NG_FUN_S0_F4R_EHEHEHEHEHO_93A5B675}
```

## `BITSCTF{I_H0P3_Y0UR3_H4V1NG_FUN_S0_F4R_EHEHEHEHEHO_93A5B675}`
