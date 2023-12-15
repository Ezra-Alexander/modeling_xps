#!/bin/bash

#the goal of this script is to create and run a ground state ddft job from an optimization as soon as it finishes running
#this should be run with the following command: 
#sbatch  --dependency=afterok:"Job ID" nowait_gs_ddft.sh opt*.out * * * *
#need to have qchem_helper.py and output_xyz.py, as well as gs_ddft_runner.sh and its dependencies

opt_out=$1 #the name of the qchem.out file

ref=$2 #reference ddft.in

cores=$3 #requested number of cores. 12 should be fine

charge=$4 #charge. Should always be 0, but just in case

priority=$5 #priority. based on size of studied system. short, normal, high, veryhigh

python3 ~/code/output_xyz.py $opt_out

xyz_name=${opt_out%.*}".xyz"

sh ~/code/gs_ddft_runner.sh $xyz_name $ref $cores $charge $priority