#!/bin/bash

#this script takes a qchem output file and generates a ddft input file with the converged geometry (does not change basis set, etc)
#it then runs run_ddft on that inout file over a given range
#configured for ulysses
#separate jobs must be run in separate directories

#the qchem output file
qchem=$1
#reference ddft.in
ref=$2
#start of range of core electrons to be excited (inclusive)
st=$3
#end of range of core elelectrons to be excited (inclusive)
ed=$4

python3 /work/ezraa/code/ddft_maker.py $qchem $ref

sh /work/ezraa/code/run_ddft.sh reference.in $st $ed