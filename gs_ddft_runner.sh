#!/bin/bash

#this script takes an xyz, a reference ddft gs input, and some parameters. Assumes spin 1
#it then generates a ddft gs input file with the converged geometry (does not change basis set, etc)
#it then makes a .sh file to run the ground state and save its scratch to the current directory
#finally, it runs that .sh
#configured for large dots on telemachus
#should be run in the parent directory of each of the individual core excitations
#may run into labeling trouble if running multiple jobs from .xyzs of the same name

#PENDING BUG FIX - if reference geometry section is shorter than xyz geometry, it curtails geometry

#must be a .xyz
xyz=$1
#reference ddft.in
ref=$2
#requested number of cores. 12 should be fine
cores=$3
#charge. Should always be 0, but just in case
charge=$4
#priority. based on size of studied system. short, normal, high, veryhigh
priority=$5

python3 ~/code/gs_ddft_maker.py $xyz $ref $cores $charge $priority

sbatch submit_gs.sh
