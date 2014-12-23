#! /bin/bash 
echo "$1"
cat "$1" | cut -d $'\t' -f 1 > .out.txt
while read line
do
    echo "Extraction until $line"
    python ExtractUntilPeriod.py $line
done < "$1"
