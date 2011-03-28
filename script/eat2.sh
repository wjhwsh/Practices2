#!/bin/bash

choice=(麥當勞 肯德基 漢堡王)
size=${#choice[*]}

echo "選項有"
for((i=0;i<$size;i++));do
    echo "$((i+1)) ${choice[$i]}"
done

question1="今天中午要吃甚麼，請按enter鍵... "
question2="離開請按 n 或按其他鍵重新選擇... "

question=$question1
while ((size>0)); do
        read -p $question -n 1 ans
        [ "$ans" = n ] && break
        echo "今天去吃${choice[`expr $RANDOM % $size`]}...吧!!!"
        question=$question2
done
echo ""

