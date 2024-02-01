import numpy as np
import sys
import math
from geom_helper import *
from openpyxl import Workbook, load_workbook
from ddft_helper import get_energy
from qchem_helper import read_lowdin, get_geom_io, read_beta_lowdin

# the main juice of the bash script of the same name
# for a given ddft excited state, this script:
#	1. Computes the CEBE
#   2. Confirms that the correct P was excited
#		2.a. If wrong P was excited or CEBE is too high, prints stuff and skips excel editing
#   3. Writes the results to an excel script
#   	3.a. Creates the excel script if necessary
#   4. weights the different peaks by the appropriate amount using the directory name and a read-in weight
#		4.a. This means it extracts the P info from the geometry
#		4.b. Labels each peak as bulk, P-3c, or describing surface In
#		4.c. I'm assuming that P-3c and surface P-4c should be weighted the same but that isn't necessarily correct
#		4.d. I might also want to change "surface P-4c" to just "P-4c on In-3c and/or P-4c on high ligand In"
# right now this is hard-coded for P but it wouldn't be hard to change

#this version is adapted for the case of an unrestricted ground state and therefore an alpha hole (instead of the usual beta)

es_out=sys.argv[1] #excited state qchem ddft.out
gs_out=sys.argv[2] #excited state qchem ddft.out
iteration=int(sys.argv[3]) #which step of the excel creation you are on. For indexing
directory=sys.argv[4] #name of the directory, which should be of the form P_{N}, where N is the P-specific index.
ligand=sys.argv[5] #the ligand used here. Abbreviate. "F" for fluorine, "Cl" for chlorine
bulk_weight=int(sys.argv[6]) #the weighting to be applied to bulk P relative to P-uc and surface P-4c
orbital=sys.argv[7] #either 's' for the P1s orbital or 'p' for the P2p

bond_cutoff=3.1 #empirical parameter for upper bound on chemical bonds
if orbital=="p":
	energy_cutoff=143 #empirical parameter for upper bound on expected CEBEs. CEBEs above this will be considered to have failed to converge
elif orbital=="s":
	energy_cutoff=2160 #empirical parameter for upper bound on expected CEBEs. CEBEs above this will be considered to have failed to converge
else:
	raise Exception("orbital type not supported - please use either 's' for the P1s orbital or 'p' for the P2p")

#compute the CEBE
gs_energy = get_energy(gs_out) 
es_energy = get_energy(es_out)
energy_difference = es_energy - gs_energy

#determine target P
flag=0
p_index=""
for i,char in enumerate(directory):
	if char=="_":
		flag=flag+1
	elif flag==1:
		p_index=p_index+char

print(p_index)
#get geometry
atoms,coords=get_geom_io(gs_out)

test=False
#read Lowdin populations
if orbital=="p":
	#read first orb on the target
	orb_num=read_beta_lowdin(es_out,"P",p_index,2,"p") 
	#compare to minimum ground state P 2p orb
	min_p2p=read_beta_lowdin(gs_out,"P",str(0),2,"p")
	if orb_num<min_p2p:
		test=True

if  test and energy_difference<energy_cutoff: #1
	print("Excitation of", directory[:-1], "successful with energy", energy_difference, "and excited index",orb_num)
	converged=True
else:
	print("Warning! Excitation of", directory[:-1], "unsuccessful with energy", energy_difference, "and excited index",orb_num)
	converged=False
