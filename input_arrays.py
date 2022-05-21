import numpy as np
import functions as fu
#Contains the potential HX designs/layouts

#numbers of tubes
nt_array = np.arange(1,22,1)

#numbers of baffles
nb_array = np.arange(1,20,1)

passes_array = [[ 1,1],[1,2],[2,1],[2,2]]  #Nt = 1 for first two entries



def Lt_calc(nt,Nt):
    Lt_calc = fu.Lt_total_cu/nt - 12e-3 #length of copper tube inside HX calculated by dividing total cu pipe by nt

    #now calculate the maximum permissible tube length
    if Nt == 1:
        a = b = 59e-3   # Header tank length + tube plate + end
    elif Nt == 2:
        a = 59e-3   #Header tank two fit both nozzle
        b = 34e-3   #Header tank for turning

    Lt_max = fu.L_HX_max - (a + b)

    Lt = min(Lt_max, Lt_calc)
    return Lt
    

Lt_array =[[],[]]
for i in nt_array:
    Nt=1
    Lt_array[0].append( round(Lt_calc(i,Nt),3) )
    Nt=2
    Lt_array[1].append( round(Lt_calc(i,Nt),3) )



#pitch spacings between centres

def pitch(nt): 
    #function that gives an approximate Y given to us by another group
    coeffs = [5.06546580e-08, -5.11669291e-06,  1.92046625e-04, -3.39430513e-03, 3.50150832e-02]
    polynomial_fit = 0
    deg = len(coeffs) - 1
    for i in range(deg + 1):
        polynomial_fit += coeffs[i]*nt**(deg - i)
    return polynomial_fit
    #return Dsh/(1.3*np.sqrt(n_tubes))

pitch_array =[]
for i in nt_array:
    pitch_array.append(round(pitch(i),5))

