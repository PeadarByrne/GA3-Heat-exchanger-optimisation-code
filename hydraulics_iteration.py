import functions as fu
import numpy as np
import math


#------Hotside analysis





def hydraulic_h(Lt,nt,Nt):
    #Guess mh
    m_h=0.5
    m_h_old = 0
    p_calc_old = 0
    e_h_target=0.0001
    e=1

    #two passes creates an equivalent HX with nt/2 of length 2Lt
    if Nt == 2:
        nt = nt/2
        Lt = 2*Lt

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
        p_t = f*(Lt/fu.d_i)*0.5*fu.rho*v_t**2   #pressure loss along copper tubes from friction
        kc = 0.4 - 0.4*sigma                          #regression functions from excel for Re=inf for turbulent flow
        ke = (1-sigma)**2 
        #kc = -0.3952*sigma + 0.4973                  #regression functions from excel for Re=10000 for turbulent flow
        #ke = 0.9773*sigma**2 -2.0738*sigma + 0.9983  
        #print("kc,ke",kc,ke)
        p_e = 0.5*fu.rho*v_t**2*(kc + ke)*Nt            #pressure loss caused by entrance exit losses into copper tubes - updated with Nt
        p_n = fu.rho*v_nh**2    # pressure loss from nozzles entering HX

        header_gap = 0.03   #Header gap for a header with no nozzle

        if Nt == 1:
            p_hturn = 0
        elif Nt == 2:
            area_ratio = (nt*0.5*math.pi*(fu.d_i/2)**2)/(header_gap*fu.d_sh)
            v_header = area_ratio * v_t
            p_hturn = 0.5*fu.rho*(v_header**2)

        p_h = p_t + p_e + p_n + p_hturn  #pressure in pascals
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
    print("p_h_calc", p_h_calc)
    print("m_h", m_h)

    # calculated m_h is within the limits of the pumps capabilities
    if m_hl < 0.0694:
        print('hotside-outside the pumps performance limits')
        #raise ValueError('outside the pumps performance limits')
    return m_h    

#------Coldside analysis


def hydraulic_c(Lt,Y,nb,N,Ns):
    m_c=0.4
    m_c_old =0
    p_calc_old =0
    e_c_target=0.0001
    e=1
    
    pitch_shape = "triangular"

    c , a = fu.pitch_constants(pitch_shape) 
    A_sh = fu.A_sh(Y,nb,Lt,Ns) 
    counter =0
    Kt = 1    #Coefficient for turning loss
    while(abs(e)>e_c_target and counter<=100):

        counter+=1
        #calculate pressure drop from guessed m_c
        v_sh = fu.v_sh(m_c,A_sh) 
        Re_sh = fu.Re_sh(m_c,A_sh)
        vn_c = fu.v_n(m_c)
        if Ns == 1:
            p_sh = 4*a*Re_sh**(-0.15)*N*fu.rho*v_sh**2*(nb + 1)*Ns #Shell side pressure loss normal to tubes
            p_turn = Kt*0.5*fu.rho*(v_sh**2)*Ns*nb                  #turning pressure loss
        elif Ns == 2:
            #the losses are doubled as nb represents number of plates and one plate is a baffle on two sides
            p_sh = 4*a*Re_sh**(-0.15)*N*fu.rho*v_sh**2*(nb + 1)*Ns  #Shell side pressure loss normal to tubes
            p_turn = Kt*0.5*fu.rho*(v_sh**2)*Ns*nb                #turning pressure loss
        p_n = 0.5*fu.rho*vn_c**2                            #nozzle losses
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
    print("p_c_calc", p_c_calc)
    print("m_c", m_c)

    #check calculated m_c is within the limits of the pumps capabilities
    if m_cl < 0.1708:
        print('coldside-outside the pumps performance limits')
        #raise ValueError('outside the pumps performance limits')
    return m_c



# #---------calculate massflow rates
# m_c = hydraulic_c(350e-3,14e-3,9,13,'square')
# print("coldside mass flow rate: {}".format(m_c))
# m_h = hydraulic_h(350e-3,13)
# print("hotside mass flow rate: {}".format(m_h))


