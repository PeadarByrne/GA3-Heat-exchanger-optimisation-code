import functions as fu
import numpy as np

#------Hotside analysis

#Guess mh
m_h=0.45

m_t=fu.m_t(m_h)
v_t=fu.v_t(m_h)
v_nh=fu.v_n(m_h)
Re_t=fu.Re_t(m_h)

f=(1.82*np.log10(Re_t) - 1.64)**-2

dp_t = f*(fu.Lt/fu.d_i)*0.5*fu.rho*v_t**2     #pressure drop along copper tubes from friction
sigma=fu.sigma()
'''
#create approximate function for kc,ke
'''

kc=0.45
ke=0.8
dp_e = 0.5*fu.rho*v_t**2*(kc + ke)
dp_n = 0.5*fu.rho*v_nh**2

dp = dp_t + dp_e + dp_n



#------Coldside analysis
m_c=0.5
v_sh = fu.v_sh(m_c)
Re_sh = fu.Re_sh(m_c)

a=
dp_sh = 4*a*Re_sh**0.15*N*fu.rho*v_sh**2



