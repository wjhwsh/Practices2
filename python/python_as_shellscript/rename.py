#!/usr/bin/python
import subprocess
pipe = subprocess.Popen('ls score*', shell=True, stdout=subprocess.PIPE).stdout
namelist = pipe.read().split()

#decomposition
for filename in namelist:
    split_filename = filename.split('_')        
    score = int(split_filename[2])*2
    split_filename[2] = str(score) 
    #reconstruction
    new_name = '_'.join(split_filename)
    subprocess.call('mv ' + filename + ' ' + new_name, shell=True)
