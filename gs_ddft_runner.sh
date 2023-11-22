#!/bin/bash

#this script takes an xyz, a reference ddft gs input, and some parameters. Assumes spin 1
#it then generates a ddft gs input file with the converged geometry (does not change basis set, etc)
#it then makes a .sh file to run the ground state and save its scratch to the current directory
#finally, it runs that .sh
#configured for large dots on telemachus
#should be run in the parent directory of each of the individual core excitations
#may run into labeling trouble if running multiple jobs from .xyzs of the same name

#PENDING BUG FIX - if reference geometry section is shorter than xyz geometry, it curtails geometry

#the qchem plot output file. needs to be qchem and not xyz because it takes the spin and charge
xyz=$1
#reference ddft.in
ref=$2
#requested number of cores. 12 should be fine
cores=$3
#charge. Should always be 0, but just in case
charge=$4

python3 ~/code/gs_ddft_maker.py $xyz $ref $cores $charge

sbatch submit_gs.sh
