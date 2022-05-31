import numpy as np
import functions as fu
import hydraulics_iteration as hydro
import math

def Thermal_LMTD(m_h, m_c, nt, nb, Y, Lt, Nt, Ns):

    Re_i = fu.Re_t(m_h,nt/Nt)   #Internal tube reynolds number
    A_sh = fu.A_sh(Y,nb,Lt,Ns)  #Shell area between tubes
    Re_o = fu.Re_sh(m_c,A_sh)   #External shell reynolds
   
    pitch_shape = "triangular"
    c , a = fu.pitch_constants(pitch_shape)

    #caculating the overall heat transfer coefficient
    A_i = np.pi * fu.d_i * Lt * nt #sum of inner surface areas of all tubes
    A_o = np.pi * fu.d_o * Lt * nt #sum of outer surface areas of all tubes
    Nu_i = 0.023 * (Re_i**0.8) * (fu.Pr**0.3) #inner Nusselt number
    Nu_o = c * (Re_o**0.6) * (fu.Pr**0.3) #outer Nusselt number  #c is 0.2 for triangular tube pitch and 0.15 for square tube pitch
    h_i = (Nu_i*fu.kw)/fu.d_i
    h_o = (Nu_o*fu.kw)/fu.d_o
    U = 1/((1/h_i) + ((fu.d_i*np.log(fu.d_o/fu.d_i)/(2*fu.kt)))+(fu.d_i/(fu.d_o*h_o)))

    #setting up temperature for iteration
    dT_target = 0.001    #cut off value for change in temperature estimate between iterations (error)
    dT_c = 1    #initialise change in cold temperature output between interations
    dT_h = 1    #initialise change in hot temperature output between interations
    T_h_out=55.27   #Water out estimates
    T_c_out=24.05
    T_c_out_old = T_c_out   #keep the old values to see if values have converged enough
    T_h_out_old = T_h_out   
       
    counter = 0

    #while loop to iteratively solve the  three thermal equations (Eq.1 in handout)
    while (dT_c>dT_target) or (dT_h>dT_target):
        counter += 1
        delta_T_lm = ((fu.T_h_in-T_c_out)-(T_h_out-fu.T_c_in))/(np.log((fu.T_h_in-T_c_out)/(T_h_out-fu.T_c_in)))
      

        #Correction factor for multipass designs
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

        #Solve three  thermal equations for outlet temperatures

        T_c_out = ((F * U * A_o * delta_T_lm)+(fu.T_c_in * m_c * fu.Cp))/(m_c*fu.Cp)     #finds new cold output temp
        T_h_out = (-(F * U * A_o * delta_T_lm)+(fu.T_h_in * m_h * fu.Cp))/(m_h*fu.Cp)    #finds new hot output temp
        
        #iterating
        dT_c = abs(T_c_out-T_c_out_old)     #finds change in estimated cold output temp
        dT_h = abs(T_h_out-T_h_out_old)     #finds change in estimated hot output temp
        T_c_out_old = T_c_out   #store the old values
        T_h_out_old = T_h_out   
        T_h_out = 0.5*T_h_out + 0.5*T_h_out_old #weighted average for new value
        T_c_out = 0.5*T_c_out + 0.5*T_c_out_old

    Q = U*A_o*F*delta_T_lm      #rate of heat transfer
    mc_c = m_c*fu.Cp            #mass flow times specific heat capacity
    mc_h = m_h*fu.Cp
    mc_min = min(mc_h,mc_c)     #find the minimum value of m*cp

    #find effectiveness using the fluid with minimum m*cp
    if mc_min == mc_c :
        e=(T_c_out-fu.T_c_in)/(fu.T_h_in-fu.T_c_in)
    else:
        e=(fu.T_h_in-T_h_out)/(fu.T_h_in-fu.T_c_in)

    #Q =fudge*Q
    return e,Q


def Thermal_NTU(m_h, m_c, nt, nb, Y, Lt, Ns):

    Re_i = fu.Re_t(m_h,nt)
    A_sh = fu.A_sh(Y,nb,Lt,Ns) 
    Re_o = fu.Re_sh(m_c,A_sh)

    pitch_shape = "triangular"

    c , a = fu.pitch_constants(pitch_shape)

    #caculating the overall heat transfer coefficient
    A_i = np.pi * fu.d_i * Lt * nt #sum of inner surface areas of all tubes
    A_o = np.pi * fu.d_o * Lt * nt #sum of inner surface areas of all tubes
    Nu_i = 0.023 * (Re_i**0.8) * (fu.Pr**0.3) #inner Nusselt number
    Nu_o = c * (Re_o**0.6) * (fu.Pr**0.3) #outer Nusselt number  #c is 0.2 for triangular tube pitch and0.15 for square tube pitch
    h_i = (Nu_i*fu.kw)/fu.d_i
    h_o = (Nu_o*fu.kw)/fu.d_o
    U = 1/((1/h_i) + ((fu.d_i*np.log(fu.d_o/fu.d_i)/(2*fu.kt)))+(fu.d_i/(fu.d_o*h_o)))

    #finding the min and max m*cp
    mc_c = m_c*fu.Cp  
    mc_h = m_h*fu.Cp
    mc_min = min(mc_h,mc_c) 
    mc_max = max(mc_h,mc_c)

    Rc = mc_min/mc_max    #Ratio of the heat capacities
    NTU = U*A_o/mc_min    #Number of Transfer Units

    e_NTU = (1 - np.exp(-NTU*(1 - Rc)))/(1 - Rc*np.exp(-NTU*(1 - Rc)))  #effectiveness equation from 3A6 handout

    Q_max= mc_min*(fu.T_h_in - fu.T_c_in)
    Q = e_NTU*Q_max
    return e_NTU,Q

