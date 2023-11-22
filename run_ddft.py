import numpy as np
import sys
from qchem_helper import *

ref = sys.argv[1]
target = sys.argv[2]
print(ref, target)

lines = []
with open(ref,'r') as inp:
	for i,line in enumerate(inp):
		lines.append(line)

name = target+"th_electron_ddft.in"
target = int(target)
flag = 0
with open(name,'w') as out:
	for i,line in enumerate(lines):
		if flag==2:
			#max electrons needs to be changed if I change systems
			out.write("1:"+str(target-1)+" "+str(target+1)+":579 \n")
			flag = 0
		elif flag ==1:
			out.write(line)
			flag = flag+1
		elif line.find('$occupied') != -1 and flag==0:
			out.write(line)
			flag = flag+1
		else:
			out.write(line)
