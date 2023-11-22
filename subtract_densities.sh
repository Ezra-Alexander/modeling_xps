#!/bin/bash

#A script that recursively goes through a bunch of directories and runs cube_tools.py for all of them
#note that the inputs are the full directory names, not just the numbers

for dir in "$@"
do

	cd $dir
	
	cd difference_density

	cube_tools.py -s es_plot.out.plots/dens.0.cube gs_plot.out.plots/dens.0.cube

	cd ../..

done