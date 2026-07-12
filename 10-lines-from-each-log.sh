#!/bin/bash
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

echo "Choose Output Dirctory: "

check=0
while [ $check -eq 0 ];
do
        read dir
        if [ -d "$dir" ]; then
                check=1
        else
                echo "$dir does not exist or mistyped - try again:"
        fi
done


mkdir -p /collect
cd /collect
rm -rf *

cd /syslog
for i in `ls -t | tail -n 7`;
        do
                cp $i /collect
        done

cd /collect
gunzip *.gz

for n in `ls -1`;
        do
                tail -n 10 $n > $n-last10lines.txt
                rm -f $n
        done

cd /syslog
for m in `ls -1 *.log`;
        do
                tail -n 10 $m > /collect/$m`date +"%d-%m-%Y"`-last10lines.txt
        done

mv /collect/* $dir
rm -fr /collect

echo "Done Collecting 10 lines from each log oldest and newest logs, the are in $dir"
