# my-assm-hurts
> As Mary was attempting to time travel, she slipped on a patch of ice and landed on her butt. While getting up from the ice, she found a cool-looking USB flash drive containing a file with some system code. Can you help Mary decrypt what information the file has?

> I am COOL in here, are you?

The attachment is some kind of assembly code. Based on the hint, a quick Google search led me to a language called COOL. First thing I did is open up the [reference manual](https://dijkstra.eecs.umich.edu/eecs483/cool-manual/cool-manual.html). Thankfully there is a section about the language's assembly langauge. I skimmed through it and noticed this sentence:

> The normal Cool compiler executable (e.g., cool.exe) also serves as a Cool CPU Simulator that executes Cool Assembly Language programs. 

That's handy. I decided to look for the compiler executable, which was a pain to find. Finally found it on [this website](https://web.eecs.umich.edu/~weimerw/2015-4610/cool.html). I renamed the attachement file to match the pattern expected by the compiler and tried to run it: `./cool --asm freezingprogram.cl-asm`.

```
ERROR: 199: Assembler: reference to undefined label the.empty.string
Best-Effort Backtrace:
```

There was an error on line 199 about `the.empty.string` being undefined. Line 199:

```
la r1 <- the.empty.string
```

I didn't really know where to get that from, so I decided to create a simple Hello World program and compare it's assembly.

```
class Main inherits IO { 
    main() : Object { 
        out_string("Hello, world.\n") 
    } ; 
} ;
```

```
...
                        ;; global string constants
the.empty.string:       constant ""
string1:                constant "Bool"
string2:                constant "IO"
string3:                constant "Int"
string4:                constant "Main"
string5:                constant "Object"
string6:                constant "String"
string7:                constant "abort\n"
string8:                constant "Hello, world.\n"
string9:                constant "ERROR: 0: Exception: String.substr out of range\n"
...
```

Looking at this section in the challenge program:

```
;; global string constants
;; ERROR
```

Copying the entire section from my dummy program to the challenge's resulted in another error:

```
ERROR: 424: Assembler: reference to undefined label string10
Best-Effort Backtrace:
```

Line 424:
```
;; string10 hols "I"
la r2 <- string10
```

This made me think that I have to look for all `string*` constants and fill them based on the comments:

```
the.empty.string:       constant ""
string1:                constant "Bool"
string2:                constant "IO"
string3:                constant "Int"
string4:                constant "Main"
string5:                constant "Object"
string6:                constant "String"
string7:                constant "abort\n"
string8:                constant "N"
string9:                constant "ERROR: 0: Exception: String.substr out of range\n"
string10:               constant "I"
string11:               constant ""
string12:               constant "C"
string13:               constant ""
string14:               constant ""
string15:               constant "{"
string16:               constant ""
string17:               constant "h"
string18:               constant ""
string19:               constant "E"
string20:               constant ""
string21:               constant "y"
string22:               constant ""
string23:               constant "_"
string24:               constant ""
string25:               constant "t"
string26:               constant "h"
string27:               constant ""
string28:               constant "1"
string29:               constant ""
string30:               constant "s"
string31:               constant ""
string32:               constant "-"
string33:               constant ""
string34:               constant "i"
string35:               constant ""
string36:               constant "s"
string37:               constant ""
string38:               constant ""
string39:               constant "o"
string40:               constant ""
string41:               constant "0"
string42:               constant ""
string43:               constant "L"
string44:               constant ""
string45:               constant "}"
string46:               constant ""
string47:               constant ""
```

Now the executable prints out the flag.

`NICC{hEy_th1s-is_Co0L}`