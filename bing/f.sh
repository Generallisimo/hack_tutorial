#!/bin/bash


read -p "Society number?" num

if [ "$num" == 5 ]; then
	echo "walk man"
elif [ "$num" -gt 10 ]; then
	echo "Hello bro"
else
	read -p "Name?" name
fi
