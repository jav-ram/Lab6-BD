#!/bin/sh

set FILES = ""
set FILE = " data/items-"
set EXTENSION = ".xml"

for i in $(seq 0 39) 
do
	$FILES="$FILE$iEXTENSION"|
done

python paser.py data/items-0.xml