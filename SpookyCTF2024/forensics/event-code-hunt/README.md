# event-code-hunt
> Maya Elmer managed to seize one of The Consortium’s computers, but when she tried to access a critical file, a sudden blue box flashed across her screen, and the file was instantly encrypted. Now, with the clock ticking, participants must step in to decrypt the file and uncover the hidden contents. The Consortium's encryption is tough to crack, and only the most determined will succeed in revealing the secrets locked away within.

In this challenge, we are given a Windows Event Viewer logs and an encrypted flag. Most of the logs don't contain any useful information, besides standard Windows stuff. Log file `PowershellOP`, however, contains a Python source code and a command used to run it:

```
Creating Scriptblock text (1 of 1):
"import sys`n`ndef process_data(input_bytes, key):`n    key_bytes = key.encode('utf-8')`n    return bytearray([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(input_bytes)])`n`ndef main():`n    if len(sys.argv) != 4:`n        print('Usage: python script.py <input_file> <output_file> <key>')`n        return`n    input_file = sys.argv[1]`n    output_file = sys.argv[2]`n    key = sys.argv[3]`n`n    with open(input_file, 'rb') as f:`n        input_data = f.read()`n`n    result_data = process_data(input_data, key)`n`n    with open(output_file, 'wb') as f:`n        f.write(result_data)`n`nif __name__ == '__main__':`n    main()" | Set-Content -Path "C:\Users\johndoe\Documents\Chrome.py"; Get-Content "C:\Users\johndoe\Documents\Chrome.py"


ScriptBlock ID: 0cc776b3-1118-4a90-8b1f-b31fe6d43bac
Path: 
```

```
python3 .\Documents\Chrome.py .\Documents\flag.txt .\Documents\encrypt_flag.txt I_Like_Big_Bytes_And_I_cannot_Lie!
```

Cleaned up script:

```py
import sys

def process_data(input_bytes, key):
    key_bytes = key.encode('utf-8')
    return bytearray([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(input_bytes)])

def main():
    if len(sys.argv) != 4:
        print('Usage: python script.py <input_file> <output_file> <key>')
        return
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    key = sys.argv[3]

    with open(input_file, 'rb') as f:
        input_data = f.read()

    result_data = process_data(input_data, key)

    with open(output_file, 'wb') as f:
        f.write(result_data)

if __name__ == '__main__':
    main()
```

In the `process_data` function, the part `bytearray([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(input_bytes)])` indicates that this is some sort of XOR cipher. We already know that the script was ran with a key `I_Like_Big_Bytes_And_I_cannot_Lie!`, so just running the script and providing the encrypted flag as input, alongside the key, we can obtain the final answer.

`NICC{Maya_Elmer_D3t3cts_Mal1c10us_P4yl04d_1n_3v3ntL0gs}`