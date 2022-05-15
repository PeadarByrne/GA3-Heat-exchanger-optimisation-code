import functions as fu
import numpy as np


#------Hotside analysis

#Guess mh
sigma=fu.sigma()


def hydraulic_h():
    m_h=0.5
    m_h_target=0.00001
    dm_h=1
    counter =0
    while(dm_h>m_h_target):
        counter +=1
        m_h_old = m_h

        # m_hl=fu.m_L(m_h)
        # p_pump_h=-0.4713*m_h**2-0.8896*m_h + 0.6381

        m_t=fu.m_t(m_h)
        v_t=fu.v_t(m_h)
        v_nh=fu.v_n(m_h)
        Re_t=fu.Re_t(m_h)

        f=(1.82*np.log10(Re_t) - 1.64)**-2           #estimation of the friction factor in the copper tubes

        p_t = f*(fu.Lt/fu.d_i)*0.5*fu.rho*v_t**2     #pressure drop along copper tubes from friction
        kc = -0.3952*sigma + 0.4973
        ke = 0.9773*sigma**2 -2.0738*sigma + 0.9983
        p_e = 0.5*fu.rho*v_t**2*(kc + ke)
        p_n = 0.5*fu.rho*v_nh**2

        p_h = p_t + p_e + p_n   #pressure in pascals
        p_hb = p_h/1e5          #pressure in bar
        m_h = (-0.3086*p_hb**2 -0.6567*p_hb + 0.5493)*fu.rho*1e-3

        dm_h=abs(m_h-m_h_old)
        print(counter)
    return m_h    

m_h=hydraulic_h()
print(m_h)

    



#------Coldside analysis


def hydraulics_c():
    m_c=0.4
    m_c_target=0.01
    dm_c=1
    counter =0
    #p_pump_c=0.7843*m_cl**2 - 0.4802*m_cl + 0.6598
    # p_pump_c=-0.4713*sigma**2 - 0.8896*sigma + 0.6381

    v_sh = fu.v_sh(m_c)
    Re_sh = fu.Re_sh(m_c)
    N=5
    p_sh = 4*fu.a*Re_sh**-0.15*N*fu.rho*v_sh**2 #Shell side pressure loss (This has poor validity)
    

#dp_sh = 4*a*Re_sh**0.15*N*fu.rho*v_sh**2

