#!/bin/bash

#takes a number of ddft jobs and runs the density plots for them so that difference density plots can be made
#uses the python script of the same name

for dir in "$@"
do

	cd "${dir}*"
	echo $dir

	mkdir "difference_density"
	cd "difference_density"
	
	#currently configured for Ulysses
	python3 /work/ezraa/code/ddft_difference_density-ifier.py *.in 
	echo running

	cd ../..

done