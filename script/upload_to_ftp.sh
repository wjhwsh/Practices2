#!/bin/bash
FILENAME=gerrit2-$(date "+%Y-%m-%d").tar.gz
tar -zcvf $FILENAME gerrit2
ftp -inv 140.112.29.206 << EOF
user modcarl wclab
cd modcarl
put $FILENAME

