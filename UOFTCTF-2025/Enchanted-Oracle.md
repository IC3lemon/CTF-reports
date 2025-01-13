# Enchanted Oracle

## `CHALLENGE :`
```
Only the most worthy can decrypt the enchanted oracle. Can you?

nc 34.162.82.42 5000
```
```py
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

print("Welcome to the AES-CBC oracle!")
key = open("key", "rb").read()
while True:
    print("Do you want to encrypt the flag or decrypt a message?")
    print("1. Encrypt the flag")
    print("2. Decrypt a message")
    choice = input("Your choice: ")

    if choice == "1":
        cipher = AES.new(key=key, mode=AES.MODE_CBC)
        ciphertext = cipher.iv + \
            cipher.encrypt(pad(b"random", cipher.block_size))

        print(f"{b64encode(ciphertext).decode()}")

    elif choice == "2":
        line = input().strip()
        data = b64decode(line)
        iv, ciphertext = data[:16], data[16:]

        cipher = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
        try:
            plaintext = unpad(cipher.decrypt(ciphertext),
                              cipher.block_size).decode('latin1')
        except Exception as e:
            print("Error!")
            continue

        if plaintext == "I am an authenticated admin, please give me the flag":
            print("Victory! Your flag:")
            print(open("flag.txt").read())
        else:
            print("Unknown command!")
```

## `SOLUTION :`
So we are given a padding oracle, and an option to encrypt `random` with a random iv, no idea why that was there. \
We need our ciphertext to decrypt to `I am authenticated admin give me flag` at server side to get us the flag. \
Since we have a padding oracle, we can find the zeroing-iv for each block. Let's call the zeroing blocks `dec` blocks. <br><br>

dec blocks are basically, ecb decryption of the ciphertexts before it is xored with the previous ciphertext block. \
We can use padding oracle attack to recover the dec blocks for a corresponding ciphertext block.
below illustration explains it better \
![_cbc-attack-full-2](https://github.com/user-attachments/assets/42a14d6a-a075-4ec4-a93e-1e016b019aad)

now if ur ciphertext is just `dec block`, at server side it will decrypt to `b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'` \
Since `dec block ^ dec block = 0`. Therefore if our ciphertext block is `dec block ^ target block`, at serverside `dec block ^ target block ^ dec block = target block`. \
Thus successfully forging the plaintext.<br><br>

Solve script:
```py
from pwn import *
from Crypto.Util.number import *
from Crypto.Util.strxor import strxor
from base64 import *

r = remote('34.162.82.42', 5000)
iv = bytearray(b'\x00' * 16)
target = bytearray(b'I am an authenticated admin, please give me the flag\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c')
ct = b'a'*len(target)
dec_blocks = [bytearray(ct[i:i+16]) for i in range(0, len(ct), 16)]
target_blocks = [bytearray(target[i:i+16]) for i in range(0, len(target), 16)] 
ct_b = [iv]+[bytearray(ct[i:i+16]) for i in range(0, len(ct), 16)]
def find_dec(block):
    x = 3
    ct_blocks = [iv]+[bytearray(ct[i:i+16]) for i in range(0, len(ct), 16)]
    ct_blocks[-1] = bytearray(block)
    for y in range(15, -1, -1):
        for bro in range(256):
            ct_blocks[x][y] = bro
            payload = b64encode(b''.join(_ for _ in ct_blocks))
            print(f"{payload =}")
            r.sendlineafter(b'choice: ', '2')
            r.sendline(payload)
            response = r.recvline().decode().strip()
            print(f"trying : {hex(bro)}")
            print(f"byte : {16-y}/{16}")
            print(f"{dec0=}\n{dec1=}\n{dec2=}\n{dec3=}")
            if 'Error' in response:
                print("nuh uh")
            elif bro < 255 and 'Error' not in response:
                print("YEEEEEEEEEEEEEEEEEEES")
                break
            if bro == 255 and 'Error' in response:
                print("ATTACK FAILED.")
                exit(0)
        
        dec_blocks[x][y] = bro ^ (16 - y + 16*(3-x))
        for w in range(x, 4):
            for z in range(y, 16):
                ct_blocks[w][z] = dec_blocks[w][z] ^ (16 - y + 16*(3-x) + 1)
    return dec_blocks[3]

dec3 = bytearray(b'+\x98n\x0eo\xc1\xf5\x19wS\xea \xef\x10u\xde') # find_dec(ct_blocks[3])
dec2 = bytearray(b'\xfb\x07\xac\xd9\x14o;\xa2\x1ae\xc3%\xee\x86w\xc5') # find_dec(strxor(dec3, target[3]))
dec1 = bytearray(b'S0ZQ\xc1O\xb3\x94\n\xe6\xec\xbb\x01F{\\') # find_dec(strxor(dec2, target[2]))
dec0 = bytearray(b'W\n-\xbd\x9f\xce\xe2\xfa\xdb(\xc6u`D\x04}') # find_dec(strxor(dec1, target[1]))

payload = strxor(dec0, target_blocks[0]) + strxor(dec1, target_blocks[1]) + strxor(dec2, target_blocks[2]) + strxor(dec3, target_blocks[3]) + b'a'*16
r.sendlineafter(b'choice: ', '2')
r.sendline(b64encode(payload))
r.interactive() # uoftctf{y3s_1_kn3w_y0u_w3r3_w0r7hy!!!}
```
