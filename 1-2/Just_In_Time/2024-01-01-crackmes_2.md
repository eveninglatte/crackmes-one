### crackme id: 63c4ee1a33c5d43ab4ecf49a
### BEST VIEWED THRU VSCODE OR OTHER MARKDOWN READER

# The thought process
The binary in need of cracking is called `ski000`, let's execute it:

![](<assets/1.png>)

I started by importing the file to Ghidra and letting it analyse it:

![](<assets/2.png>)

Here is the entry point. `__libc_start_main()` function is an initialisation routine responsible for executing the `main()` function, so `FUN_00101422` must be `main()`.
After jumping to that function and renaming it appropriately, we are left with this chunk of code:

```cpp
undefined8 main(void)
{
  int iVar1;
  size_t sVar2;
  ulong uVar3;
  undefined8 local_a8;
  undefined8 local_a0;
  undefined8 local_98;
  undefined8 local_90;
  undefined2 local_88;
  undefined8 local_58;
  undefined8 local_50;
  undefined4 local_48;
  time_t local_40;
  undefined local_38 [24];
  int local_20;
  int local_1c;
  
  time(&local_40);
  DAT_00104070 = localtime(&local_40);
  FUN_0010138a(local_38);
  iVar1 = FUN_001011ba(local_38);
  if ((iVar1 == 0) && (iVar1 = FUN_00101189(local_38), iVar1 == 0)) {
    local_a8 = 0x4af2d0d4eeeee890;
    local_a0 = 0xd2eee8f8f0f0ccea;
    local_98 = 0xeed8e6e8904a4a66;
    local_90 = 0xe8dcf2cce2f4f2cc;
    local_88 = 0x4ce6;
    for (local_1c = 0; uVar3 = (ulong)local_1c, sVar2 = strlen((char *)&local_a8), uVar3 < sVar2;
        local_1c = local_1c + 1) {
      putchar((*(byte *)((long)&local_a8 + (long)local_1c) >> 1) - 5);
    }
  }
  else {
    local_58 = 0xd0d4eeeee8d0e69c;
    local_50 = 0xe8f8f0f0ccea4af2;
    local_48 = 0x66d2ee;
    for (local_20 = 0; uVar3 = (ulong)local_20, sVar2 = strlen((char *)&local_58), uVar3 < sVar2;
        local_20 = local_20 + 1) {
      putchar((*(byte *)((long)&local_58 + (long)local_20) >> 1) - 5);
    }
  }
  return 0;
}
```

Looks intimidating. 
I started by figuring out which of the initialised variables are actually used and renamed them, just to set them apart from the rest:

```cpp
undefined8 main(void)
{
  // this variable is used to store some return value, hence the name
  int retval;
  // same with this one
  size_t size;
  ulong uVar1;
  undefined8 some_var;
  undefined8 local_a0;
  undefined8 local_98;
  undefined8 local_90;
  undefined2 local_88;
  undefined8 some_var2;
  undefined8 local_50;
  undefined4 local_48;
  // here Ghidra found a variable type, let's rename it accordingly
  time_t cur_time;
  undefined tab [24];
  // these seem to be used as loop iterators, so let's rename them as such
  int j;
  int i;
  
  time(&cur_time);
  ptr_local_time = localtime(&cur_time);
  FUN_0010138a(tab);
  retval = FUN_001011ba(tab);
  if ((retval == 0) && (retval = FUN_00101189(tab), retval == 0)) {
    some_var = 0x4af2d0d4eeeee890;
    local_a0 = 0xd2eee8f8f0f0ccea;
    local_98 = 0xeed8e6e8904a4a66;
    local_90 = 0xe8dcf2cce2f4f2cc;
    local_88 = 0x4ce6;
    for (i = 0; uVar1 = (ulong)i, size = strlen((char *)&some_var), uVar1 < size; i = i + 1) {
      putchar((*(byte *)((long)&some_var + (long)i) >> 1) - 5);
    }
  }
  else {
    some_var2 = 0xd0d4eeeee8d0e69c;
    local_50 = 0xe8f8f0f0ccea4af2;
    local_48 = 0x66d2ee;
    for (j = 0; uVar1 = (ulong)j, size = strlen((char *)&some_var2), uVar1 < size; j = j + 1) {
      putchar((*(byte *)((long)&some_var2 + (long)j) >> 1) - 5);
    }
  }
  return 0;
}
```

Let's also get rid of the variables that aren't being used:

```cpp
undefined8 main(void)
{
  int retval;
  size_t size;
  ulong uVar1;
  undefined8 some_var;
  undefined8 some_var2;
  time_t cur_time;
  undefined tab [24];
  int j;
  int i;
  
  time(&cur_time);
  ptr_local_time = localtime(&cur_time);
  FUN_0010138a(tab);
  retval = FUN_001011ba(tab);
  if ((retval == 0) && (retval = FUN_00101189(tab), retval == 0)) {
    some_var = 0x4af2d0d4eeeee890;
    for (i = 0; uVar1 = (ulong)i, size = strlen((char *)&some_var), uVar1 < size; i = i + 1) {
      putchar((*(byte *)((long)&some_var + (long)i) >> 1) - 5);
    }
  }
  else {
    some_var2 = 0xd0d4eeeee8d0e69c;
    for (j = 0; uVar1 = (ulong)j, size = strlen((char *)&some_var2), uVar1 < size; j = j + 1) {
      putchar((*(byte *)((long)&some_var2 + (long)j) >> 1) - 5);
    }
  }
  return 0;
}
```

Okay, looks a bit more manageable. Now, I tried to analyse the output line by line.

The first lines grab the current time and tranform the output from type `time_t` to type `tm`, then the program calls two functions and saves the return value of the second one. Then, it compares this return value and the return value of the other, third function (this one is called directly in the if statement's condition parentheses) - if they are both 0, it does something, and if they aren't, it does something else.

First things first. Here's the first function that's being called `FUN_0010138a(tab)`:

```cpp
void FUN_0010138a(char *param_1)
{
  size_t sVar1;
  char *pcVar2;
  ulong uVar3;
  undefined8 local_38;
  undefined8 local_30;
  undefined local_28;
  int local_1c;
  
  local_38 = 0xccea4aeed4f2e694;
  local_30 = 0x4a7ed2eee8f8f0f0;
  local_28 = 0;
  local_1c = 0;
  while (true) {
    uVar3 = (ulong)local_1c;
    sVar1 = strlen((char *)&local_38);
    if (sVar1 <= uVar3) break;
    putchar((*(byte *)((long)&local_38 + (long)local_1c) >> 1) - 5);
    local_1c = local_1c + 1;
  }
  pcVar2 = fgets(param_1,0x18,stdin);
  if (pcVar2 == (char *)0x0) {
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  return;
}
```

It accepts a `char *` as a parameter - we can therefore deduce that `tab` in the `main()` function is a `char *`.

I applied a similar "deobfuscation" treatment to this function:

```cpp
// since the parameter is being used in the fgets() call later, we can name it input
void FUN_0010138a(char *input)
{
  size_t size;
  char *ptr_str;
  ulong uVar1;
  undefined8 some_str;
  int i;
  
  some_str = 0xccea4aeed4f2e694;
  i = 0;
  while (true) {
    uVar1 = (ulong)i;
    size = strlen((char *)&some_str);
    if (size <= uVar1) break;
    putchar((*(byte *)((long)&some_str + (long)i) >> 1) - 5);
    i = i + 1;
  }
  // set equate from hex to decimal, 0x18 = 24
  str = fgets(input, 24, stdin);
  // set equate from 0x0 to NULL, given this is what fgets() could return
  if (str == (char *)NULL) {
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  return;
}
```

This function seems to take the value saved in `some_str` variable, transforms it somehow and prints it out using the `putchar()` function. Then, it seems to collect the input from `stdin` using `fgets()` with a maximum number of characters read value of 24.

Even without deciphering curious method of printing being employed, it seems that this function prompts the user for input, then collects it. I renamed it as such in the `main()` function:

```cpp
undefined8 main(void)
{
  int retval;
  size_t size;
  ulong uVar1;
  undefined8 some_var;
  undefined8 some_var2;
  time_t cur_time;
  undefined tab [24];
  int j;
  int i;
  
  time(&cur_time);
  ptr_local_time = localtime(&cur_time);
  prompt_for_input(tab);
  retval = FUN_001011ba(tab);
  if ((retval == 0) && (retval = FUN_00101189(tab), retval == 0)) {
    some_var = 0x4af2d0d4eeeee890;
    for (i = 0; uVar1 = (ulong)i, size = strlen((char *)&some_var), uVar1 < size; i = i + 1) {
      putchar((*(byte *)((long)&some_var + (long)i) >> 1) - 5);
    }
  }
  else {
    some_var2 = 0xd0d4eeeee8d0e69c;
    for (j = 0; uVar1 = (ulong)j, size = strlen((char *)&some_var2), uVar1 < size; j = j + 1) {
      putchar((*(byte *)((long)&some_var2 + (long)j) >> 1) - 5);
    }
  }
  return 0;
}
```

Moving on to the next function called, `FUN_001011ba(tab)`:

undefined4 FUN_001011ba(char *param_1)

```cpp
undefined4 FUN_001011ba(char *param_1)
{
  undefined4 uVar1;
  byte bVar2;
  
  if (((((param_1[3] == 'k') && (((int)param_1[0xb] & 0x3fffffffU) == 0x31)) &&
       (((int)param_1[5] & 0x3fffffffU) == 0x39)) &&
      ((((param_1[0xc] == 'F' &&
         (bVar2 = (byte)((*ptr_local_time % 10) % 3), (int)param_1[7] << (bVar2 & 0x1f) == 0xf6)) &&
        (((int)param_1[1] << (bVar2 & 0x1f) == 200 &&
         (((int)param_1[0xd] << (bVar2 & 0x1f) == 0x68 && (((int)param_1[8] & 0x3fffffffU) == 0x2e))
         )))) && (*param_1 == '%')))) &&
     (((((int)param_1[2] << (bVar2 & 0x1f) == 0xd4 && (param_1[9] == 'f')) && (param_1[6] == '^'))
      && (((int)param_1[10] << (bVar2 & 0x1f) == 0x80 && ((int)param_1[4] << (bVar2 & 0x1f) == 0x50)
          ))))) {
    uVar1 = 0;
  }
  else {
    uVar1 = 1;
  }
  return uVar1;
}
```

This one is a fine candidate to deobsfucate too, but even now it's clear that it's a checklist of some sort, and given it's being passed the `input` variable it's probably the function that checks the password's correctness.

After applying some *Set equate* and *Rename Variable*:

```cpp
undefined4 FUN_001011ba(char *input)
{
  undefined4 retval;
  // even though it doesn't make much sense to change the name like that, it's easier on the eyes for me
  byte some_byte;
  
  if (((((input[3] == 'k') && (((int)input[11] & 0x3fffffffU) == 49)) &&
       (((int)input[5] & 0x3fffffffU) == 57)) &&
      ((((input[12] == 'F' &&
      // some_byte is being assigned, but Ghidra didn't realise that ptr_local_time is a tm * type
         (some_byte = (byte)((*ptr_local_time % 10) % 3), (int)input[7] << (some_byte & 31) == 246))
        && (((int)input[1] << (some_byte & 31) == 200 &&
            (((int)input[13] << (some_byte & 31) == 104 && (((int)input[8] & 0x3fffffffU) == 46)))))
        ) && (*input == '%')))) &&
     (((((int)input[2] << (some_byte & 31) == 212 && (input[9] == 'f')) && (input[6] == '^')) &&
      (((int)input[10] << (some_byte & 31) == 128 && ((int)input[4] << (some_byte & 31) == 80))))))
  {
    retval = 0;
  }
  else {
    retval = 1;
  }
  return retval;
}
```

Okay, if all these checks pass, `retval` is being assigned 0 - this seems to be the desired outcome, given that check in the `main()` function.

After retyping (*Right click -> Retype*) the `ptr_local_time` variable from `int *` to `tm *` in Ghidra we now know what value is being assigned to `some_byte`:
```cpp
some_byte = (byte)((ptr_local_time->tm_sec % 10) % 3)
```
It's the current number of seconds modulo 10 modulo 3 - so it equates **either 0, 1 or 2**, depending on the time the program is run. Clever!

I wrote down the checks and split them into simple, complicated and the ones using `some_byte` to make writing a keygen easier:

1. Simple:
- input[0] == '%'
- input[3] == 'k'
- input[6] == '^'
- input[9] == 'f'
- input[12] == 'F'

2. Complicated:
- (int)input[11] & 0x3fffffffU == 49
- (int)input[5] & 0x3fffffffU == 57
- (int)input[8] & 0x3fffffffU == 46

3. Using `some_byte`:
- (int)input[7] << (some_byte & 31) == 246
- (int)input[1] << (some_byte & 31) == 200
- (int)input[13] << (some_byte & 31) == 104
- (int)input[2] << (some_byte & 31) == 212
- (int)input[10] << (some_byte & 31) == 128
- (int)input[4] << (some_byte & 31) == 80

1st and 2nd ones seem manageable, and, after realising that `some_byte` can only equal either 0, 1 or 2 (and 31 is 0b11111, so AND'ing it with any number yields that number), 3rd one seems like it too.

One other thing to notice is that ASCII code ranges from 0 to 127, and:

1. subsituting 0 for `some_byte` means that some values in `input` are "supposed to" be higher than 127, 
2. subsituting 2 for `some_byte` means that some values in `input` are "supposed to" be non-integer (e.g. 104 isn't divisible by 4)

Therefore 1 is the only state in which all the tests are passed.
Obviously, one can try to run the keygen for all of the possible `some_byte` states and find that out empyrically (like, to be frank, I did).

Now it's possible to write a keygen script. I've divided it into 2 files (`keygen.cpp` and `init.sh`, I've attached them to the archive) for easier redirection of generated key to the crackme.