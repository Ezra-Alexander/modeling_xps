import sys
import numpy as np

#this script is meant to extract the Atomic Orbital Overlap Matrix and MO Coefficient Matrix 
#from a qchem ddft output using scf_final_print 3 in the first job and print_orbitals true in the second
#combines alpha and beta MO coefficients into one matrix

#delta-dft output file
out = sys.argv[1]

#useful parameters to extract from output file
nbas = 0 #number of basis functions
n_a_elec = 0 #number of alpha = beta electrons in ground state

#open output file
with open(out, "r") as o:
	lines = o.readlines()


copy_o = 0 #flag that turns on copying of Overlap Matrix in ground-state calculation
copy_c = 0 #flag that turns on copying of MO coefficients in core-excited state calculation
job = 1 #flag that determines which of the two calculations you are in
o_mat = [] #for storing raw overlap matrix from output
coeff = [] #for storing raw alpha and beta mo coefficient matrices from ouput

#begin iterating through file
for i, line in enumerate(lines):

	if line.find("basis functions") != -1: #extract nbas
		nbas = int(line.strip().split()[5])

	if line.find("beta electrons") != -1: #extract number of electrons/2
		n_a_elec = int(line.strip().split()[2])

	if copy_o > 0 and line.find("Core Hamiltonian") != -1: #end copying of overlap matrix
		copy_o = 0

	if copy_o > 0: #copy overlap matrix while flag is on
		#print(line)
		o_mat.append(line.strip().split())

	if line.find("Overlap Matrix") != -1: #begin copying overlap matrix on the next line
		copy_o = 1

	if line.find("Have a nice day") != -1: #switch to job 2
		job = 2

	if copy_c > 0 and line.find("Ground-State Mulliken Net Atomic Charges")!= -1: #stop copying MO coeficient matrix
		copy_c = 0

	if copy_c > 0: #copy MO coefficient matrix while flag is on
		#print(line)
		coeff.append(line.strip().split())

	if job==2 and line.find("ALPHA MOLECULAR ORBITAL COEFFICIENTS")!= -1: #begin copying MO coefficient matrix on next line
		copy_c = 1


#prune saved arrays so that they only contain desired matrix elements

npop = nbas//6 #QChem outputs the Overlap matrix 6 columns at a time. Npop is the number of times it does this
#at this point OMat is 7 across and npop*(nbas+1) long, where the 1st, 116th, 231st, etc rows are 6 across

for i in range(npop): #Each set of columns is proceeded by a row of numbering. We want to remove that
	#print(o_mat[(npop-1-i)*(nbas+1)]) 
	o_mat.pop((npop-1-i)*(nbas+1)) #cycle through them backwards and pop them off
#at this poiny OMAT is 7 across and npop*nbas long, with no rows that are 6 across

for i,line in enumerate(o_mat):
	line.pop(0) #Each set of columns is proceeded by a column of numbering as well. Here we also remove that. OMat is now 6 across
	for j, element in enumerate(line):
		line[j] = float(element) #convert our energies from strings to floats
		

proper_o_mat = [None]*nbas #initialize what will be the final version of the overlap matrix. We want something nbas x nbas. Currently we are one-dimensional

for i, line in enumerate(proper_o_mat): #iterate over the first set of omat elements, all nbas overlaps for basis functions 1-6
	proper_o_mat[i] = o_mat[i] #the first 6 entries in each row come from the first set of OMat elements

	for j in range(npop-1): #iterate over the remaining sets of 6 by nbas omat elements. Indexing is a bit tricky here
		proper_o_mat[i] = proper_o_mat[i]+o_mat[((j+1)*nbas)+i] #the next 6 entries in the ith row come from the (j+1)th set, where each set is nbas beneath the previous one

#print(proper_o_mat[-1])

#Organize MO coefficients 
#this will almost certainly need some changes for when we have atoms with multiple initials (i.e. In)

#alpha electrons first
n_a_pop = (n_a_elec+5)//6 #by default, qchem prints coefficients for all occupied MOs plus 5 virtual MOs.
						  # if I ever need more or less virtual MOs, I will need to change all this
						  #just like before, qchem prints 6 MOs per row

for i in range(n_a_pop+1): #this deletes the rows that contain the MO indices and MO energies
	#print(coeff[(n_a_pop-i)*(nbas+2)+1])
	#print(coeff[(n_a_pop-i)*(nbas+2)])
	coeff.pop((n_a_pop-i)*(nbas+2)+1)
	coeff.pop((n_a_pop-i)*(nbas+2))
#print(coeff)

#delete the last 3 rows of the alpha section, including "BETA MOLECULAR ORBITAL COEFFICIENTS" 
#print(coeff[nbas*(n_a_pop+1)])
coeff.pop(nbas*(n_a_pop+1))
#print(coeff[nbas*(n_a_pop+1)])
coeff.pop(nbas*(n_a_pop+1))
#print(coeff[nbas*(n_a_pop+1)])
coeff.pop(nbas*(n_a_pop+1))

#note that we have not removed the first four entries in each row, i.e. "73 F 1 s". 
#Ultimately we will want to remove the 1st index.
#When there is only one of an atom type (as in our PF3 example), there is no indexing number after the atom

n_b_pop = (n_a_elec+4)//6 #there is one occupied beta MO than alpha

for i in range(n_b_pop+1): #again, remove eigenvalues and indices
	#print(coeff[nbas*(n_a_pop+1)+(n_a_pop-i)*(nbas+2)+1])
	coeff.pop(nbas*(n_a_pop+1)+(n_a_pop-i)*(nbas+2)+1)
	#print(coeff[nbas*(n_a_pop+1)+(n_a_pop-i)*(nbas+2)])
	coeff.pop(nbas*(n_a_pop+1)+(n_a_pop-i)*(nbas+2))

#remove the single empty line at the end
coeff.pop(-1)


guide = [None]*nbas
for i,line in enumerate(coeff): #now we'll remove the first several entries in each line. Since the ultimate goal is to get a matrix, but maybe I want to hold on to the ordering somewhere
	line.pop(0) #remove the index
	if i < nbas:
		guide[i]=line[0]
	line.pop(0) #remove the atom type
	if i < nbas:
		guide[i]=guide[i]+" "+line[0]
	line.pop(0) #if there is more than one atom of this type, this removes this index. Otherwise it deletes the orbital
	if line[0] == "s" or line[0] == "px" or line[0] == "py" or line[0] == "pz":  # remove the orbital when there's more than one of the atom type
		if i < nbas:
			guide[i]=guide[i]+" "+line[0]
		line.pop(0)
	if line[0] == "d": #for some reason the d orbitals are indexed "d 1" "d 2" etc, so they register as two things you have to remove separately
		if i < nbas:
			guide[i]=guide[i]+" "+line[0]
		line.pop(0)
		if i < nbas:
			guide[i]=guide[i]+" "+line[0]
		line.pop(0)
	if line[0] == "1" or line[0] == "2" or line[0] == "3" or line[0] == "4" or line[0] == "5": # for the d orbitals
		if i < nbas:
			guide[i]=guide[i]+" "+line[0]
		line.pop(0)
	for j, element in enumerate(line): #convert everything left into a float
		line[j] = float(element)

#print(guide)
#separate the alpha and beta MOs. Note that the last set of rows in each will have less than 6 entries
alpha = coeff[:nbas*(n_a_pop+1)]
beta = coeff[nbas*(n_a_pop+1):]

flat_alpha = [None]*nbas #put the alpha MOs into nbas rows of (ultimately) nbas
for i in range(nbas):
	for j in range(n_a_pop+1):
		if j==0:
			flat_alpha[i]=alpha[j*nbas+i]
		else:
			flat_alpha[i]=flat_alpha[i]+alpha[j*nbas+i]

flat_beta = [None]*nbas #put the alpha MOs into nbas rows of (ultimately) nbas
for i in range(nbas):
	for j in range(n_b_pop+1):
		if j==0:
			flat_beta[i]=beta[j*nbas+i]
		else:
			flat_beta[i]=flat_beta[i]+beta[j*nbas+i]

alpha_coefficients=np.array(flat_alpha)
beta_coefficients=np.array(flat_beta)
#print(alpha_coefficients)
np.savez("alpha_co.npz",alpha_coefficients)
np.savez("beta_co.npz", beta_coefficients)

