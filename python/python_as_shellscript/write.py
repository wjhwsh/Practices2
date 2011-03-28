#!/usr/bin/python
#-*- coding: utf-8 -*-
import subprocess
import codecs

linelist = []
fin = open("lab1_score.txt")
while(fin.readline() != ''):
    linelist.append(fin.readline().split())
fin.close()
del linelist[len(linelist)-6:len(linelist)-1]
#already initialized

pipe = subprocess.Popen('ls score*', shell=True, stdout=subprocess.PIPE).stdout
namelist = pipe.read().split()
#decomposition
for filename in namelist:
    split_filename = filename.split('_')        
    score = split_filename[2]
    id = split_filename[1]
    for line in linelist:
        try:
            if id == line[2]:
                line.append(score)
        except:
            pass

fout = open('test', 'w')
fout.write( codecs.BOM_UTF8 )
for line in linelist:
    for element in line:
        write_str = element + ' '
        fout.write(write_str)
    fout.write('\n')
fout.close()
        
