#!/bin/bash

#this script is meant to take a pre-made XPS excel sheet and apply a specifed spin-orbit splitting to it, which it then plots

excel=$1 #name of excel file to read
splitting=$2 #the spin-orbit splitting to apply. 0.86 eV is an often used value, derived from PH3 and PF3
title=$3 #the title you want on the plot

#almost all of this can be done by a python function, I think. The bash script is uneccesary but nice
python3 ~/wormk/code/basic_spin_orbit_applier.py $excel $splitting 

#then call my plotting function on the new excel
python3 ~/wormk/code/figure_xps_general.py "spin_orbit_${excel}" "$title"
