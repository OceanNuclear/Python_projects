#!/bin/bash
read -p "Please input the filename without 1- and .wpl:" filename

filename=$filename'.wpl'

sed -i -e 's/E:\\Ocean2\\Music\\//g' $filename
sed -i.bak -e 's:Instrumental\\:Instrumental/:g' $filename
sed -i.bak -e 's:Crywolf _:Crywolf \&amp;:g' $filename

filename_new='1-'$filename
mv $filename $filename_new
rm *.bak
