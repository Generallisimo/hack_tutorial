#!/bin/bash

for(( i=1; i<10; i++)); do
	echo  "Number? $i"
done

for i in {2..5}; do
	echo "What? $i"
done

i=0
while [ $i -lt 10 ];do
	echo "Ok? $i"
	i=$(($i+1))
done
