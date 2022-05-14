import functions as fu
import numpy as np


#------Hotside analysis

#Guess mh
sigma=fu.sigma()


def hydraulic_h():
    m_h=0.45
    dp_target=100
    while(dp_h>dp_target):
        counter +=1
        m_old = m_h
        m_hl=fu.m_L(m_h)
        p_pump_h=0.7843*m_hl**2 - 0.4802*m_hl + 0.6598

        m_t=fu.m_t(m_h)
        v_t=fu.v_t(m_h)
        v_nh=fu.v_n(m_h)
        Re_t=fu.Re_t(m_h)

        f=(1.82*np.log10(Re_t) - 1.64)**-2

        p_t = f*(fu.Lt/fu.d_i)*0.5*fu.rho*v_t**2     #pressure drop along copper tubes from friction
        kc = -0.3952*sigma + 0.4973
        ke = 0.9773*sigma**2 -2.0738*sigma + 0.9983
        p_e = 0.5*fu.rho*v_t**2*(kc + ke)
        p_n = 0.5*fu.rho*v_nh**2

        p_h = p_t + p_e + p_n

        dp_h = p_h - p_pump_h

    



#------Coldside analysis
m_c=0.5
p_pump_c=-0.4713*sigma**2 - 0.8896*sigma + 0.6381
v_sh = fu.v_sh(m_c)
Re_sh = fu.Re_sh(m_c)


#dp_sh = 4*a*Re_sh**0.15*N*fu.rho*v_sh**2



