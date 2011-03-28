#!/bin/bash

list="麥當勞 肯德基 漢堡王 摩斯漢堡"

while((1));do
 echo 今天吃： $list|awk '{print $1 $'"$[$RANDOM%`echo $list|wc -w`+2]"' }'
 read -n 1 -p "Enter 鍵繼續，Ctrl+c  離開"
done
