import numpy as np
import sys
from qchem_helper import *

#the goal is to write a quick script that takes as input:
#a custom basis set for an atomic species, as a text for file
#another basis set, as a name
#a .xyz file
#a target atom of that same atomic species
#and writes the qchem basis section where that one atom has that one custom basis and everything else has the other basis

#for ddft
#output file is called basis_section.txt
#it includes everything between $basis and $end, not inclusive

#IMPORTANT: THIS DOESN'T WORK
#BASIS ISN'T ATOM-SPECIFIC INDEXED, IT'S TOTAL INDEXED

#also these uncontract-one approaches don't convergesca

xyz=sys.argv[1]
bas_file=sys.argv[2]
other_basis=sys.argv[3]
target_species=sys.argv[4]
target_index=int(sys.argv[5])

coords,atoms=read_xyz(xyz)
bas = open(bas_file, "r")
bas_lines=bas.readlines()

#determine each present atomic species
present=[]
for i,atom in enumerate(atoms):
	if atom not in present:
		present.append(atom)

#count them
counts={}
for i,atom in enumerate(present):
	counts[atom]=0

with open("basis_section.txt", "w") as out:
	for i,atom in enumerate(atoms):
		counts[atom]=counts[atom]+1
		out.write(atom+" "+str(counts[atom])+" \n")
		if atom==target_species and counts[atom]==target_index:
			for i,line in enumerate(bas_lines):
				out.write(bas_lines[i])
		else:
			out.write(other_basis+" \n")
		out.write("**** \n")



