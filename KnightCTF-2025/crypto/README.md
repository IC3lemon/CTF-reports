## Astra Equinox
```py
from Crypto.Util.number import *
import random
ct = '_2A7$zZ3L:BEwzfjh*Bq~?V8vzv"2-/Q,au"W}5kuLjv@f)r\'r7rp_zqeiIv6JO#Azeyf'
SEED= 145556
random.seed(SEED)
shifts = [random.randint(1, 93) for _ in range(len(ct))]
pluh = ""
for i in range(len(ct)):
    ye = ord(ct[i]) - shifts[i]
    ye = (ye - 32) % 94 + 32  
    pluh += chr(ye)

charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
pls = [sum(charset.index(char) * (62 ** i) for i, char in enumerate(i[::-1])) for i in pluh.split('-')]
print("".join(chr(x) for x in pls)) # KCTF{F14G_M4K3_YOU_H4ppY}
```

## Random Senior Adleman
```py
from Crypto.Util.number import *
c = 4744275480125761149475439652189568532719997985297643024045625900665305682630452044004013647350658428069718952801828651333880186841289630294789054322237585
q = 81950208731605030173072901497240676460946134422613059941413476068465656250011
e=15537
phi = (q-1)
# print(GCD(e, phi))
d = inverse(e, phi)
print(long_to_bytes(pow(c, d, q))) # KCTF{Don't_CA#ll_Me_Herp}
```

## Forward yet it falls back 
```py
from Crypto.Util.Padding import *
from Crypto.Cipher import AES
from base64 import *

shit = b32decode("G7G2DGQ5SY4DCK5YVUDRROJI3UOAUUNTVR6XKDOKQO4CAAKK2MJA====")
key = b"0123456789ABCDEF"
iv  = b"FEDCBA9876543210"

cipher = AES.new(key, AES.MODE_CBC, iv)
flag = unpad(cipher.decrypt(shit), 16)
print(flag[::-1]) # KCTF{R3vers3_R3vers3_D3C0DE}
```

## Reflections in Random
```py
from Crypto.Util.strxor import *
from base64 import *
chipher="PzExcRcFHQsdOxF2cR0WEXIPOQQWAQk="
pluh = strxor(b64decode(chipher),(bytes.fromhex("42")*50)[:len(b64decode(chipher))])
print(pluh[::-1]) # b'KCTF{M0ST_34Sy_I_GU3ss}'
```
