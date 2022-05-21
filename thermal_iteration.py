import numpy as np
import functions as fu
import hydraulics_iteration as hydro
import math

'''
#made up values to test thermal, final code will need to pull these from hydaulics
m_c = 0.5      #example value of cold water mass flow rate
m_h = 0.48     #example value of hot water mass flow rate
#These mass flow rates need to be different to eachother to prevent dividing by zero
'''
   

def Thermal_LMTD(m_h, m_c, nt, nb, Y, Lt, Nt, Ns):
    #Find Reynolds numbers
    Re_i = fu.Re_t(m_h,nt)
    A_sh = fu.A_sh(Y,nb,Lt,Ns) 
    Re_o = fu.Re_sh(m_c,A_sh)

    pitch_shape = "triangular"

    c , a = fu.pitch_constants(pitch_shape)

    A_i = np.pi * fu.d_i * Lt * nt #sum of inner surface areas of all tubes
    Nu_i = 0.023 * (Re_i**0.8) * (fu.Pr**0.3) #inner Nusselt number
    Nu_o = c * (Re_o**0.6) * (fu.Pr**0.3) #outer Nusselt number  #c is 0.2 for triangular tube pitch and0.15 for square tube pitch
    h_i = (Nu_i*fu.kw)/fu.d_i
    h_o = (Nu_o*fu.kw)/fu.d_o
    U = 1/((1/h_i) + ((fu.d_i*np.log10(fu.d_o/fu.d_i)/(2*fu.kt)))+(fu.d_i/(fu.d_o*h_o)))


    
    dT_target = 0.01    #cut off value for change in temperature estimate between iterations
    dT_c = 1    #initialise change in cold temperature output between interations
    dT_h = 1    #initialise change in hot temperature output between interations

    #Water out estimates
    T_h_out=55.27
    T_c_out=24.05
    T_c_out_old = T_c_out
    T_h_out_old = T_h_out   #keep the old values to see if values have converged enough
       

    #set up counter to check if stuff is broken
    counter = 0
    while (dT_c>dT_target) or (dT_h>dT_target):
        counter += 1

        if (Nt==1) and (Ns==1): #one shell one pass
            F = 1
                    
        elif Nt > 1: # if we have more than 1 tube pass, need F
            R = (fu.T_h_in-T_h_out)/(T_c_out-fu.T_c_in)
            P = (T_c_out-fu.T_c_in)/(fu.T_h_in-fu.T_c_in)

            if R!= 1:
                W = ((1-P*R)/(1-P))**(1/Ns)
                S = ((R**2 +1)**0.5)/(R-1)
                F = (S*np.log(W))/np.log((1+W-S+S*W)/(1+W+S-(S*W)))
            elif R==1: #must take Ns=1
                W_dash = (Ns - Ns*P)/(Ns-Ns*P+P)
                F = np.sqrt(2)*((1-W_dash)/W_dash)/np.log(((W_dash/(1-W_dash))+(1/np.sqrt(2)))/((W_dash/(1-W_dash))-(1/np.sqrt(2))))
        
        delta_T_lm = ((fu.T_h_in-T_c_out)-(T_h_out-fu.T_c_in))/(np.log((fu.T_h_in-T_c_out)/(T_h_out-fu.T_c_in)))
        T_c_out = ((F * U * A_i * delta_T_lm)+(fu.T_c_in * m_c * fu.Cp))/(m_c*fu.Cp)     #finds new cold output temp
        T_h_out = (-(F * U * A_i * delta_T_lm)+(fu.T_h_in * m_h * fu.Cp))/(m_h*fu.Cp)    #finds new hot output temp
        
        #iterating
        dT_c = abs(T_c_out-T_c_out_old)     #finds change in estimated cold output temp
        dT_h = abs(T_h_out-T_h_out_old)     #finds change in estimated hot output temp
        T_c_out_old = T_c_out
        T_h_out_old = T_h_out   #store the old values 
        T_h_out = 0.5*T_h_out + 0.5*T_h_out_old #weighted average for new value
        T_c_out = 0.5*T_c_out + 0.5*T_c_out_old
        #print(counter)
        
    print("Correction factor:", F)
    print("T_c_out", T_c_out)
    print("T_h_out", T_h_out)
    

    Q = U*A_i*F*delta_T_lm      #rate of heat transfer
    mc_c = m_c*fu.Cp  
    mc_h = m_h*fu.Cp
    mc_min = min(mc_h,mc_c)     #find the minimum value of mcp
    #find effectiveness using the minimum fluid
    
    if mc_min == mc_c :
        e=(T_c_out-fu.T_c_in)/(fu.T_h_in-fu.T_c_in)
    else:
        e=(fu.T_h_in-T_h_out)/(fu.T_h_in-fu.T_c_in)
    
    #Find effectiveness using Q
    #E=Q/(mc_min*(fu.T_h_in-fu.T_c_in))

    # print('No. of iterations = ',counter)
    # print('Cold output temperature = ',T_c_out)
    # print('Hot output temperature = ',T_h_out)
    # print('Rate of heat transfer = ',Q)
    # print('Effectiveness = ',e)
    #print('Or maybe effectiveness = ',E)
    '''
    #junk for seeing relvant P and R for correction factor F
    T1 = fu.T_c_in
    T2 = T_c_out
    t1 = fu.T_h_in
    t2 = T_h_out
    R = (T1-T2)/(t2-t1)
    P = (t2-t1)/(T1-t1)
    print('R = ',R)
    print('P = ',P)   
    '''

    return e,Q



def Thermal_NTU(m_h, m_c, nt, nb, Y, Lt, Ns):
    Re_i = fu.Re_t(m_h,nt)
    A_sh = fu.A_sh(Y,nb,Lt,Ns) 
    Re_o = fu.Re_sh(m_c,A_sh)

    pitch_shape = "triangular"

    c , a = fu.pitch_constants(pitch_shape)

    A_i = np.pi * fu.d_i * Lt * nt #sum of inner surface areas of all tubes
    Nu_i = 0.023 * (Re_i**0.8) * (fu.Pr**0.3) #inner Nusselt number
    Nu_o = c * (Re_o**0.6) * (fu.Pr**0.3) #outer Nusselt number  #c is 0.2 for triangular tube pitch and0.15 for square tube pitch
    h_i = (Nu_i*fu.kw)/fu.d_i
    h_o = (Nu_o*fu.kw)/fu.d_o
    U = 1/((1/h_i) + ((fu.d_i*np.log(fu.d_o/fu.d_i)/(2*fu.kt)))+(fu.d_i/(fu.d_o*h_o)))

    mc_c = m_c*fu.Cp  
    mc_h = m_h*fu.Cp
    mc_min = min(mc_h,mc_c) 
    mc_max = max(mc_h,mc_c)

    Rc = mc_min/mc_max    #Ratio of the heat capacities
    NTU = U*A_i/mc_min    #Number of Transfer Units

    e_NTU = (1 - np.exp(-NTU*(1 - Rc)))/(1 - Rc*np.exp(-NTU*(1 - Rc)))

    Q_max= mc_min*(fu.T_h_in - fu.T_c_in)
    Q = e_NTU*Q_max
    return e_NTU,Q


# e_NTU, Q_NTU = Thermal_NTU(hydro.m_h,hydro.m_c, 13, 9, 14e-3, 350e-3, 'square')
# print("Effectiveness (NTU): {}".format(e_NTU))
# print("Q (NTU): {}".format(Q_NTU))

# #function inputs: m_h, m_c, nt, nb, Y, Lt, pitch_shape
# e_LMTD,Q_LMTD = Thermal_LMTD(hydro.m_h,hydro.m_c, 13, 9, 14e-3, 350e-3, 'square')
# print("Effectiveness (LMTD): {}".format(e_LMTD))
# print("Q (LMTD): {}".format(Q_LMTD))
