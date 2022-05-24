from operator import length_hint
from matplotlib.pyplot import vlines
import functions as fu


#check that HX in not overweight
def CheckMass(Lt,nt,nb,Nt,Ns):
    
    mass_tubes = (Lt+fu.Lt_extra)*fu.mlt*nt #total mass of copper tubes used
    mass_nozz = 4*fu.m_n    #total mass of nozzles
    A_end = fu.A(fu.d_sh)     #area of an end plate
    A_plate = A_end - (nt*fu.A(fu.d_o))  #area of a tube end plate
    mass_plates = ((2*A_end) + (2*A_plate))*fu.map  #total mass of end plates and tube end plates
    #baffle area approximated to half the shell area
    A_baffle = 0.5*A_end    #area of a baffle
    mass_baffles = nb*A_baffle*fu.mab   #total mass of baffles
    
    if Nt == Ns == 1:
        #both full size end chambers with nozzles
        l=Lt+0.1
        mass_splitter=0
    elif Nt==2 and Ns==1:
        #One smaller end chamber
        l=Lt+0.08
        #mass of splitter in end chamber
        mass_splitter = 0.05*fu.d_sh*fu.mab
    elif Nt==2 and Ns==2:
        #One smaller end chamber
        l=Lt+0.08
        #mass of splitter in end chamber and 
        mass_splitter = (0.05 + Lt)*fu.d_sh*fu.mab

    mass_shell = l*fu.mls    #total mass of shell, including around end chambers
    #total mass of the heat exchanger
    mass_total = mass_tubes+mass_shell+mass_nozz+mass_plates+mass_baffles+mass_splitter
    if mass_total > fu.mass_limit:
        print("Design is overweight")
        raise ValueError("This design is overweight")




#check closeness of holes in plates
def CheckHoles(Y):
    holespace = Y - fu.d_o
    if holespace < fu.holespace_min:
        print("Holes in the tube end plates are too close together")
        raise ValueError("Holes in the tube end plates are too close together")

