import numpy as np
import functions as fu
#Contains the potential HX designs/layouts

#string descriptions of pitch shape
shape_array = ["square","square","square","square","square","square","triangular","triangular","triangular","triangular"]

#numbers of tubes
nt_array = [4,5,9,12,13,16,3,7,13,19]

#number of tubes in longest straight line or equivalent for funky layouts
nt_cross_array = [2.828427125,3,4.242640687,4.16227766,5,5.656854249,2,3,4.464101615,5]

#lengths of shell
l_array = [0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35]

#lengths of tubes
#lt_array = [0.243,0.243,0.243,0.243,0.243,0.21875,0.243,0.243,0.243,0.21875]

def lt_array_calc(nt_array):
    l_array=[]
    for i in nt_array:
        l=fu.Lt_total/i
        if l>0.243:
            l_array.append(0.243)
        else:
            l_array.append(l)
    return l_array

lt_array = lt_array_calc(nt_array)   
#print(lt_array)

#pitch spacings between centres
Y_array = [1.67E-02,1.60E-02,1.22E-02,1.24E-02,1.07E-02,9.61E-03,2.13E-02,1.60E-02,1.17E-02,1.07E-02]

#number of baffles
nb_array = np.arange(0,5,1)
