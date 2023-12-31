#!/bin/bash

#takes reference es input, gs.out, and gs scratch as inputs, then some number of P you want to excite
#run_big_es_ddft will make the specific ddft input for a given excitation as well as make the appropriate scratch manipulation sbatch script (submit_es.sh)
#reference should be in directory this is run from
#Adapted for running big jobs on telemachus
#should work for P 2p and P 2s spectra

reference=$1 #reference excited state input with correct basis set, rem
gs_scratch=$2 #scratch directory for ground state. Needs to have no "/" at the end
ncores=$3 # of cores you want to run on. recommend 8
gs_out=$4 # ground state output file, for lowdin populations
orbital=$5 #either 's' for the P1s orbital or 'p' for the P2p
priority=$6 #priority. based on size of studied system. short, normal, high, veryhigh

shift 6

#the following inputs should be a list of P atom-specific indexes. 


while [[ $# -gt 0 ]]; do

	num=$1

	mkdir "P_${num}"
	cd "P_${num}"

	scp "../${reference}" .
	scp "../${gs_out}" .

	#Written for Telemachus
	python3 ~/code/run_big_es_ddft.py $reference $num $ncores $gs_out $gs_scratch $orbital $priority

	sbatch submit_es.sh

	cd ..
	
	shift 1

done

