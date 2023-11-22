#!/bin/bash

#this script takes a qchem output file and a reference es ddft input and then generates a ddft es input file with the converged geometry (does not change basis set, etc)
#it then runs es_run_ddft on that input file over a given range
#configured for ulysses
#separate jobs must be run in separate directories

#the qchem output file
qchem=$1
#reference es ddft.in
ref=$2
#start of range of core electrons to be excited (inclusive)
st=$3
#end of range of core elelectrons to be excited (inclusive)
ed=$4
#the number of cores you want each job to run on
ncores=$5

python3 /work/ezraa/code/es_ddft_maker.py $qchem $ref

sh /work/ezraa/code/es_run_ddft.sh es_reference.in $st $ed $ncores
