from operator import length_hint
from matplotlib.pyplot import vlines
import functions as fu
from input_arrays import Y_array

#check total length of HX
def CheckHXlength(l):
    if l > fu.l_max:
        print('HX length too big')
        raise ValueError('The heat exchanger is too long')


#check that we have enough copper tube
def CheckTubeLength(Lt,nt):
    Lt_used = (Lt + fu.Lt_extra) * nt
    if Lt_used > fu.Lt_total:
        print('Tube length too big')
        raise ValueError('This design uses too much copper pipe')


#check that tubes fit in shell
def CheckTubesInShell(nt_cross,Y):
    d_t_total = (nt_cross +1)*Y
    if d_t_total > fu.d_sh:
        print('Tubes dont fit inside shell')
        raise ValueError('The pipes do not fit in the shell')


#check that HX in not overweight
def CheckMass(Lt,l,nt,nb):
    mass_tubes = (Lt+fu.Lt_extra)*fu.mlt #total mass of copper tubes used
    mass_shell = l*fu.mls    #total mass of shell
    mass_nozz = 4*fu.m_n    #total mass of nozzles
    A_end = fu.A(fu.d_sh)     #area of an end plate
    A_plate = A_end - (nt*fu.A(fu.d_o))  #area of a tube end plate
    mass_plates = ((2*A_end) + (2*A_plate))*fu.map  #total mass of end plates and tube end plates
    #baffle area approximated to half the shell area
    A_baffle = 0.5*A_end    #area of a bafflew
    mass_baffles = nb*A_baffle   #total mass of baffles
    #total mass of the heat exchanger
    mass_total = mass_tubes+mass_shell+mass_nozz+mass_plates+mass_baffles
    if mass_total > fu.mass_limit:
        print('Design is overweight')
        raise ValueError('This design is overweight')

#check end chamber room/space for end nozzles
def CheckEnds(l,Lt):
    l_endspace = (l-Lt)/2 #length of end chambers
    if l_endspace < fu.l_endspace_min:
        print('Does not allow sufficient spaces for nozzles at either end')
        raise ValueError('Does not allow sufficient spaces for nozzles at either end')


#check closeness of holes in plates
def CheckHoles(Y):
    holespace = Y - fu.d_o
    if holespace < fu.holespace_min:
        print('Holes in the tube end plates are too close together')
        raise ValueError('Holes in the tube end plates are too close together')

#Function to check all input arrays are equal length
def CheckArrayLength(shape_array,nt_array,nt_cross_array,l_array,lt_array,Y_array):
    length = len(shape_array)
    if length != len(nt_array):
        print('nt_array is not the same length as shape_array')
        raise ValueError('nt_array is not the same length as shape_array')
    if length != len(nt_cross_array):
        print('nt_cross_array is not the same length as shape_array')
        raise ValueError('nt_cross_array is not the same length as shape_array')
    if length != len(l_array):
        print('nt_array is not the same length as shape_array')
        raise ValueError('nt_array is not the same length as shape_array')
    if length != len(lt_array):
        print('lt_array is not the same length as shape_array')
        raise ValueError('lt_array is not the same length as shape_array')
    if length != len(Y_array):
        print('Y_array is not the same length as shape_array')
        raise ValueError('Y_array is not the same length as shape_array')


#Function that runs all checks for one design (run a separate array lenghts check)
def CheckDesign(l,Lt,nt,nt_cross,Y,nb):
    CheckHXlength(l)
    CheckTubeLength(Lt,nt)
    CheckTubesInShell(nt_cross,Y)
    CheckMass(Lt,l,nt,nb)
    CheckEnds(l,Lt)
    CheckHoles(Y)