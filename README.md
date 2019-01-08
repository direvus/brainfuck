# brainfuck
A [Brainfuck](https://en.wikipedia.org/wiki/Brainfuck) library in Python 2.

## Usage

```
brainfuck.py [program]
```

E.g.:

```
brainfuck.py "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
```

```
Hello World!
```

## Module contents

The `brainfuck` module provides one class `BrainfuckMemory`, to simulate an infinite(ish) byte array for program memory.

It also provides a pure function `execute` to parse and run an arbitrary Brainfuck program.
