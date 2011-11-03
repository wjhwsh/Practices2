#!/usr/bin/python
import subprocess
pipe = subprocess.Popen("ls", shell=True, stdout=subprocess.PIPE).stdout
file_str = pipe.read()
file_list = list(file_str.split('\n'))

for file in file_list:
    print '"' + str(file) + '"' + ', '
