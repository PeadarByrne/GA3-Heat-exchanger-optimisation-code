from matplotlib.pyplot import vlines
import functions as fu

#check total length of HX
if fu.l > fu.l_max:
    raise ValueError('The heat exchanger is too long')


#check that we have enough copper tube
Lt_used = (fu.Lt + fu.Lt_extra) * fu.nt
if Lt_used > fu.Lt_total:
    raise ValueError('This design uses too much copper pipe')


#check that tubes fit in shell
d_t_total = (fu.nt_cross +1)*fu.Y
if d_t_total > fu.d_sh:
    raise ValueError('The pipes do not fit in the shell')


#check that HX in not overweight
mass_tubes = (fu.Lt+fu.Lt_extra)*fu.mlt #total mass of copper tubes used
mass_shell = fu.l*fu.mls    #total mass of shell
mass_nozz = 4*fu.m_n    #total mass of nozzles
A_end = fu.A(fu.sh)     #area of an end plate
A_plate = A_end - (fu.nt*fu.A(fu.d_o))  #area of a tube end plate
mass_plates = ((2*A_end) + (2*A_plate))*fu.map  #total mass of end plates and tube end plates
#baffle area approximated to half the shell area
A_baffle = 0.5*A_end    #area of a bafflew
mass_baffles = fu.nb*A_baffle   #total mass of baffles
#total mass of the heat exchanger
mass_total = mass_tubes+mass_shell+mass_nozz+mass_plates+mass_baffles
if mass_total > fu.mass_limit:
    raise ValueError('This design is overweight')

