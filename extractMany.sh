#! /bin/bash 
while read line
do
    python2.7 ExtractUntilPeriod.py $line
done < $1
