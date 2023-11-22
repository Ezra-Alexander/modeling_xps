import numpy as np
import sys
from qchem_helper import *

#Takes a ddft input and makes two jobs that plot the ground state and excited state density respectively
#meant to be used in conjunction with the bash script of the same name


ref = sys.argv[1]

lines = []
with open(ref,'r') as inp:
	for i,line in enumerate(inp):
		lines.append(line)

gs_name = "gs_"+ref
flag =0
with open(gs_name,'w') as gs:
	for i,line in enumerate(lines):
		if line.find('$rem') != -1 and flag==0:
			flag += 1
			gs.write(line)
			gs.write("make_cube_files true \n")
			gs.write("plots true \n")
		elif line.find('$end') != -1 and flag==1:
			flag += 1
			gs.write(line)
			gs.write("\n")
			gs.write("$plots \n")
			gs.write("grid_range (-20,20) (-20,20) (-20,20) \n")
			gs.write("grid_points 150 150 150 \n")
			gs.write("total_density 0 \n")
			gs.write("$end \n")
		else:
			gs.write(line)

es_name = "es_"+ref
flag =0
with open(es_name,'w') as es:
	for i,line in enumerate(lines):
		if line.find('$rem') != -1 and flag==0:
			flag += 1
			es.write(line)
		elif line.find('$rem') != -1 and flag==1:
			es.write(line)
			flag += 1
			es.write("make_cube_files true \n")
			es.write("plots true \n")
		elif line.find('$end') != -1 and flag==2:
			flag += 1
			es.write(line)
			es.write("\n")
			es.write("$plots \n")
			es.write("grid_range (-20,20) (-20,20) (-20,20) \n")
			es.write("grid_points 150 150 150 \n")
			es.write("total_density 0 \n")
			es.write("$end \n")
		else:
			es.write(line)