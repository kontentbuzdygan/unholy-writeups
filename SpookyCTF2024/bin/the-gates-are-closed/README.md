# the-gates-are-closed
> A USB drive was found in front of the locked gates of an abandoned cemetery. It may contain information regarding the strange sightings reported to nearby authorities in the graveyard, which NICC decided to investigate.

We are given a binary file which only prints `Nothing is going on here... :D` upon execution. Opening it in Ghidra and inspecting function names reveals a function `secretfunction`:

```c
void secretfunction(void)

{
  puts("TklDQ3s0X1IzNGxfRmw0Z30=");
  return;
}
```

Decoding the string from base64 outputs a flag.

`NICC{4_R34l_Fl4g}`