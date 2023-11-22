import sys
import copy
import numpy as np
import math
import cmath

#I should ask troy about this, but this is currently incomplete. I need the coefficients from all 3 (or 6?) core excited states
alpha_co=sys.argv[1] #alpha MO coefficients of target 
beta_co=sys.argv[2] #beta MO coefficients. The coefficient matrices will end up being block diagonal in alpha and beta
cebes=sys.argv[3] #some file containing the CEBEs of each of our states that I still need to figure out how to make
omat=sys.argv[4] #the overlap matrix may need to be employed here somewhere. 
basis=sys.argv[5] #I think I will need some accounting of the basis set, which will be in the same order for all relevant jobs

#currently using PH3 as our reference, despite being far from perfect
#troy suggested trying all 3 and comparing

#from our MOM calcs. udef2-SVP, HSE06
#i'm not actually sure what order this is in exactly, which is probably an issue
#spin pairs are next to each other, but which orbital is l=1,0,-1 is unclear
#ask troy?
#for now lets say {|1 1/2>,|1 -1/2>,|0 1/2>,|0 -1/2>,|-1 1/2>,|-1 -1/2>,}
H_nr=np.diag([137.0913198,137.0913198,137.0913307,137.0913307,136.9817923,136.9817923])

#from Cavell, R. G.; Tan, K. H. High-Resolution Gas-Phase Core-Level X-Ray Photoelectron Spectroscopy of PH3 and H2S with a Synchrotron Source: Observations of Vibrational Structure on Resolved Spin—Orbit Core (2p) Lines. Chemical Physics Letters 1992, 197 (1), 161–164. https://doi.org/10.1016/0009-2614(92)86040-O.
#first two entries are j=1/2, next 4 are j=3/2
#lets say {|1/2 1/2>,|1/2 -1/2>,|3/2 3/2>,|3/2 1/2>,|3/2 -1/2>,|3/2 -3/2>,}
H_r=np.diag([137.86,137.86, 137.00,137.00,137.00,137.00])


#THE FOLLOWING SECTION IS ALL JUST MATH AND IS THE SAME IRRESPECTIVE OF OUR INPUT

#first, transform Hr into the basis of our calculations (the |ml ms> basis) using the Clebsch-Gordon Coefficients
#our clebsch-gordon matrix, defined in the  |j mj> => |ml ms> direction
#each column is one of our |j mj> basis elements written in the |ml ms> basis
cg_mat=np.zeros((6,6))
cg_mat[:,0]=[0,math.sqrt(2/3),-math.sqrt(1/3),0,0,0] #|1/2 1/2>
cg_mat[:,1]=[0,0,0,-math.sqrt(1/3),math.sqrt(2/3),0] #|1/2 -1/2>
cg_mat[:,2]=[1,0,0,0,0,0] #|3/2 3/2>
cg_mat[:,3]=[0,math.sqrt(1/3),math.sqrt(2/3),0,0,0] #|3/2 1/2>
cg_mat[:,4]=[0,0,0,math.sqrt(2/3),math.sqrt(1/3),0] #|3/2 -1/2>
cg_mat[:,5]=[0,0,0,0,0,1] #|3/2 -3/2>

#Now we transform Hr into the |ml ms> basis
H_r_tilde=np.matmul(cg_mat,np.matmul(H_r,cg_mat.transpose()))

#now we compute the relativistic correction term
dH=H_r_tilde-H_nr

#now we transform the correction from the |ml ms> basis into the solid harmonics (i.e. real px py pz basis)
#or real basis will be ordered as {px 1/2,px -1/2,py 1/2,py -1/2,pz 1/2 ,pz -1/2}
#not 100% sure about the spins here
#note that I'm actuallt writing this in the real => complex direction - I'll need to reverse it
c2r_mat=np.zeros((6,6),dtype=np.complex_)
c2r_mat[:,0]=[math.sqrt(1/2),0,math.sqrt(1/2),0,0,0]
c2r_mat[:,1]=[0,math.sqrt(1/2),0,math.sqrt(1/2),0,0]
c2r_mat[:,2]=[math.sqrt(1/2)*(1/1j),0,-math.sqrt(1/2)*(1/1j),0,0,0]
c2r_mat[:,3]=[0,math.sqrt(1/2)*(1/1j),0,-math.sqrt(1/2)*(1/1j),0,0]
c2r_mat[:,4]=[0,0,0,0,1,0]
c2r_mat[:,5]=[0,0,0,0,0,1]

#now we transform dH to the real basis
dh_tilde= np.matmul(c2r_mat.transpose(),np.matmul(dH,c2r_mat))
print(dh_tilde)

