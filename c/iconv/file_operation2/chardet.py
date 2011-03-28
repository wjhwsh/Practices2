#!/usr/bin/python
import chardet
import sys
import getopt

def main():
    print "hello"
    input_file = sys.argv[1]
    fin = open(str(input_file))
    print chardet.detect(fin.readline())        

if __name__ == "__main__":
    main()

