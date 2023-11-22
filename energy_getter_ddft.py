import numpy as np
import sys
from ddft_helper import get_mulliken_charges, get_lowdin_charges, get_becke_charges, run_test, get_energy, get_time, get_energies

output_file=sys.argv[1]
#gs_file=sys.argv[2]

energy_difference = get_energies(output_file)
#gs_energy = get_energy(gs_file) #use these two when gs and es are in different files
#es_energy = get_energy(output_file)
#energy_difference = es_energy - gs_energy
print()
print("Energy difference is ", energy_difference, "eV")
print()