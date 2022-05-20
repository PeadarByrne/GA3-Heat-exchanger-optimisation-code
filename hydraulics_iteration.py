import functions as fu
import numpy as np


#------Hotside analysis





def hydraulic_h(Lt,nt,Nt):
    #Guess mh
    m_h=0.5
    m_h_old = 0
    p_calc_old = 0
    e_h_target=0.0001
    e=1
    sigma=fu.sigma(nt)

    counter =0

    while(abs(e)>e_h_target and counter<100):
        counter +=1
        

        # m_hl=fu.m_L(m_h)
        # p_pump_h=-0.4713*m_h**2-0.8896*m_h + 0.6381

        v_t=fu.v_t(m_h,nt)
        v_nh=fu.v_n(m_h)
        Re_t=fu.Re_t(m_h,nt)

        f=(1.82*np.log10(Re_t) - 1.64)**-2           #estimation of the friction factor in the copper tubes

        #calculate pressure drop from guessed m_h
        p_t = f*(Lt/fu.d_i)*0.5*fu.rho*v_t**2     #pressure loss along copper tubes from friction
        kc = -0.3952*sigma + 0.4973                  #regression functions from excel for Re=10000 for turbulent flow
        ke = 0.9773*sigma**2 -2.0738*sigma + 0.9983  
        p_e = 0.5*fu.rho*v_t**2*(kc + ke)            #pressure loss caused by entrance exit losses into copper tubes
        p_n = 0.5*fu.rho*v_nh**2    # pressure loss from nozzles entering HX

        p_h = p_t + p_e + p_n   #pressure in pascals
        p_h_calc = p_h/1e5          #pressure in bar

        #m_h = (-0.3086*p_hb**2 -0.6567*p_hb + 0.5493)*fu.rho*1e-3   #regression function from excel spreadsheet correlating the pressure drop across the pump to mass flow
        dp_calc = (p_h_calc - p_calc_old)/(m_h - m_h_old) #Calculate an approximate derivative of p_calc 
        m_h_old = m_h   #store m_h from previous guess
        m_hl =(fu.rho/1000)*m_h #convert to litres/s
        p_h_pump = -0.4713*m_hl**2 - 0.8896*m_hl + 0.6598
        dp_h_pump = -2*.4713*m_hl - 0.8896
        m_h = m_h - (p_h_pump - p_h_calc)/(dp_h_pump - dp_calc)    #calculate new mass flow using newton raphson iteration
        e = p_h_pump - p_h_calc #calculate error
        p_calc_old = p_h_calc   #store previosly calculated pressure for next iteration
      
        if counter == 100:
            raise RuntimeError
    #print(counter)

    # calculated m_h is within the limits of the pumps capabilities
    # if m_h > 0.4583:    #Pump becomes unstead operating beyond this point
    #     raise ValueError('outside the pumps performance limits')
    # elif m_h < 0:
    #     raise ValueError('outside the pumps performance limits')
    return m_h    

#------Coldside analysis


def hydraulic_c(Lt,Y,nb,N,Ns):
    m_c=0.4
    m_c_old =0
    p_calc_old =0
    e_c_target=0.0001
    e=1
    
    pitch_shape = "triangular"

    c , a = fu.pitch(pitch_shape) 
    A_sh = fu.A_sh(Y,nb,Lt) 
    counter =0

    while(abs(e)>e_c_target and counter<=100):

        counter+=1
        #calculate pressure drop from guessed m_c
        v_sh = fu.v_sh(m_c,A_sh) 
        Re_sh = fu.Re_sh(m_c,A_sh)
        vn_c = fu.v_n(m_c)
        p_sh = 4*a*Re_sh**(-0.15)*N*fu.rho*v_sh**2*(nb + 1) #Shell side pressure loss (This has poor validity)
        p_n = 0.5*fu.rho*vn_c**2
        p_turn = 0.5*fu.rho*(v_sh**2)*Ns*nb                 #turning pressure loss
        p_c = p_sh + p_n + p_turn   #calculated pressure from m_c guess
        p_c_calc = p_c/1e5  #convert pressure to bar
        

        dp_calc = (p_c_calc - p_calc_old)/(m_c - m_c_old) #Calculate an approximate derivative of p_calc 
        m_c_old = m_c   #store m_c from previous guess
        m_cl =(fu.rho/1000)*m_c #convert to litres/s
        p_c_pump = -.7843*m_cl**2 - 0.4802*m_cl + 0.6598
        dp_c_pump = -2*.7843*m_cl - 0.4802
        m_c = m_c - (p_c_pump - p_c_calc)/(dp_c_pump - dp_calc)    #calculate new mass flow using newton raphson iteration
        e = p_c_pump - p_c_calc #calculate error
        p_calc_old = p_c_calc   #store previosly calculated pressure for next iteration
      
        if counter == 100:
            raise RuntimeError
    #print(counter)

    # check calculated m_c is within the limits of the pumps capabilities
    # if m_c > 0.5833:    #Pump becomes unstead operating beyond this point
    #     raise ValueError('outside the pumps performance limits')
    # elif m_c < 0:
    #     raise ValueError('outside the pumps performance limits')
    return m_c



# #---------calculate massflow rates
# m_c = hydraulic_c(350e-3,14e-3,9,13,'square')
# print("coldside mass flow rate: {}".format(m_c))
# m_h = hydraulic_h(350e-3,13)
# print("hotside mass flow rate: {}".format(m_h))


