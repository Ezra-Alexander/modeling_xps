#this should analyze the outputs of a delta dft job - assuming the leftover core state is now the lowest energy alpha MO

import numpy as np
import sys
from ddft_helper import get_mulliken_charges, get_lowdin_charges, get_becke_charges, run_test, get_energies, get_time, run_better_test

#inputs from the command line
output_file=sys.argv[1]
#core electron to be excited
#target = sys.argv[2]
#ligand
ligand = "F"

#test to make sure that the job actually excited what we think it did
test = run_better_test(output_file)
print(test)
#if test == False:
#	print("Uh oh!")
#	quit()

#get the mulliken charges
atoms, m_charges = get_mulliken_charges(output_file)

#get the Lowdin charges
l_atoms, atom_nums, orbs, l_occs = get_lowdin_charges(output_file)

#get the Becke charge
b_atoms, b_charges = get_becke_charges(output_file)

#check to see which atom(s) have an unusual mulliken charge

#the array of atoms with unusual mulliken charge
fucky_atoms = []

#separate the charges into a separate array for each atom
p_charges = []
in_charges = []
f_charges = []

for i,atom in enumerate(atoms):
	if atom == "In":
		in_charges.append(m_charges[i])
	if atom == ligand:
		f_charges.append(m_charges[i])
	if atom == "P":
		p_charges.append(m_charges[i])

#find the mean and stddev of the charge for each atom
p_mean = np.mean(p_charges)
in_mean = np.mean(in_charges)
f_mean = np.mean(f_charges)
p_stddev = np.std(p_charges)
in_stddev =  np.std(in_charges)
f_stddev = np.std(f_charges)

#add any atoms with very different mulliken charge from the average to "fucky atoms"
#NOTE - I am currently considering an atom to be fucky if it has a mulliken charge > 1.5 standard deviations from the mean. The choice of 3 here is just a guess
for i,atom in enumerate(atoms):
	if atom == "In":
		if abs(m_charges[i]-in_mean) > 1.5*in_stddev:
			fucky_atoms.append(i)
	if atom == "P":
		if abs(m_charges[i]-p_mean) > 1.5*p_stddev:
			fucky_atoms.append(i)
	if atom == ligand:
		if abs(m_charges[i]-f_mean) > 1.5*f_stddev:
			fucky_atoms.append(i)

#"error messages"			
mean = 'whoops'
stddev = "uh oh"

#print statement
#print("The following atoms have unusual Mulliken Charge")
#for atom in fucky_atoms:
#	print("Atom", atom+1)
#	print("Which is a", atoms[atom])
#	print("Has a Mulliken charge of", m_charges[atom])
#	if atoms[atom] == "In":
#		mean = in_mean
#		stddev = in_stddev
#	if atoms[atom] == ligand:
#		mean = f_mean
#		stddev = f_stddev
#	if atoms[atom] == "P":
#		mean = p_mean
#		stddev = p_stddev
#	print("Whereas the average charge for a", atoms[atom], "is", mean)
#	print("With a standard deviation of", stddev)
#	print()


#check to see which atom(s) have an unusual lowdin charge

#the array of indices of atoms with unusual lowdin charge
lowdin_atoms = []
#the array of nonzero occupation numbers
nonzero_occs = []

#find all nonzero occupation numbers - edited for p orbitals
for i, occs in enumerate(l_occs):
	for occ in occs:
		if occ > 0.01:
			lowdin_atoms.append(i)


#print statement
print("The following atoms have nonzero Lowdin Charge")
for atom in lowdin_atoms:
	print("Atom", atom//3+1)
	print("Which is", l_atoms[atom],atom_nums[atom])
	print("Has an occupation of", l_occs[atom], "in a", orbs[atom], "orbital, the lowest MO of its kind")
	print()


#check to see which atom(s) have an unusual becke charge

#the array of atoms with unusual becke charge
fucky_becke = []

#separate the charges into a separate array for each atom
p_charges_b = []
in_charges_b = []
f_charges_b = []

for i,atom in enumerate(b_atoms):
	if atom == "In":
		in_charges_b.append(b_charges[i])
	if atom == ligand:
		f_charges_b.append(b_charges[i])
	if atom == "P":
		p_charges_b.append(b_charges[i])

#find the mean and stddev of the charge for each atom
p_mean_b = np.mean(p_charges_b)
in_mean_b = np.mean(in_charges_b)
f_mean_b = np.mean(f_charges_b)
p_stddev_b = np.std(p_charges_b)
in_stddev_b =  np.std(in_charges_b)
f_stddev_b = np.std(f_charges_b)

#add any atoms with very different becke charge from the average to "fucky atoms"
#NOTE - I am currently considering an atom to be fucky if it has a becke charge > 2 standard deviations from the mean. The choice of 2 here is just a guess
for i,atom in enumerate(b_atoms):
	if atom == "In":
		if abs(b_charges[i]-in_mean_b) > 2*in_stddev_b:
			fucky_becke.append(i)
	if atom == "P":
		if abs(b_charges[i]-p_mean_b) > 2*p_stddev_b:
			fucky_becke.append(i)
	if atom == ligand:
		if abs(b_charges[i]-f_mean_b) > 2*f_stddev_b:
			fucky_becke.append(i)

#"error messages"			
mean = 'whoops'
stddev = "uh oh"

#print statement
#print("The following atoms have unusual Becke Charge")
#for atom in fucky_becke:
#	print("Atom", atom+1)
#	print("Which is a", b_atoms[atom])
#	print("Has a Becke charge of", b_charges[atom])
#	if b_atoms[atom] == "In":
#		b_mean = in_mean_b
#		b_stddev = in_stddev_b
#	if b_atoms[atom] == ligand:
#		b_mean = f_mean_b
#		b_stddev = f_stddev_b
#	if b_atoms[atom] == "P":
#		b_mean = p_mean_b
#		b_stddev = p_stddev_b
#	print("Whereas the average charge for a", b_atoms[atom], "is", b_mean)
#	print("With a standard deviation of", b_stddev)
#	print()

energy_difference = get_energies(output_file)
print("Energy difference is ", energy_difference, "eV")
print()

time = get_time(output_file)
print("CPU Time is ", time, "s")
