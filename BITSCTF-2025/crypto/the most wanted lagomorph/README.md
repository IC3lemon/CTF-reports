# the most wanted lagomorph

## Challenge
```
簾簿 簾簽 簽籶 簽籀 簿簼 簼簻 簾簻 簽籁 簾簿 簿米 籀簽 簾籂 簽米 簾簼 籀簽 簽籴 簾籂 簼簻 簿籵 籀籂 簾簽 簽簿 簽簿 簼簻 簾簾 簽簿 簾簻 簼簾 簽米 簽簽 簾籶 簿籲 簾籂 簾簽 簾籂 簼簻 簿簼 簾簾 簼簺 簾簾 簾簻 簽籀 簿簽 籀簿 簾簽 簼簻 簿籴 籀籀 簽籲 簿籴 簽籲 簼簽 簾簼 簽簽 簽簿 簼簹 簽籲 簼簹 簾簿 籀籂 簾籶 簾簾 簿籴 籀簽 簿簾 簽簿 簿簽 簽簽 簾簾 簽簽 簽籲 簾簼 簾籂 簾籁 簽籶 簾簾 簿簾 簾簿 簽籶 簾簾 簾簿 簾簽 簽籶 籀簻 簽米 簼簹 簼簾 籀籂 簾籶 簽簽 簾簻 簼簻 簾簺 簼簻 簿籁 簼簿 簾籂 簼簺 簿籁 簾籶 簾簼 簼簼 簽簿 簾簺 簾籀 簿籴 簽籲 簼簾 簿簻 簽簽 簽籲 簾簾
```
```no more Bunny Business```

## Solution
![image](https://github.com/user-attachments/assets/b6e0332d-a398-489a-8c19-4e73bdb6abb8)

The base 64 you recieve `U2FsdGVkX1+Kci2LQvPTy06ga66qMTDgoOip6SxH1t7EreImxWCP3RarTyRTU2k3Nrd4vChzcXYKqPZSyl3T` \
decodes to this :
```
b'Salted__\x8ar-\x8bB\xf3\xd3\xcbN\xa0k\xae\xaa10\xe0\xa0\xe8\xa9\xe9,G\xd6\xde\xc4\xad\xe2&\xc5`\x8f\xdd\x16\xabO$SSi76\xb7x\xbc(sqv\n\xa8\xf6R\xca]\xd3'
```
the string starting with `Salted_` suggests it was encrypted via a stream cipher or openssl. \
But after probing a bit, teammates alerted that lagomorph is a Bunny, entire chall is centered around rabbits, \
and ssure enough, there exists a `Rabbit Cipher` FUCKING RABBIT CIPHER. https://www.codeeeee.com/en/encrypt/rabbit.html \
and yes it is a stream cipher. Now to figure out the passphrase for it. \
tried bunny, rabbit, lagomorph everything. NUHUH guess what the password was.... \
***`dennis`*** FUCKING DENNIS. ASS CHALLENGE. AND HOW DID I FIGURE THAT OUT ?? \
![image](https://github.com/user-attachments/assets/a9434a6d-f6ca-4f96-b866-f9d9ca7c6aa9) \
PEAK CRYPTOGRAPHY GUYS.

decrypted the rabbit cipher off of https://www.codeeeee.com/en/encrypt/rabbit.html \
![image](https://github.com/user-attachments/assets/534b7b48-30f1-4a18-93a5-790de35d24ac)

## `BITSCTF{f3rb_1_kn0w_wh47_w3_4r3_60nn4_d0_70d4y}`

