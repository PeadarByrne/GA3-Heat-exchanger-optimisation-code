import numpy as np
import functions as fu
#Contains the potential HX designs/layouts

#numbers of tubes
nt_array = np.arange(2,22,1)

#numbers of baffles
nb_array = [np.arange(2,20,1),np.arange(2,12,1)]
#nb_array_1 = [np.arange(2,20,1)]
#nb_array_2 = [np.arange(2,12,1)]
#nb_array = np.arange(2,20,1)


#[Nt,Ns]
passes_array = [[ 1,1],[2,1],[2,2],[4,1],[4,2]]
 

def Lt_calc(nt,Nt):
    Lt_calc = fu.Lt_total_cu/nt - 12e-3 #length of copper tube inside HX calculated by dividing total cu pipe by nt
    #12e-3 includes extra copper tube length fr width of end plate and extra poking out the end
    #now calculate the maximum permissible tube length
    if Nt == 1:
        a = b = 59e-3   # Header tank length + tube plate + end
    elif Nt == 2:
        a = 57e-3   #Header tank two fit both nozzle
        b = 29e-3   #Header tank for turning

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

def choose_N(nt,Nt):
    if Nt == 2:
        N = 3
    elif Nt == 1:
        if nt < 14:
            N=3
        else:
            N=4
    else:
        if nt>21:
            N=4
        else:
            N=3
    return N