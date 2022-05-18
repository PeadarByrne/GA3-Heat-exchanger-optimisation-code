import functions as fu
import numpy as np


#------Hotside analysis





def hydraulic_h(Lt,nt):
    #Guess mh
    m_h=0.5
    e_h_target=0.0001
    e=1
    sigma=fu.sigma(nt)

    counter =0

    while(e>e_h_target and counter<10000):
        counter +=1
        m_h_old = m_h

        # m_hl=fu.m_L(m_h)
        # p_pump_h=-0.4713*m_h**2-0.8896*m_h + 0.6381

        v_t=fu.v_t(m_h,nt)
        v_nh=fu.v_n(m_h)
        Re_t=fu.Re_t(m_h,nt)

        f=(1.82*np.log10(Re_t) - 1.64)**-2           #estimation of the friction factor in the copper tubes

        p_t = f*(Lt/fu.d_i)*0.5*fu.rho*v_t**2     #pressure loss along copper tubes from friction
        kc = -0.3952*sigma + 0.4973                  #regression functions from excel for Re=10000 for turbulent flow
        ke = 0.9773*sigma**2 -2.0738*sigma + 0.9983  
        p_e = 0.5*fu.rho*v_t**2*(kc + ke)            #pressure loss caused by entrance exit losses into copper tubes
        p_n = 0.5*fu.rho*v_nh**2

        p_h = p_t + p_e + p_n   #pressure in pascals
        p_hb = p_h/1e5          #pressure in bar
        m_h = (-0.3086*p_hb**2 -0.6567*p_hb + 0.5493)*fu.rho*1e-3   #regression function from excel spreadsheet correlating the pressure drop across the pump to mass flow

        e=abs(m_h-m_h_old)
        m_h = 0.5*(m_h_old + m_h)
        
        if counter == 10000:
            raise RuntimeError
    print(counter)
    # check calculated m_h is within the limits of the pumps capabilities
    # if m_h > 0.4583:
    #     raise ValueError('outside the pumps performance limits')
    # elif m_h < 0.0694:
    #     raise ValueError('outside the pumps performance limits')
    return m_h    

#------Coldside analysis


def hydraulic_c(Lt,Y,nb,N,pitch_shape):
    m_c=0.4
    e_c_target=0.0001
    e=1
  
    c , a = fu.pitch(pitch_shape)
        
    A_sh = fu.A_sh(Y,nb,Lt) 
    counter =0
    while(abs(e)>e_c_target and counter<=1000):
        counter+=1
        m_c_old = m_c

        #calculate pressure drop from input m_c
        v_sh = fu.v_sh(m_c,A_sh) 
        Re_sh = fu.Re_sh(m_c,A_sh)
        vn_c = fu.v_n(m_c)
        p_sh = 4*a*Re_sh**(-0.15)*N*fu.rho*v_sh**2*(nb + 1) #Shell side pressure loss (This has poor validity)
        p_n = 0.5*fu.rho*vn_c**2
        p_c_guess = p_sh + p_n    #calculated pressure from m_c guess
        p_cb_guess = p_c_guess/1e5  #convert pressure to bar

        #new iterator
        # #calculate the pressure loss associated with the pump for this pressure loss
        # m_cl= fu.m_L(m_c)    #convert kg/s to l/s
        # p_cb_pump = -.7843*m_cl**2 - 0.4802*m_cl + 0.6598   #pump pressure in bar

        # e = p_cb_pump - p_cb_guess  #error in bar
        # print(e,m_c)
        
        # de = -1.5686*m_cl - 0.4802
        # m_c = m_c  - e/de

        #old iterator
        m_c = -0.6221*p_cb_guess**2 - 0.506*p_cb_guess + 0.6463
        e = abs(m_c-m_c_old)
        m_c = 0.5*(m_c_old + m_c)
        

        if counter == 1000:
            raise RuntimeError
    print(counter)

    # # check calculated m_c is within the limits of the pumps capabilities
    # if m_c > 0.5833:
    #     raise ValueError('outside the pumps performance limits')
    # elif m_c < 0.1708:
    #     raise ValueError('outside the pumps performance limits')
    return m_c



# #---------calculate massflow rates
m_c = hydraulic_c(350e-3,14e-3,9,13,'square')
print("coldside mass flow rate: {}".format(m_c))
m_h = hydraulic_h(350e-3,13)
print("hotside mass flow rate: {}".format(m_h))


