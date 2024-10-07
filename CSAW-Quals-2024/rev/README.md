# Obfuscation [ unsolved ]

crazy crazy chal. legit too much obfuscation. \
So this is a VM chal. custom instructions exist. \
First big discoveries made when tryna solve were these in the decompilation \
![image](https://github.com/user-attachments/assets/61ccded3-76c7-4674-a509-918929294c45)

this looked to weird. But I believe we sadly didn't go forth with this. 

## then saw the writeups -
turns out those were opcodes. You had to sit down. TRACE EACH opcode, to understand what it is \
Then make a CUSTOM DISASSEMBLER, TO MAKE SENSE OF THE THING OMGW 
```python
import struct

with open('prog.bin', 'rb') as f:
    program = list(u[0] for u in struct.iter_unpack('<Q', f.read()))
u64_to_i32 = lambda x: struct.unpack('<i', struct.pack('<Q', x)[:4])[0]

def var(program, pc):
    offset = u64_to_i32(program[pc+1])
    return 'push', f'&var(0x{offset:02x})', pc+2

def push32(program, pc):
    value = u64_to_i32(program[pc+1])
    return 'push32', f'0x{value:x}', pc+2

def store32(program, pc):
    return 'store32', 'TOS ⇒ M[TOS1]', pc+1

def jmp(program, pc):
    rel = u64_to_i32(program[pc+1])
    return 'jmp', f'0x{(pc+1+rel):04x}', pc+2

def load_ptr(program, pc):
    arg = u64_to_i32(program[pc+1])
    match arg:
        case 0:
            return 'push', '&node_A', pc+2
        case 1:
            return 'push', '&node_B', pc+2
        case 2:
            return 'push', '&magic', pc+2
        case 3:
            return 'push', '&numbers', pc+2
        case 4:
            return 'push', '&zero', pc+2
        case _:
            raise ValueError(f'Unknown load_ptr argument {arg}')

def load64(program, pc):
    return 'load64', 'M[TOS] ⇒ TOS', pc+1

def setne(program, pc):
    return 'set', 'TOS1 != TOS', pc+1

def jnz(program, pc):
    rel = u64_to_i32(program[pc+1])
    return 'jtrue', f'0x{(pc+1+rel):04x}', pc+2

def load32(program, pc):
    return 'load32', 'M[TOS] ⇒ TOS', pc+1

def setlt(program, pc):
    return 'set', 'TOS1 < TOS', pc+1

def push64(program, pc):
    value = program[pc+1]
    return 'push64', f'0x{value:x}', pc+2

def mul(program, pc):
    return 'mul', 'TOS1 * TOS ⇒ TOS', pc+1

def add(program, pc):
    return 'add', 'TOS1 + TOS ⇒ TOS', pc+1

def nop(program, pc):
    return 'nop', '', pc+1

def sar(program, pc):
    return 'sar', 'TOS1 >> TOS ⇒ TOS', pc+1

def xor(program, pc):
    return 'xor', 'TOS1 ^ TOS ⇒ TOS', pc+1

def sub(program, pc):
    return 'sub', 'TOS1 - TOS ⇒ TOS', pc+1

def mod32(program, pc):
    return 'mod32', 'TOS % TOS1 ⇒ TOS', pc+1

def zext(program, pc):
    return 'zext', 'TOS ⇒ TOS', pc+1

def get_input(program, pc):
    arg = u64_to_i32(program[pc+1])
    if arg == 0:
        return 'push', '&input', pc+2
    raise ValueError('Unknown get_input argument')

def sext(program, pc):
    return 'sext', 'TOS ⇒ TOS', pc+1

def load8(program, pc):
    return 'load8', 'M[TOS] ⇒ TOS', pc+1

def store8(program, pc):
    return 'store8', 'TOS ⇒ M[TOS1]', pc+1

def idfk(program, pc):
    arg = u64_to_i32(program[pc+1])
    match arg:
        case 1:
            return 'sbox', 'var(0x11) = F_0c66f(var(0x10))', pc+2
        case 2:
            return 'strncpy', '(*var(0x14), *var(0x22), 5)', pc+2
        case 3:
            return 'strtol', '(*var(0x2c), 0, 10) ⇒ var(0x48)', pc+2
        case 4:
            return 'srand', '(*var(0x54))', pc+2
        case 5:
            return 'rand', '⇒ var(0x60)', pc+2
        case _:
            return 'syscall', f'{arg}, unsure', pc+2

def broken(program, pc):
    return '??', 'this one does not disassemble properly', pc+2

def store64(program, pc):
    return 'store64', 'TOS1 ⇒ M[TOS]', pc+1

def resize8(program, pc):
    return 'resize8', 'TOS & 0xff ⇒ TOS', pc+1

def store32_inv(program, pc):
    return 'store32', 'TOS1 ⇒ M[TOS]', pc+1

def push8(program, pc):
    value = program[pc+1] & 0xff
    return 'push8', f'0x{value:x}', pc+2

def seteq(program, pc):
    return 'set', 'TOS1 == TOS', pc+1

def shl(program, pc):
    return 'shl', 'TOS << TOS1 ⇒ TOS', pc+1

def and_(program, pc):
    return 'and', 'TOS & TOS1 ⇒ TOS', pc+1

def or_(program, pc):
    return 'or', 'TOS | TOS1 ⇒ TOS', pc+1

def ret(program, pc):
    return 'ret', 'TOS', pc+1

opcodes = {
    0x12e307: var,
    0x127de9: push32,
    0x123950: store32,
    0x1204f4: jmp,
    0x12f4c5: load_ptr,
    0x12c6f5: load64,
    0x13660c: setne,
    0x129ec6: jnz,
    0x1206c6: load32,
    0x12d2b3: setlt,
    0x122291: push64,
    0x124d28: mul,
    0x12a5b5: push64,
    0x130708: add,
    0x13513c: add,
    0x12ea5b: load32,
    0x1229af: load64,
    0x135d23: add,
    0x122136: nop,
    0x1298d0: push64,
    0x135fc4: sar,
    0x11f318: xor,
    0x137929: sub,
    0x12bbc2: nop,
    0x12ff28: mod32,
    0x1214a8: mul,
    0x127fce: add,
    0x12e1ff: zext,
    0x13303d: mod32,
    0x12c950: setne,
    0x13222d: get_input,
    0x12ba08: sext,
    0x11e9b3: add,
    0x11f702: load8,
    0x130e7a: store8,
    0x12d628: idfk,
    0x131b7b: add,
    0x1205bb: broken,
    0x12d50b: nop,
    0x11fb61: store64,
    0x12476f: resize8,
    0x126c2a: sext,
    0x12c850: load64,
    0x123763: store64,
    0x1311e8: nop,
    0x121347: nop,
    0x131422: store32_inv,
    0x120ad1: resize8,
    0x137531: zext,
    0x121cac: sext,
    0x12ab3f: xor,
    0x1245bf: store8,
    0x1248d4: push8,
    0x12f0ac: seteq,
    0x12fbea: load8,
    0x129449: setne,
    0x134e01: shl,
    0x1273ec: and_,
    0x133acd: sub,
    0x126d42: seteq,
    0x125c0f: or_,
    0x134b35: add,
    0x122ac9: xor,
    0x13875d: and_,
    0x132579: or_,
    0x1210ee: xor,
    0x12873a: setne,
    0x1347bc: ret,
}

pc = 0
while pc < len(program):
    cur_pc = pc
    opcode = program[pc]
    if opcode not in opcodes:
        raise ValueError(f'Unknown opcode 0x{opcode:x}')
    op, disasm, pc = opcodes[opcode](program, pc)
    print(f'0x{cur_pc:04x}: {op:10s}{disasm}')
```

once you get this disassembly now, the writeup guy insinuated these points from it : 
- An sbox is applied to user input thrice.
- first four characters that go through the above are converted from string to long, then used as seed on srand
- then there is a loop that xor's the output of step 1 with this rand() that was srandded with the thing in step 2
- then a check happens to see if the result we got now is equal to a bytearray stored in memory. If yes, flag mil gaya

So To reverse the above steps you had to :
- create an INVERSE sbox. `sbox_inv = {c: i for i, c in enumerate(sbox)}`
- xor the rand() result you get when the correct srand is set ( i still don't know how he got that, can't figure it out ) with the target bytearray that's in mem
- inverse sbox the thing 3 times, and u get the password

sending this password to the nc gives flag.

this was the final solve script to get the password \
by the writeup guy
```python
sbox = [0x0,0x78,0xec,0x8e,0x76,0x2c,0x10,0x30,0xad,0x26,0xc5,0xf3,0xc9,0x68,0xf9,0xbc,0x7c,0x42,0xd6,0x61,0xba,0x8d,0x51,0xf0,0x7e,0x58,0xa1,0xca,0x2,0x3e,0x6b,0xd8,0x38,0x6a,0x44,0x66,0xa2,0xa7,0x85,0xa0,0x9,0x8f,0x7d,0x1d,0xe0,0xa8,0x17,0x9e,0x31,0xd7,0xbd,0x5a,0x84,0x23,0xe7,0x4c,0xb9,0x99,0x7b,0xa9,0x71,0xf6,0xcf,0x3c,0x62,0xef,0xe5,0x3d,0xf4,0xea,0x19,0xb5,0xfb,0xe1,0x56,0x55,0xd5,0x2a,0x5d,0xed,0x29,0x65,0x6c,0x96,0x4d,0x9b,0x28,0xc7,0x47,0xb2,0x43,0x6e,0x20,0xe9,0xa3,0x95,0xce,0xb4,0x8b,0xac,0x82,0xbb,0xb0,0x93,0xd3,0x3a,0x69,0xbf,0x33,0xe2,0xc4,0x25,0x9c,0x37,0xf2,0x35,0xe6,0xeb,0xe4,0x24,0x88,0x5b,0xfe,0xd1,0x89,0x8a,0x52,0xcd,0x5f,0x46,0x27,0x4e,0x53,0x72,0x91,0x8,0xa,0x67,0x6,0x18,0x50,0x79,0x49,0xaf,0x7a,0x48,0xb3,0xae,0x80,0xcb,0x9d,0x12,0x77,0xda,0xf8,0x4,0xc0,0x74,0x3b,0xc3,0x45,0x1,0xc2,0xe,0x1f,0xf,0x81,0xe8,0x15,0x86,0xd2,0xaa,0xd9,0x59,0xab,0x14,0xc8,0xbe,0x73,0x2f,0xdd,0xff,0xfc,0x4b,0x2d,0xb8,0x57,0x1c,0x6d,0x2e,0xdc,0xf7,0xdb,0x36,0x64,0x70,0xb7,0x3f,0x1e,0x54,0x4f,0x60,0x34,0xf5,0x92,0xd,0x13,0xee,0x9a,0x6f,0x94,0xfa,0x8c,0x97,0x1b,0xfd,0x2b,0x1a,0x9f,0x22,0xcc,0x21,0xde,0x4a,0xb6,0xb1,0x39,0x3,0x98,0x87,0xdf,0xa6,0xd0,0x75,0x5c,0xc1,0x11,0xe3,0x40,0x7f,0xf1,0xd4,0xa5,0x7,0xc,0x5e,0x5,0xc6,0x32,0x16,0xb,0x41,0x83,0x90,0xa4,0x63]
sbox_inv = {c: i for i, c in enumerate(sbox)}
def undo(s):
    return bytes(sbox_inv[c] for c in s)

target = bytes.fromhex('a5cdffe4e96ffa54bec68713fd6bf980c454e46f58d52335adcc21f593620cad5a320d')
rand   = bytes.fromhex('67c6697351ff4aec29cdbaabf2fbe3467cc254f81be8e78d765a2e63339fc99a66320d')
bruh = bytes(a ^ b for a, b in zip(target, rand))
for _ in range(3):
    bruh = undo(bruh)

with open('input', 'wb') as f:
    f.write(bruh)
```

## takeaways :

this was way beyond my current level. I could never have traced the instructions, and created a disassembler accordingly. (maybe done it partially, but it still would've not been accurate)

- should've gone deeper when we found the function filled with the bytes for the opcodes.
- need to get better. more grind needed.
