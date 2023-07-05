#!/bin/bash



lol() {
	echo "$1 $2"
	if [ $2 == 1 ]; then
		echo "Error"
	else
		res=$(($1/$2))
		echo "LoL $res"
	fi
}

lol 10 1
