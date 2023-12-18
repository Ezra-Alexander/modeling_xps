#!/bin/bash

#to reduce manual interference, this script runs es_run_big_ddft.sh with a specified number of random P chosen

reference=$1 #reference excited state input with correct basis set, rem
gs_scratch=$2 #scratch directory for ground state. Needs to have no "/" at the end
ncores=$3 # of cores you want to run on. recommend 8
gs_out=$4 # ground state output file, for lowdin populations
orbital=$5 #either 's' for the P1s orbital or 'p' for the P2p
n_sub=$6 #the number of P you want to excite
p_max=$7 #the number of P in your QD
priority=$8 #priority. based on size of studied system. short, normal, high, veryhigh

i=1
chosen=()
last=0
while [[ $i -le $n_sub ]]; do
	temp=$((1 + $RANDOM % $p_max))

	if [[ !  ${chosen[@]}  =~  " ${temp} " && !  ${chosen[0]}  =~  ${temp}  ]]; then 
		if [[ $temp != $last ]]; then
			chosen+=($temp)
    		i=$(( i + 1 ))
    		last=$temp
		fi
    	
	fi

			
done

sh ~/code/es_run_big_ddft.sh $reference $gs_scratch $ncores $gs_out $orbital $priority ${chosen[@]}