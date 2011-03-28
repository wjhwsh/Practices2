#!/usr/bin/python
import subprocess
for i in range(5, 8):
    yacc_file = "example"+str(i)+".y"
    lex_file = "example"+str(i)+".l"
    out_file = "example"+str(i)+".out"
    cmd1 = "yacc -d "+yacc_file   
    cmd2 = "lex "+lex_file  
    cmd3 = "cc -o "+out_file+" y.tab.c lex.yy.c -ly -ll"
    print cmd1
    subprocess.call(cmd1, shell=True)
    print cmd2
    subprocess.call(cmd2, shell=True)
    print cmd3
    subprocess.call(cmd3, shell=True)
