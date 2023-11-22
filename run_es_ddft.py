import numpy as np
import sys
from qchem_helper import *

#makes the es ddft inputs and submit scripts.
#configured for Ulysses

ref = sys.argv[1]
target = sys.argv[2]
print(ref, target)
ncores = sys.argv[3]

lines = []
with open(ref,'r') as inp:
	for i,line in enumerate(inp):
		lines.append(line)

name = target+"th_ddft.in"
target = int(target)
flag = 0
max_e=0
with open(name,'w') as out:
	for i,line in enumerate(lines):
		if flag==2:
			#max electrons needs to be changed if I change systems
			out.write("1:"+str(target-1)+" "+str(target+1)+":"+max_e+" \n")
			flag = 0
		elif flag ==1:
			out.write(line)
			max_e=line.strip()[2:]
			flag = flag+1
		elif line.find('$occupied') != -1 and flag==0:
			out.write(line)
			flag = flag+1
		else:
			out.write(line)

with open("submit_es.sh",'w') as sub:
	sub.write("#!/bin/bash \n")
	sub.write("\n")
	sub.write("#SBATCH -J "+name[:-3]+" \n")
	sub.write("#SBATCH -o "+name[:-3]+".log \n")
	sub.write("#SBATCH -e "+name[:-3]+".log \n")
	sub.write("#SBATCH --time unlimited \n")
	sub.write("#SBATCH -c "+ncores+" \n")
	sub.write("#SBATCH --mem-per-cpu 4000 \n")
	sub.write(" \n")
	sub.write('scratch="scratch_gs_ddft" \n')
	sub.write("rm -r /scratch/ezraa/$scratch/ \n")
	sub.write(" \n")
	sub.write("scp -r ../$scratch/ . \n")
	sub.write('mv $scratch/ "${scratch}_'+name[:-8]+'"/ \n')
	sub.write("\n")
	#for ulysses
	sub.write('scp -r "${scratch}_'+name[:-8]+'"/ /scratch/ezraa \n')
	sub.write("\n")
	sub.write('qchem.latest -save -nt '+ncores+' '+name+' '+name[:-3]+'.out "${scratch}_'+name[:-8]+'" \n')
	sub.write(" \n")
	sub.write("rm -r /scratch/ezraa/$scratch/ \n")
	sub.write('rm -r "${scratch}_'+name[:-8]+'"/ \n')
