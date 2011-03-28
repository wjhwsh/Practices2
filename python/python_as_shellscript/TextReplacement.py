#!/usr/bin/python
import os, sys
usage = "usage: %s search_text replace_text [infile [outfile]]" %         os.path.basename(sys.argv[0])

if len(sys.argv) < 3:
    print usage
else:
    stext = sys.argv[1]
    rtext = sys.argv[2]
    input = sys.stdin
    output = sys.stdout
    if len(sys.argv) > 3:
        input = open(sys.argv[3])
    if len(sys.argv) > 4:
        output = open(sys.argv[4], 'w')
    for s in input.xreadlines():
        if s.find('Report Version:  103') != -1:
            print 'report'
            output.write(s.replace('Report Version:  103', 'Report Version:  104'))
        elif s.find('??? (???)'):
            print '??'
            output.write(s.replace('??? (???)', 'armv7'))
