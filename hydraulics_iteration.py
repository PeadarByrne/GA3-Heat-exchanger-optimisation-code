import functions as fu
import numpy as np


#------Hotside analysis





def hydraulic_h(Lt,nt):
    #Guess mh
    m_h=0.5
    dm_h_target=0.0001
    dm_h=1
    sigma=fu.sigma(nt)

    counter =0

    while(dm_h>dm_h_target and counter<10000):
        counter +=1
        m_h_old = m_h

        # m_hl=fu.m_L(m_h)
        # p_pump_h=-0.4713*m_h**2-0.8896*m_h + 0.6381

        m_t=fu.m_t(m_h,nt)
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

        dm_h=abs(m_h-m_h_old)
        if counter == 10000:
            raise RuntimeError

    # check calculated m_h is within the limits of the pumps capabilities
    if m_h > 0.4583:
        m_h =0.4583
    elif m_h < 0.0694:
        m_h = 0.0694
    return m_h    

#------Coldside analysis


def hydraulic_c(Lt,Y,nb,N,pitch_shape):
    m_c=0.5
    m_c_old=m_c
    dm_c_target=0.0001
    dm_c=1
  
    c , a = fu.pitch(pitch_shape)
        
    A_sh = fu.A_sh(Y,nb,Lt) 
    counter =0
    while(dm_c>dm_c_target and counter<=10000):
        counter+=1
        m_c_old = m_c
        v_sh = fu.v_sh(m_c,A_sh)
        Re_sh = fu.Re_sh(m_c,A_sh)
        vn_c = fu.v_n(m_c)

        p_sh = 4*a*Re_sh**-0.15*N*fu.rho*v_sh**2 #Shell side pressure loss (This has poor validity)
        p_n = 0.5*fu.rho*vn_c**2
        p_c = p_sh + p_n

        p_cb = p_c/1e5
        m_c = -0.6221*p_cb**2 - 0.506*p_cb + 0.6463
        dm_c = m_c-m_c_old
        dm_c = abs(m_c-m_c_old)
        
        if counter == 10000:
            raise RuntimeError

    # check calculated m_c is within the limits of the pumps capabilities
    if m_c > 0.5833:
        m_c =0.5833
    elif m_c < 0.1708:
        m_c = 0.1708
    return m_c


'''
#---------calculate massflow rates
m_c = hydraulic_c(350e-3,14e-3,9,13,'square')
m_h = hydraulic_h(350e-3,13)
print("hotside mass flow rate: {}".format(m_h))
print("coldside mass flow rate: {}".format(m_c))
'''
