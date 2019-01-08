#!/usr/bin/python
# vim:encoding=utf-8
"""brainfuck.py is a Python2 library for the Brainfuck language.

Usage: brainfuck.py [program]

E.g., brainfuck.py "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
Hello World!
"""
import sys


class BrainfuckMemory(object):
    """A class implementing a Brainfuck machine memory.
    
    A theoretical Brainfuck machine has an infinitely long array of single-byte
    data cells, all of which are initialised to zero when the program begins
    execution.  This class emulates this memory model, up to the limit for
    Python byte arrays.

    Rather than selecting an arbitrary fixed size, this memory will grow as
    needed to accommodate the indexes that are assigned to it.  Any attempt to
    assign to an index which does not yet exist will grow the list.  Any
    attempt to read from an index which does not exist will return zero.
    """
    def __init__(self):
        self.store = bytearray()

    def __getitem__(self, key):
        try:
            return self.store[key]
        except IndexError:
            return 0

    def __setitem__(self, key, value):
        try:
            self.store[key] = value
        except IndexError:
            pad = key - len(self.store)
            self.store = bytearray(list(self.store) + (pad * [0]) + [value])


def execute(program, data=None, instream=None, outstream=None):
    """Execute a Brainfuck program.
    
    If 'data' is provided, it should behave as a mutable sequence of integers
    in the range 0-255.  If 'data' is None, a new BrainfuckMemory object will
    be created to contain the program's runtime memory.

    The 'instream' and 'outstream' arguments should be readable and writable
    file-like objects, respectively.  If they are None, they will default to
    sys.stdin and sys.stdout, respectively.

    Raise a ValueError if the program is found to be invalid.
    """
    if data is None:
        data = BrainfuckMemory()
    if instream is None:
        instream = sys.stdin
    if outstream is None:
        outstream = sys.stdout

    dp = 0 # data pointer
    ip = 0 # instruction pointer
    forward = {}
    backward = {}

    # Parse the program, check for correctness and map out the jump
    # positions for easy reference later on.
    jumps = []
    for k, v in enumerate(program):
        if v == '[':
            jumps.append(k)
        elif v == ']':
            if len(jumps) < 1:
                raise ValueError("Invalid program: unmatched ']' at position {}".format(k))
            jump = jumps.pop()
            forward[jump] = k
            backward[k] = jump
    if len(jumps) > 0:
        raise ValueError("Not all '[' matched by ']' at end of program.")

    while ip < len(program):
        ins = program[ip]
        if ins == '>':
            # Increment the data pointer.
            dp += 1
        elif ins == '<':
            # Decrement the data pointer.
            dp -= 1
        elif ins == '+':
            # Increment the instruction pointer.
            value = data[dp] + 1
            if value > 255:
                value = 0
            data[dp] = value
        elif ins == '-':
            # Decrement the instruction pointer.
            value = data[dp] - 1
            if value < 0:
                value = 255
            data[dp] = value
        elif ins == '.':
            # Output the byte pointed to by the data pointer to stdout.
            outstream.write(chr(data[dp]))
        elif ins == ',':
            # Input a byte from stdin, to the cell pointed to by the data
            # pointer.
            data[dp] = ord(instream.read(1))
        elif ins == '[':
            # Jump forward past the matching ']', if the byte pointed to by the
            # data pointer is zero.
            if data[dp] == 0:
                ip = forward[ip]
        elif ins == ']':
            # Jump backward to the matching '['.
            ip = backward[ip] - 1
        ip += 1


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print __doc__
        sys.exit(1)
    execute(sys.argv[1])

