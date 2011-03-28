#!/usr/bin/python
import sys
import chardet
fin = open(sys.argv[1])
print chardet.detect(fin.readline())
