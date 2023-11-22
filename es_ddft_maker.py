import numpy as np
import sys
from qchem_helper import get_geom_e_opt_last, get_rem_sp

#takes a qchem output and a reference es ddft input  and makes a new es ddft input (es_reference.in) using the optimized geometry

#the converged qchem opt
qchem=sys.argv[1]
#the reference ddft job
ref=sys.argv[2]

with open(qchem, "r") as q:
	lines = q.readlines()
	geom = get_geom_e_opt_last(lines)
	for i, line in enumerate(lines):
		if line.find('$molecule') != -1:
			spcharge = lines[i+1]
			break
	for i, line in enumerate(lines):
		if line.find('beta electrons') != -1:
			max_e = line.strip().split()[2]
			break
	sp = spcharge.strip().split()[1]
	charge = spcharge.strip().split()[0]

lines = []
with open(ref, "r") as re:
	lines = re.readlines()

geom_flag = 0
job_flag = 2
occ_flag = 0
with open("es_reference.in", "w") as out:
	for i,line in enumerate(lines):

		if geom_flag > 1 and line.find('$end') == -1:
			if geom_flag <= len(geom)+1:
				for j,coord in enumerate(geom[geom_flag-2]):
					out.write(coord)
					out.write(" ")
				out.write("\n")
				geom_flag=geom_flag+1
			else:
				geom_flag=geom_flag+1

		elif geom_flag ==1 and job_flag==1:
			out.write(spcharge)
			geom_flag=geom_flag+1

		elif geom_flag ==1 and job_flag==2:
			out.write(str(int(charge)+1) + " " + str(int(sp)+1) + " \n")
			geom_flag=geom_flag+1

		elif geom_flag > 1 and line.find('$end') != -1:
			geom_flag=0
			out.write(line)

		elif occ_flag ==1:
			out.write("1:"+str(max_e)+" \n")
			#print(line.strip()[2:])
			occ_flag=2

		elif occ_flag==2:
			out.write("1 3:"+str(max_e)+" \n")
			occ_flag=0

		elif line.find('$molecule') != -1:
			geom_flag = 1
			out.write(line)

		elif line.find('@@@') != -1:
			job_flag=2
			out.write(line)

		elif line.find('$occupied') != -1:
			occ_flag=1
			out.write(line)

		else:
			out.write(line)
