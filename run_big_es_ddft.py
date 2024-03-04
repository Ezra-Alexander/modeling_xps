import numpy as np
import sys
from qchem_helper import *

#makes the es ddft inputs and submit scripts.
#configured for big dots on Telemachus

ref = sys.argv[1] #reference es.in
target = sys.argv[2] #P atom-specific index 
print(ref, target)
ncores = sys.argv[3] #number of cores
gs_out=sys.argv[4] #gs output file with Lowdin populations
gs_scratch=sys.argv[5] #ground state scratch directory
orbital=sys.argv[6] #either 's' for the P1s orbital or 'p' for the P2p
priority=sys.argv[7] #priority. based on size of studied system. short, normal, high, veryhigh

if orbital=="p":
	mo_index=read_lowdin(gs_out,"P",target,2,orbital)
elif orbital=="s":
	mo_index=read_lowdin(gs_out,"P",target,1,orbital)
else:
	raise Exception("orbital type not yet supported - please enter either 's' for the P1s orbital or 'p' for the P2p")

mo_index=int(mo_index)
print("Targeting MO", mo_index)

with open(gs_out,'r') as out: #get max electrons
	for i,line in enumerate(out):
		if line.find("beta")!= -1:
			line=line.strip().split()
			max_e=line[2]
			break

atoms,coords=get_geom_io(gs_out)

lines = []
with open(ref,'r') as inp:
	for i,line in enumerate(inp):
		lines.append(line)

name = "P_"+target+"_ddft.in"
target = int(target)
occ_flag = 0
geom_flag= 0
with open(name,'w') as out:
	for i,line in enumerate(lines):
		if occ_flag==2:
			out.write("1:"+str(mo_index-1)+" "+str(mo_index+1)+":"+max_e+" \n")
			occ_flag = 0
		elif occ_flag==1:
			out.write("1:"+str(max_e) +" \n")
			occ_flag = occ_flag+1
		elif line.find('$occupied') != -1 and occ_flag==0:
			out.write(line)
			occ_flag = occ_flag+1
		elif line.find('$molecule') != -1 and geom_flag==0:
			geom_flag=geom_flag+1
			out.write(line)
		elif geom_flag==1:
			geom_flag=geom_flag+1
			out.write(line)
		elif line.find('mem_total') != -1:
			mem_total=line.strip().split()[1]
			out.write(line)
		elif geom_flag>1:
			if line.find('$end')!=-1:

				if len(atoms)>geom_flag-2: #accounts for geometries longer than the reference geometry section
					n_more=len(atoms)-geom_flag+2
					for j in range(n_more):
						out.write(atoms[geom_flag-2+j]+" " + str(coords[geom_flag-2+j][0])+" "+ str(coords[geom_flag-2+j][1])+" "+ str(coords[geom_flag-2+j][2])+" \n")

				geom_flag=0
				out.write(line)
			elif geom_flag-2>= len(atoms):
				pass
			else:
				out.write(atoms[geom_flag-2]+" " + str(coords[geom_flag-2][0])+" "+ str(coords[geom_flag-2][1])+" "+ str(coords[geom_flag-2][2])+" \n")
				geom_flag=geom_flag+1
		else:
			out.write(line)

if priority=="veryhigh":
	with open("submit_es.sh",'w') as sub:
		sub.write("#!/bin/bash \n")
		sub.write("\n")
		sub.write("#SBATCH -J "+name[:-3]+" \n")
		sub.write("#SBATCH -o "+name[:-3]+".log \n")
		sub.write("#SBATCH -e "+name[:-3]+".log \n")
		sub.write("#SBATCH --time unlimited \n")
		sub.write("#SBATCH -c "+ncores+" \n")
		sub.write("#SBATCH --mem-per-cpu "+mem_total+" \n")
		sub.write("#SBATCH -p veryhigh \n")
		sub.write(" \n")
		sub.write('scratch='+gs_scratch+' \n')
		sub.write("rm -r /scratch/ezraa/$scratch/ \n")
		sub.write(" \n")
		# sub.write("scp -r ../$scratch/ . \n")
		# sub.write('mv $scratch/ "${scratch}_'+name[:-8]+'"/ \n')
		# sub.write("\n")
		# sub.write('scp -r "${scratch}_'+name[:-8]+'"/ /scratch/ezraa \n')
		# sub.write('rm -r "${scratch}_'+name[:-8]+'"/ \n')
		sub.write('scp -r ../$scratch/ /scratch/ezraa/"${scratch}_'+name[:-8]+'" \n')
		sub.write("\n")
		sub.write('qchem.latest -save -nt '+ncores+' '+name+' '+name[:-3]+'.out "${scratch}_'+name[:-8]+'" \n')
		sub.write(" \n")
		sub.write("rm -r /scratch/ezraa/${scratch}_"+name[:-8]+"/ \n")
		#sub.write('rm -r "${scratch}_'+name[:-8]+'"/ \n')
elif priority=="short":
	with open("submit_es.sh",'w') as sub:
		sub.write("#!/bin/bash \n")
		sub.write("\n")
		sub.write("#SBATCH -J "+name[:-3]+" \n")
		sub.write("#SBATCH -o "+name[:-3]+".log \n")
		sub.write("#SBATCH -e "+name[:-3]+".log \n")
		sub.write("#SBATCH -c "+ncores+" \n")
		sub.write("#SBATCH --mem-per-cpu "+mem_total+" \n")
		sub.write("#SBATCH -p short \n")
		sub.write(" \n")
		sub.write('scratch='+gs_scratch+' \n')
		sub.write("rm -r /scratch/ezraa/$scratch/ \n")
		sub.write(" \n")
		sub.write("scp -r ../$scratch/ . \n")
		sub.write('mv $scratch/ "${scratch}_'+name[:-8]+'"/ \n')
		sub.write("\n")
		#for ulysses
		sub.write('scp -r "${scratch}_'+name[:-8]+'"/ /scratch/ezraa \n')
		sub.write('rm -r "${scratch}_'+name[:-8]+'"/ \n')
		sub.write("\n")
		sub.write('qchem.latest -save -nt '+ncores+' '+name+' '+name[:-3]+'.out "${scratch}_'+name[:-8]+'" \n')
		sub.write(" \n")
		sub.write("rm -r /scratch/ezraa/${scratch}_"+name[:-8]+"/ \n")
		sub.write('rm -r "${scratch}_'+name[:-8]+'"/ \n')
else:
	raise Exception("File not written - chosen priority not yet coded")