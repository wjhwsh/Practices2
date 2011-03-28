#!/usr/bin/python
import os, sys

input = sys.stdin
output = sys.stdout

input = open(sys.argv[1])
output = open(sys.argv[1] + '.ok', 'w')

for s in input.xreadlines():
    print s
    if s.find('Report Version:  103') != -1:
        output.write(s.replace('Report Version:  103', 'Report Version:  104'))
    elif s.find('??? (???)'):
        output.write(s.replace('??? (???)', 'armv7'))
