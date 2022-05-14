import functions as fu
import numpy as np


#------Hotside analysis

#Guess mh
m_h=0.45
p_drop_h=0.7843*m_h**2 - 0.4802*m_h + 0.6598

m_t=fu.m_t(m_h)
v_t=fu.v_t(m_h)
v_nh=fu.v_n(m_h)
Re_t=fu.Re_t(m_h)

f=(1.82*np.log10(Re_t) - 1.64)**-2

dp_t = f*(fu.Lt/fu.d_i)*0.5*fu.rho*v_t**2     #pressure drop along copper tubes from friction
sigma=fu.sigma()



kc = -0.3952*sigma + 0.4973
ke = 0.9773*sigma**2 -2.0738*sigma + 0.9983
dp_e = 0.5*fu.rho*v_t**2*(kc + ke)
dp_n = 0.5*fu.rho*v_nh**2

dp = dp_t + dp_e + dp_n



#------Coldside analysis
m_c=0.5
v_sh = fu.v_sh(m_c)
Re_sh = fu.Re_sh(m_c)


#dp_sh = 4*a*Re_sh**0.15*N*fu.rho*v_sh**2



