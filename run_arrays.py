import functions as fu
import validity_check as check
import thermal_iteration as thermal
import hydraulics_iteration as hydro
import input_arrays as input

#Function runs simulations for geometries in input arrays
def run_optimisation(shape,nt,nt_cross,l,lt,Y):
    count = 0
    length = len(shape)
    while count >= length:
