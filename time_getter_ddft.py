import numpy as np
import sys
from ddft_helper import get_mulliken_charges, get_lowdin_charges, get_becke_charges, run_test, get_energies, get_time

#inputs from the command line
output_file=sys.argv[1]

time = get_time(output_file)
print()
print("CPU Time is ", time, "s")
print()