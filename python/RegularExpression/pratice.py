#!/usr/bin/python

import re
f = open('test.log')
for i in f:
    regex = re.search(r'Invalid user ([^ ]+) from ([^ ]+)', i)
    if regex:
        print regex.group(1) + " => " + regex.group(2),
f.close()

