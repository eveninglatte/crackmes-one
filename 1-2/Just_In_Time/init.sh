#!/bin/bash

g++ keygen.cpp

until [ ]; do
	SECS=$(date '+%S')
	if [ $((SECS % 10 % 3)) -eq 1 ]; then
		# we found the correct time to enter the password
		./a.out > >(./ski000)
		exit
	fi
	sleep 1
done

