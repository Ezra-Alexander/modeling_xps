#!/bin/bash

#A replacement for ddft_output_time_saver
#meant to turn a directory full of ddft jobs into a single excel spreadsheet that plots the XPS
#excel spreadhseet will be named "collected_spectrum.xlsx"

gs=$1 #the name of the ground state output file
splitting=$2 #the spin-orbit splitting to apply. 0.86 eV is an often used value for P 2p, derived from PH3 and PF3
plot_title=$3 #the title you want on the plot
ligand=$4 #the ligand present in your dot (for determining where the surface is). F for fluorine, Cl for chlorine
bulk_weight=$5 #the number of times you want to repeat each bulk peak to get a spectrum that looks appropriately weighted

sed -i '.bak' '/ProcedureUnspecified/d' $gs #edits the ground state output file to not crash the script

i=0
for d in */ #loop over each subdirectory
do
	scratch=${d:0:7}
	if [ $scratch == "scratch" ];
	then
		echo Skipping $d
	else
		cd $d
		if [ $i -ne 0 ];
		then
			scp ../collected_spectrum.xlsx .
		fi
		len=${#d}
		name=${d:0:$len-1} #some finagling to get the file names right
		sed -i '.bak' '/ProcedureUnspecified/d' ${name}_ddft.out
		scp ../$gs . 
		python3 ~/wormk/code/big_ddft_analyzer.py ${name}_ddft.out $gs $i $d $ligand $bulk_weight
		scp collected_spectrum.xlsx ../
		cd ../
		i=$(( i + 1))
	fi
done

sh ~/wormk/code/basic_spin_orbit_applier.sh collected_spectrum.xlsx $splitting "$plot_title"