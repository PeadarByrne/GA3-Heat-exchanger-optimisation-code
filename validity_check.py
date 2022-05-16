from matplotlib.pyplot import vlines
import functions as fu

#check total length of HX
def CheckHXlength(l):
    if l > fu.l_max:
        raise ValueError('The heat exchanger is too long')


#check that we have enough copper tube
def CheckTubeLength(Lt,nt):
    Lt_used = (Lt + fu.Lt_extra) * nt
    if Lt_used > fu.Lt_total:
        raise ValueError('This design uses too much copper pipe')


#check that tubes fit in shell
def CheckTubesInShell(nt_cross,Y):
    d_t_total = (nt_cross +1)*Y
    if d_t_total > fu.d_sh:
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
        raise ValueError('This design is overweight')

#check end chamber room/space for end nozzles
def CheckEnds(l,Lt):
    l_endspace = (l-Lt)/2 #length of end chambers
    if l_endspace < fu.l_endspace_min:
        raise ValueError('Does not allow sufficient spaces for nozzles at either end')


#check closeness of holes in plates
def CheckHoles(Y):
    holespace = Y - fu.d_o
    if holespace > fu.holespace_min:
        raise ValueError('Holes in the tube end plates are too close together')


def CheckDesign(l,Lt,nt,nt_cross,Y,nb):
    CheckHXlength(l)
    CheckTubeLength(Lt,nt)
    CheckTubesInShell(nt_cross,Y)
    CheckMass(Lt,l,nt,nb)
    CheckEnds(l,Lt)
    CheckHoles(Y)