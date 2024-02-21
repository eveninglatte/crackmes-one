
###  crackme id: 6513567328b5870bef263329
### BEST VIEWED THRU VSCODE OR OTHER MARKDOWN READER

# The thought process
The crackme listing specifies the crackme executable as an [ELF][elf-wikipedia] (which usually indicates it's a Linux executable, [unless you're solving crackmes designed for a Playstation][elf-wikipedia-playstation]) We can check it with the `file` command if we'd feel the need to confirm this.
Let's see how it behaves by executing it:

![](<assets\1.png>)

I started by creating a new project in Ghidra (the lazy route I know, but I want to get to know Ghidra better), importing the executable `plain_sight` and letting Ghidra analyse it:

![](<assets\2.png>)

Seems like Ghidra was able to find the `main()` function, and we even have some debug symbols left in the binary!

Here's a look at the `Login()` function:

![](<assets\3.png>)

Seems like this function prints out the string `"Enter the password: "` and stores the user's input in a variable called `local_38`:
```cpp
// call to the << operator of cout
// cout << "Enter the password: "
std::operator<<((basic_ostream *)std::cout,"Enter the password: ");
// call to the >> operator of cin
// cin >> local_38
std::operator>>((basic_istream *)std::cin,local_38);
```

`local_38` can be renamed to something easier on the eyes, like `password`, given how it looks like this input is meant to be a password provided by the user.

Next, it can be seen that `bVar1` of `bool` type stores the result of a comparison between two strings: `password` and a literal, `"do_not_hardcode"`. 
Then, if  `bVar1` is true, the program prints out `"Welcome"`, with `"Wrong password!"` being printed otherwise.

Looks like the password was found! Let's try it out:

![](assets\4.png)

Thus, the crackme is completed.

# Notes
This challenge could be completes in a number of other ways, such as:
- by using `strings` to check for any string literals in the executable and noticing that `"Enter the password"`, `"do_not_hardcode"`, `"Welcome"` and `"Wrong password!"` come one after the other
- by checking the contents of `.rodata` section, which holds read-only data (such as constants or string literals used in the program), and noticing that the four aforementioned strings are the only data being held in this segment

[elf-wikipedia]: https://en.wikipedia.org/wiki/Executable_and_Linkable_Format
[elf-wikipedia-playstation]: https://en.wikipedia.org/wiki/Executable_and_Linkable_Format#Game_consoles