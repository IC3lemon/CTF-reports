# Golden Ticket

## Aproach :
we are ultimately given two equations
```

c1 = 13**flag + 37**flag (mod p)
c2 = 13**(flag-1) + 37**(flag-1)  (mod p)

(where flag is the only unknown)

```

So did this :
```
x = 13**(flag-1)
y = 37**(flag-1)
```

because then we got 2 equations in 2 variables, which should be solvable. 
```

c1 = 13x + 37y  (mod p)
c2 = x + y      (mod p)

```
now 
```

x = c2 - y (mod p)

```
putting the value of x in eqn 1 we get 
```

c1 = 13(c2 - y) + 37y (mod p)
=>   c1 = 13c2 - 13y + 37y (mod p)
=>   c1 = 13c2 - 24y (mod p)
=>   24y = 13c2 - c1 (mod p)

```
this was where I got stuck, because division in mod math doesn't work \
but dhruti came in and taught that \
you can multiply with mod inv of 24 both sides to get rid of 24.
```

24y * modinv(24,p) = (13c2 - c1) * modinv(24,p)  (mod p)
y = (13c2 - c1) * modinv(24,p)  (mod p)

```
now `y = 13**(flag-1)  (mod p)` which is a discrete log pproblem that can be solved via alpertron or sage. \
did that and got `flag - 1`. added 1 to the same and got flag. 

## Solve :
```python
from Crypto.Util.number import *

shit = [88952575866827947965983024351948428571644045481852955585307229868427303211803239917835211249629755846575548754617810635567272526061976590304647326424871380247801316189016325247, 67077340815509559968966395605991498895734870241569147039932716484176494534953008553337442440573747593113271897771706973941604973691227887232994456813209749283078720189994152242]
c1 = shit[-1]
c2 = shit[-2]
p = 396430433566694153228963024068183195900644000015629930982017434859080008533624204265038366113052353086248115602503012179807206251960510130759852727353283868788493357310003786807
    
# 24y = c1 - 13c2

from sympy import mod_inverse

inv_24 = mod_inverse(24, p)
    
y = ((c1 - 13 * c2) * inv_24) % p
print(y)
 
alpertroned = int("57629776445896163024735745086814515288454966100802334039751672315837361336412607584713634047210889596") + 1    # +1 because y = 13**(flag - 1)   alpertroned would be flag-1
print(long_to_bytes(alpertroned))   # idek{charles_and_the_chocolate_factory!!!}
```
