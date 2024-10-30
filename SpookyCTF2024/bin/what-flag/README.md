# what-flag
> NICC recieved a mysterious email with an executable file that does nothing. Can you figure out what this executable does?

Running the binary does nothing and decompiling the `main` function in Ghidra confirms it:

```c
undefined8 main(void)

{
  return 0;
}
```

Looking at the available functions, there are a few named `a`, `f`, `g`, `h`, `h2`, `l`, `u`. This didn't make any sense to me at first, so I decided to look at the `a` function first:

```c
void a(void)

{
  long in_FS_OFFSET;
  
  if (*(long *)(in_FS_OFFSET + 0x28) != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

The decompiled version didn't really say anything so I decided to look at the assembly code:

```asm
                             **************************************************************
                             *                          FUNCTION                          *
                             **************************************************************
                             undefined a()
             undefined         AL:1           <RETURN>
             undefined8        Stack[-0x10]:8 local_10                                XREF[2]:     0010127d(W), 
                                                                                                   0010128a(R)  
             undefined2        Stack[-0x12]:2 local_12                                XREF[1]:     00101283(W)  
                             a                                               XREF[3]:     Entry Point(*), 00102058, 
                                                                                          001021a0(*)  
        00101268 f3 0f 1e fa     ENDBR64
        0010126c 55              PUSH       RBP
        0010126d 48 89 e5        MOV        RBP,RSP
        00101270 48 83 ec 10     SUB        RSP,0x10
        00101274 64 48 8b        MOV        RAX,qword ptr FS:[0x28]
                 04 25 28 
                 00 00 00
        0010127d 48 89 45 f8     MOV        qword ptr [RBP + local_10],RAX
        00101281 31 c0           XOR        EAX,EAX
        00101283 66 c7 45        MOV        word ptr [RBP + local_12],0x695f
                 f6 5f 69
        00101289 90              NOP
        0010128a 48 8b 45 f8     MOV        RAX,qword ptr [RBP + local_10]
        0010128e 64 48 2b        SUB        RAX,qword ptr FS:[0x28]
                 04 25 28 
                 00 00 00
        00101297 74 05           JZ         LAB_0010129e
        00101299 e8 b2 fd        CALL       <EXTERNAL>::__stack_chk_fail                     undefined __stack_chk_fail()
                 ff ff
                             -- Flow Override: CALL_RETURN (CALL_TERMINATOR)
                             LAB_0010129e                                    XREF[1]:     00101297(j)  
        0010129e c9              LEAVE
        0010129f c3              RET
```

The part `MOV word ptr [RBP + local_12],0x695f` is interesting. The other functions share the pattern of empty decompiled function and moving some bytes around. Gathering all those bytes into one place resulted in following hex string:

```
5f697568485f5468496e6b7d43437b5f666c40674e49
```

Translates into:
```
_iuhH_ThInk}CC{_fl@gNI
```

This is a flag, but scrambled. Looking at the functions again, the `u`, `h`, and `h2` functions contain the `NICC{` part. Being left with `a`, `f`, `g` and `l`, I guessed that the combination will be `uhh flag`, which turned out to be the answer.

```
NICC{uhH_fl@g_i_ThInk}
```