#This is a helper file for analyzing delta dft outputs
import numpy as np
import sys

def run_test(inputfile, target):
    '''
    This function looks at the output file and decides if the job actually worked the way it is supposed to 
    It checks the User-specified guess orbitals, the occupied alpha MO energies, and the unoccupied beta MO energies

    Inputs:  inputfile  -- name of qchem input/output file with geometry
             target -- core electron to be excited
    Outputs: test -- true if all three tests were passed, false otherwise
    '''
    print()
    with open(inputfile,'r') as out:
        job = 1
        test1 = False
        ready_test1 = False
        check_test1 = False
        test2 = False
        ready_test2 = False
        check_test2 = False
        test3 = False
        ready_test3 = False
        check_test3 = False
        for line in out:
            if line.find("Have a nice day")!= -1:
                job = 2

            if job==2 and line.find("User-specified occupied guess orbitals will be used")!= -1:
                ready_test1 = True
            if check_test1:
                if line.find(" " + target + " ") != -1:
                    print("Wrong electron was sent up!")
                else:
                    test1 = True
                    print("Test 1 passed!")
                ready_test1 = False
                check_test1 = False
            if ready_test1 and line.find("Beta:")!= -1:
                check_test1 = True

            if job==2 and line.find("Alpha MOs")!= -1:
                ready_test2 = True  
            if check_test2:
                line_test = line.strip().split()
                line_test = np.array(line_test)
                line_test = line_test[:].astype(float)
                line_stddev = np.std(line_test)
                if (line_test[1] - line_test[0]) > line_stddev*3:
                    test2 = True
                    print("Test 2 passed!")
                else:
                    print("Singly occupied core MO isn't the lowest in energy!")
                ready_test2 = False
                check_test2 = False
            if ready_test2 and line.find("-- Occupied --")!= -1:     
                check_test2 = True

            if job==2 and line.find("Beta MOs")!= -1:
                ready_test3 = True  
            if check_test3:
                line_test = line.strip().split()
                line_test = np.array(line_test)
                line_test = line_test[:].astype(float)
                if (line_test[1] - line_test[0]) > line_stddev*3:
                    test3 = True
                    print("Test 3 passed!")
                else:
                    print("No low energy virtual beta MO!")
                ready_test3 = False
                check_test3 = False
            if ready_test3 and line.find("-- Virtual --")!= -1:     
                check_test3 = True
    if job == 1:
        print("You only ran one job, dumbass! And it didn't even converge!")
    test = test3 and test1 and test2
    print()
    return test 


 


def get_mulliken_charges(inputfile):
    '''
    Function to extract mulliken charges from qchem output

    Inputs:  inputfile  -- name of qchem input/output file with geometry
    Outputs: atom_names -- np array with the atom names (str)
             charge     -- np array with the mulliken charges (float)
    '''
    with open(inputfile,'r') as out:
        #job = 1 #use this when both gs and es calulation are in same file
        job = 2
        copy = False
        ready = False
        charges = []
        skip = False
        i=0
        for line in out:
            if line.find("Have a nice day")!= -1:
            	job = 2
            if job==2 and line.find("Mulliken")!= -1:
            	ready = True
            if copy and line.find("--")!= -1:
            	break
            if copy:
            	charges.append(line.strip().split())
            if ready and line.find("--")!= -1:
            	copy = True

    charges =np.array(charges)
    atom_names = charges[:,1]
    charge = charges[:,2].astype(float)

    return atom_names, charge 

def get_lowdin_charges(inputfile):
    '''
    Function to extract lowdin charges from qchem output

    Inputs:  inputfile  -- name of qchem input/output file with geometry
    Outputs: atoms -- np array with the atom names (str). each atom is represented more than once
             atom_num -- np array with the number of each atom (e.g. the 7 in F 7) (str)
             orbs -- np array of s, p, or d (str)
             occs -- np array of the lowdin occupation number of the lowest alpha molecular orbital (float)
    '''
    #As written this code is actually sorta specific to the electron being looked for - right now it gets electrons 56-68
    with open(inputfile,'r') as out:
        #job = 1
        job = 2
        copy = False
        ready = False
        charges = []
        for line in out:
            if line.find("Have a nice day")!= -1:
                job = 2
            if job==2 and line.find("Partial Lowdin")!= -1:
                ready = True

            #need to change this line for new systems
            if copy and line.find("267       268")!= -1:
                break
            if copy:
                if line.find("In")!= -1 or line.find("Cl")!= -1 or line.find("Br")!= -1 or line.find("Ga")!= -1:
                    line = line[:10]+" "+line[10:]
                if len(line.strip().split()) < 10:
                    line = line[:10]+" 1 "+line[10:]
                charges.append(line.strip().split())

            #need to change this line for new systems
            if ready and line.find("261       262")!= -1:
                copy = True

    charges =np.array(charges)

    atoms = charges[:,1]
    atom_num = charges[:,2]
    orbs = charges[:,3]

    #need to change this line for new systems
    occs = charges[:,6:7].astype(float)

    return atoms, atom_num, orbs, occs

def get_becke_charges(inputfile):
    '''
    Function to extract becke charges from qchem output

    Inputs:  inputfile  -- name of qchem input/output file with geometry
    Outputs: atom_names -- np array with the atom names (str)
             charge     -- np array with the becke charges (float)
    '''
    with open(inputfile,'r') as out:
        #job = 1
        job = 2
        copy = False
        ready = False
        charges = []
        skip = False
        for line in out:
            if line.find("Have a nice day")!= -1:
                job = 2
            if job==2 and line.find("Becke")!= -1:
                ready = True
            if copy and line.find("--")!= -1:
                break
            if copy:
                charges.append(line.strip().split())
            if ready and line.find("[a.u.]")!= -1:
                copy = True

    charges =np.array(charges)
    atom_names = charges[:,1]
    charge = charges[:,2].astype(float)

    return atom_names, charge 

def get_energies(inputfile):
    '''
    Function to extract energies from qchem_output and calculate their difference in eV

    Inputs:  inputfile  -- name of qchem input/output file with geometry
    Outputs: energy difference -- the difference in energy of the core excited state and the ground state, in eV (float)
    '''
    with open(inputfile,'r') as out:
        job = 1
        ground_energy = 0
        excited_energy = 0
        for line in out:
            if line.find("Have a nice day")!= -1:
                job = 2
            if job==1 and line.find("Total energy")!= -1:
                line_array = line.strip().split()
                line_array = np.array(line_array)
                ground_energy = line_array[8].astype(float)
            if job==2 and line.find("Total energy")!= -1:
                line_array = line.strip().split()
                line_array = np.array(line_array)
                excited_energy = line_array[8].astype(float)

    if ground_energy==0 or excited_energy==0:
        print("Something's wrong with the energies!")
        quit()

    energy_difference = excited_energy - ground_energy
    eV_difference = energy_difference*27.211396641308

    return eV_difference 

def get_energy(inputfile):
    '''
    Function to extract the final energy from a qchem output with only one job

    Inputs:  inputfile  -- name of qchem input/output file with geometry
    Outputs: energy -- the  energy of the scf converged state, in eV (float)
    '''
    with open(inputfile,'r') as out:
        for line in out:
            if line.find("Total energy")!= -1:
                line_array = line.strip().split()
                line_array = np.array(line_array)
                energy = line_array[8].astype(float)

    if energy==0:
        print("Something's wrong with the energies!")
        quit()

    eV_energy = energy*27.211396641308

    return eV_energy

def get_time(inputfile):
    '''
    Function to extract cpu time from qchem_output 

    Inputs:  inputfile  -- name of qchem input/output file with geometry
    Outputs: cpu_time -- the cpu time of the last qchem job in the .out file, in seconds (float)
    '''

    with open(inputfile,'r') as out:
        cpu_time = 0
        for line in out:
            if line.find("Total job time:")!= -1:
                line_array = line.strip().split()
                cpu_time = line_array[4][:-6]

    return cpu_time

def run_better_test(inputfile):
    '''
    This function looks at the output file and decides if the job actually worked the way it is supposed to 
    It checks the 2nd job's eiegenenergies and confirms that the orbitals get_low is looking at are actually excited 

    Inputs:  inputfile  -- name of qchem input/output file with geometry
    Outputs: test -- true if test was passed, false otherwise
    '''

    #USER-SPECIFIED
    target_energy_level=261 #69 for small dot #126 for MS dot #124 for neutral MS InP Defect #261 for MS InGaP #306 for MS Cl #81 for MS H #486 for MS Br #119 for MT #263 for protonated InGaP 1 #245 for Magic Cluster

    with open(inputfile,'r') as out:
        #job = 1
        job = 2
        test = False
        copy = False
        ready = False
        alpha_mo_energies = []
        for line in out:
            if line.find("Have a nice day")!= -1:
                job = 2
            elif job==2 and line.find("Alpha MOs")!= -1:
                ready = True
            elif job==2 and ready == True and line.find(" -- Occupied --")!= -1:
                copy = True
            elif copy == True and line.find(" -- Virtual --")!= -1:
                copy = False
                ready = False
            elif copy == True:
                if line.find("*****")!=-1:
                    line = line[:8]+" "+line[8:17]+" "+line[17:26]+" "+line[26:35]+" "+line[35:44]+" "+line[44:53]+" "+line[53:62]+" "+line[62:71]
                alpha_mo_energies.append(line.strip().split())

        flat_energies = sum(alpha_mo_energies,[])

        mean = np.mean([float(flat_energies[target_energy_level-1]), float(flat_energies[target_energy_level]), float(flat_energies[target_energy_level+1])])
        
        
        if abs(mean-float(flat_energies[target_energy_level+2])) > 0.5:
            return True
        else:
            return False
