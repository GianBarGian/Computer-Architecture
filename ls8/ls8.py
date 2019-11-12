#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

if len(sys.argv) != 2:
    print("usage: 02-fileio02.py <filename>")
    sys.exit(1)

try:
    with open(sys.argv[1]) as f:
        for line in f:
            # deal with comments
            # split before and after any comment symbol '#'
            comment_split = line.split("#")

            # convert the pre-comment portion (to the left) from binary to a value
            # extract the first part of the split to a number variable
            # and trim whitespace
            num = comment_split[0].strip()

            # ignore blank lines / comment only lines
            if len(num) == 0:
                continue

            # set the number to an integer of base 2
            value = int(num, 2)
            # print the value in binary and in decimal
            cpu.load(value)
        cpu.reset_address()
    cpu.run()
except FileNotFoundError:
    print(f"{sys.argv[0]}: {sys.argv[1]} not found")
    sys.exit(2)



