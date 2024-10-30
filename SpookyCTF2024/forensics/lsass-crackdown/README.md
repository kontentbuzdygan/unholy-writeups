# lsass-crackdown

> Anna Circoh has intercepted a highly sensitive memory dump, but The Consortium has fortified it with advanced encryption, hiding their deepest secrets within. Participants must analyze the data and navigate through layers of defenses to find a key piece of information we are thinking its a leaked password. Dr. Tom Lei has rigged the memory with decoys and traps, so tread carefully—one wrong step could lead you down a path of misdirection. 

> Some AV's may detect the attachment as malicious. This is a false positive and can be ignored

We are given a Windows dump file. Opening it in Windbg and running `analyze -v` shows that a faulty module was `lsass.exe`. Quick Google search explained that lsass is reponsible for user authentication. I decided to look for vulnerabilities/info dumping techniques and I stumbled upon a tool called Mimikatz. Running it with commands `sekurlsa::minidump dump.DMP` and `sekurlsa::logonPasswords full` outputs NTLM hash of two users:

```
[00000003] Primary
* Username : Consortium
* Domain   : DESKTOP-UBFFHS2
* NTLM     : f6c479f4b9904f884fede1b2d4328d98
* SHA1     : 8e0cf85ff4c266ff4ef626580cce1ff025118c6f
* DPAPI    : 8e0cf85ff4c266ff4ef626580cce1ff0

[00000003] Primary
* Username : johndoe
* Domain   : .
* NTLM     : bbf53d134077fc615eac56ccddb8b7b3
* SHA1     : 322dfdd498b4441e023bb01daa343bf820a06210
* DPAPI    : 322dfdd498b4441e023bb01daa343bf8
```

Cracking the hashes in [crackstation.net](https://crackstation.net) gives following strings:
```
1987evilovekoen
johndoe
```

Not having anything left to do, I wrapped the first string in flag format, which turned out to be an answer.

`NICC{1987evilovekoen}`