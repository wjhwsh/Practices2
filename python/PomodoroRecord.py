#!/usr/bin/python
import sys, os, subprocess
import re
import time

pipe = subprocess.Popen("sqlite3 -line ~/Library/Application\ Support/Pomodoro/Pomodoro.sql '.dump ZPOMODOROS'"
                        , shell=True, stdout=subprocess.PIPE).stdout  
records = []
for i in pipe:
    entry = []
    # VALUES(1,1,1,319692236.602088,'Scan the paper and prepare the progress report')
    # VALUES(1,1,1,(group 1).602088,                    (groutp2)                   )
    regex = re.search(r'VALUES\(.*,(.*)\..*,\'(.*)\'\)', i)
    if regex:
        entry.append(regex.group(1))
        entry.append(regex.group(2))
        records.append(entry)

i = 0
for r in records:
    r[0] = time.localtime(int(r[0]))
    print r[1]
    #print r[0]
