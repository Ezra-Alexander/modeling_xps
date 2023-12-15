import numpy as np
import sys
from qchem_helper import *

#takes a qchem output and a reference gs ddft input (basically just a single point using the appropriate basis set) and makes a new gs ddft input (gs_ddft.in) using the optimized geometry
#then makes a .sh file (submit_gs.sh) that runs gs_ddft.in and saves its scratch directory to the current directory
#assumes 4 gb / cpu but that may sometimes not be enough

#the geometry
xyz=sys.argv[1]
#the reference ddft job
ref=sys.argv[2]
#Requested number of cores 
ncores = sys.argv[3]
#charge
charge=sys.argv[4]
#priority. based on size of studied system. short, normal, high, veryhigh
priority=sys.argv[5]

flag=0
label=""
for i,char in enumerate(xyz): #make a label algorithmically. requires .xyzs to be labeled
	if char=="_":
		flag=flag+1
	elif flag==1:
		label=label+char
print(label)

with open(xyz, "r") as q:
	geom = q.readlines()[2:]

sp="1" #assuming spin 1

lines = []
with open(ref, "r") as re:
	lines = re.readlines()

geom_flag = 0
with open("gs_ddft.in", "w") as out:
	for i,line in enumerate(lines):

		if geom_flag > 1 and line.find('$end') == -1:
			if geom_flag <= len(geom)+1:
				# for j,coord in enumerate(geom[geom_flag-2]):
				# 	out.write(coord)
				# 	out.write(" ")
				# out.write("\n")
				out.write(geom[geom_flag-2])
				geom_flag=geom_flag+1
			else:
				geom_flag=geom_flag+1

		elif geom_flag ==1:
			out.write(charge+" "+sp+" \n")
			geom_flag=geom_flag+1

		elif geom_flag > 1 and line.find('$end') != -1:
			geom_flag=0
			out.write(line)

		elif line.find('$molecule') != -1:
			geom_flag = 1
			out.write(line)

		else:
			out.write(line)

if priority=="veryhigh":
	with open("submit_gs.sh", "w") as sbatch:
		sbatch.write("#!/bin/bash \n")
		sbatch.write("\n")
		sbatch.write("#SBATCH -J gs_"+label+"_ddft.in \n")
		sbatch.write("#SBATCH -o gs_ddft.log \n")
		sbatch.write("#SBATCH -e gs_ddft.log \n")
		sbatch.write("#SBATCH --time unlimited \n")
		sbatch.write("#SBATCH -c " + ncores + " \n")
		sbatch.write("#SBATCH --mem-per-cpu 16000 \n")
		sbatch.write("#SBATCH -p veryhigh \n")
		sbatch.write(" \n")
		sbatch.write('scratch="scratch_'+label+'_gs_ddft" \n')
		sbatch.write('curr_d=$PWD \n')
		sbatch.write(" \n")
		sbatch.write("rm -r $QCSCRATCH/$scratch \n")
		sbatch.write("cp -r $scratch $QCSCRATCH \n")
		sbatch.write(" \n")
		sbatch.write("qchem.latest -save -nt " + ncores +" gs_ddft.in gs_ddft.out $scratch \n")
		sbatch.write(" \n")
		sbatch.write("cp -r $QCSCRATCH/$scratch $curr_d")
elif priority=="short":
	with open("submit_gs.sh", "w") as sbatch:
		sbatch.write("#!/bin/bash \n")
		sbatch.write("\n")
		sbatch.write("#SBATCH -J gs_"+label+"_ddft.in \n")
		sbatch.write("#SBATCH -o gs_ddft.log \n")
		sbatch.write("#SBATCH -e gs_ddft.log \n")
		sbatch.write("#SBATCH -c " + ncores + " \n")
		sbatch.write("#SBATCH --mem-per-cpu 4000 \n")
		sbatch.write("#SBATCH -p short \n")
		sbatch.write(" \n")
		sbatch.write('scratch="scratch_'+label+'_gs_ddft" \n')
		sbatch.write('curr_d=$PWD \n')
		sbatch.write(" \n")
		sbatch.write("rm -r $QCSCRATCH/$scratch \n")
		sbatch.write("cp -r $scratch $QCSCRATCH \n")
		sbatch.write(" \n")
		sbatch.write("qchem.latest -save -nt " + ncores +" gs_ddft.in gs_ddft.out $scratch \n")
		sbatch.write(" \n")
		sbatch.write("cp -r $QCSCRATCH/$scratch $curr_d")
else:
	raise Exception("File not written - chosen priority not yet coded")
