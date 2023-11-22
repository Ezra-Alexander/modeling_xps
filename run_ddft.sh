#!/bin/bash

#takes reference input as first input, and then the first and last electron you want to excite
#reference should be in directory this is run from

reference=$1
start=$2
end=$3

for (( c=$start; c<=$end; c++ ))
do
	mkdir "${c}th_electron"
	cd "${c}th_electron"

	scp "../${reference}" .

	#Written for Ulysses
	python3 /work/ezraa/code/run_ddft.py $reference "$c"

	sqthis -J "${c}th_electron_ddft" -c 4 -t unlimited qchem.latest -nt 4 "${c}th_electron_ddft.in" "${c}th_electron_ddft.out"

	cd ..
done

