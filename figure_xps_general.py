import numpy as np
from pdos_helper import dos_grid_general,get_alpha,get_ao_ind, get_ind_ao_underc
from matplotlib import pyplot as plt
import random
import pandas as pd
import sys
import math
import scipy.special

#Specify the full width half maximum. Should be changed manually
fwhm = 0.5
sigma = fwhm / 2.355

#read excel file
#file format should be: 
#first sheet should have the first row be Excitation	Atom	Number	Energy (eV) with the subsequent columns. Undesirable rows should be deleted
# second sheet should have each column be a different "type" of P, with just energies underneath it (1st row are labels)
file=sys.argv[1]

#set plot title
title = sys.argv[2]

#get full XPS data
df_full = pd.read_excel(file,sheet_name=0)
cebes=[]
column=df_full.columns[3]
for i, row in df_full.iterrows():
	cebes.append(float(row[column]))

#get sub-plot data
df_sub = pd.read_excel(file,sheet_name=1)
sub_cebes = [[] for i in range(df_sub.shape[1])]
i = 0
names = []
for name,data in df_sub.iteritems():
	names.append(name)
	for cebe in data.values:
		if not math.isnan(cebe):
			sub_cebes[i].append(float(cebe))
	i = i+1

#set grid
grid_max = round(max(cebes))+5
grid_min = round(min(cebes))-5
E_grid = np.arange(grid_min,grid_max,0.01)

#make full XPS
E_grid_reshape=np.broadcast_to(E_grid,(len(cebes),len(E_grid)))
cebes_reshape=np.broadcast_to(cebes,(len(E_grid),len(cebes))).T
deltaE=E_grid_reshape-cebes_reshape

voigt=scipy.special.voigt_profile(deltaE,0.2,0.121)
exp_eorb=np.sum(voigt,axis=0)
#deltaE2 = np.power(deltaE,2)
#exp_eorb = np.exp(-(deltaE2)/(2*sigma**2))/np.sqrt(2*np.pi*sigma**2)
#exp_eorb=np.sum(exp_eorb,axis=0)

#make subplot XPS
exp_eorbs=[]
for i,cebes_i in  enumerate(sub_cebes):
	if len(cebes_i)>0:
		E_grid_reshape1=np.broadcast_to(E_grid,(len(cebes_i),len(E_grid)))
		cebes_reshape1=np.broadcast_to(cebes_i,(len(E_grid),len(cebes_i))).T
		deltaE1=E_grid_reshape1-cebes_reshape1

		voigt1=scipy.special.voigt_profile(deltaE1,0.2,0.121)
		exp_eorb1=np.sum(voigt1,axis=0)
		#deltaE21 = np.power(deltaE1,2)
		#exp_eorb1 = np.exp(-(deltaE21)/(2*sigma**2))/np.sqrt(2*np.pi*sigma**2)
		#exp_eorb1=np.sum(exp_eorb1,axis=0)
		exp_eorbs.append(exp_eorb1)
		print(names[i],"has average CEBE",round(np.average(cebes_i),3))
	else:
		exp_eorbs.append([])

#Plot
plt.figure()
plt.style.use('tableau-colorblind10')
plt.plot(E_grid,exp_eorb,'C0',label='Full XPS')

#CB_color_cycle = ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3','#999999', '#e41a1c', '#dede00']

for i,name in enumerate(names):
	if len(sub_cebes[i])>0:
	#plt.plot(E_grid,exp_eorbs[i],CB_color_cycle[i+1],label=name)
		plt.plot(E_grid,exp_eorbs[i],'C'+str(i+1),label=name)
	#if i==8 or i==6:
	#	plt.plot(E_grid,exp_eorbs[i],'C'+str(5),label=name)
	#elif i < 3:
	#	plt.plot(E_grid,exp_eorbs[i],'C'+str(1),label=name)
	#elif i < 9:
	#	plt.plot(E_grid,exp_eorbs[i],'C'+str(2),label=name)
	#else:
	#	plt.plot(E_grid,exp_eorbs[i],'C'+str(4),label=name)

plt.legend()
plot_max = grid_max-3
plot_min = grid_min+3
y_max = round(max(exp_eorb))+5
plt.xlim(plot_max,plot_min)
plt.ylim(0,y_max)
plt.title(title)
plt.ylabel('CPS')
plt.xlabel('CEBE (eV)')
plt.savefig('spectrum.pdf')
plt.show()