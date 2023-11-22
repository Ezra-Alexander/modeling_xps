#!/bin/bash

#This script is meant to be run on my laptop, and should loop over a bunch of delta DFT directories and print CEBEs and atom numbers
#gs is the ground state output file

gs=$1
ga=$2 #either True or False


sed -i '.bak' '/ProcedureUnspecified/d' $gs

for d in */
do
	cd $d
	sed -i '.bak' '/ProcedureUnspecified/d' *.out
	scp ../$gs . #use when gs and es are in different files
	mv $gs ground_state
	#echo $d
	python3 ~/wormk/code/mass_ddft_analyzer.py *.out ground_state $ga
	# python3 ~/wormk/code/energy_getter_ddft.py *.out 
	cd ../
done