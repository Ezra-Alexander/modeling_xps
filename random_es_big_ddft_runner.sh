#!/bin/bash

#to reduce manual interference, this script runs es_run_big_ddft.sh with a specified number of random P chosen

reference=$1 #reference excited state input with correct basis set, rem
gs_scratch=$2 #scratch directory for ground state. Needs to have no "/" at the end
ncores=$3 # of cores you want to run on. recommend 8
gs_out=$4 # ground state output file, for lowdin populations
orbital=$5 #either 's' for the P1s orbital or 'p' for the P2p
n_sub=$5 #the number of P you want to excite
p_max=$6 #the number of P in your QD

i=1
chosen=()
while [[ $i -le $n_sub ]]; do
	#statements
	temp=$((1 + $RANDOM % $p_max))

	if [[ !  ${chosen[@]}  =~  $temp  ]]; then
    	chosen+=$temp
    	chosen+=" "
    	i=$(( i + 1 ))
	fi
	
done

sh ~/code/es_run_big_ddft.sh $reference $gs_scratch $ncores $gs_out $orbital $chosen