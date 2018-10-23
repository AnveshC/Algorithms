#!/bin/bash


Files=`ls ./Data/ | grep .graph`

for file in $Files
do
	filename=`echo $file | cut -d'.' -f1`
	echo $filename
    python ./src/main.py -inst ./Data/$file -alg LS1 -time 1200 -seed 145
done
