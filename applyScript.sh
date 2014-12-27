#! /bin/bash 
echo "$2"
cat "$2" | cut -d $'\t' -f 1 > .out.txt
while read line
do
    echo "Apply script $1  for " $line
    python2.7 $1 $line
done < .out.txt
rm .out.txt
