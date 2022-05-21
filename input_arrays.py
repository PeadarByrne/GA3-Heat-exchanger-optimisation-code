import numpy as np
import functions as fu
#Contains the potential HX designs/layouts

#numbers of tubes
nt_array = [4,5,9,12,13,16,3,7,13,19]

#number of tubes in longest straight line or equivalent for funky layouts
nt_cross_array = [2.828427125,3,4.242640687,4.16227766,5,5.656854249,2,3,4.464101615,5]

#lengths of shell
l_array = [0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35]

#lengths of tubes
#lt_array = [0.243,0.243,0.243,0.243,0.243,0.21875,0.243,0.243,0.243,0.21875]

def Lt_array_calc(nt_array,Nt_array):
    Lt_array=[]
    if Nt_array[i] == 1:
        a = b = 59e-3   # Header tank length + tube plate + end
    elif Nt_array[i] == 2:
        a = 59e-3   #Header tank two fit both nozzle
        b = 34e-3   #Header tank for turning
        Lt_calc = fu.Lt_total_cu/i - 12e-3 #length of copper tube inside HX calculated by dividing total cu pipe by nt
    Lt_max = fu.L_HX_max - (a + b)
    
    for i in range(nt_array):

        if Lt_calc > Lt_max:
            Lt_array.append(Lt_max)
        else:
            Lt_array.append(Lt_calc)
    return Lt_array

Lt_array = Lt_array_calc(nt_array,Nt=1)   
#print(lt_array)

#pitch spacings between centres
Y_array = [1.67E-02,1.60E-02,1.22E-02,1.24E-02,1.07E-02,9.61E-03,2.13E-02,1.60E-02,1.17E-02,1.07E-02]

#number of baffles
nb_array = np.arange(0,5,1)
