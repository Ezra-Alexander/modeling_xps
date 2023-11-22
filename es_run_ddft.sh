#!/bin/bash

#takes reference es input as first input, and then the first and last electron you want to excite
#run_es_ddft will make the specific ddft input for a given excitation as well as make the appropriate scratch manipulation sbatch script (submit_es.sh)
#reference should be in directory this is run from
#assumes that each job will be run with 4 gb/core

reference=$1
st=$2
end=$3
ncores=$4

i=$st
while [ "$i" -le "$end" ]; do
	mkdir "${i}th_core"
	cd "${i}th_core"

	scp "../${reference}" .

	#Written for Ulysses
	python3 /work/ezraa/code/run_es_ddft.py $reference "$i" $ncores

	sbatch submit_es.sh

	cd ..
	i=$(( i + 1))
done

