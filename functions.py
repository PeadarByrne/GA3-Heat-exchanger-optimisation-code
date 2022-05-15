from pydoc import doc
import numpy as np

#Geometric constraints
l = 350e-3   #length of HX
Lt = 350e-3    #lenght of copper tube
Lt_total = 3.5  #total length of copper tube available
t_b = 1.5e-3    #baffle thickness
t_p = 4.5e-3    #tube plate and end plate thickness
bore_n = 20e-3  #bore of nozzles

#Mass constraints
mass_limit = 1.1 #limit to the total mass of the heat exchanger
mlt = 0.2   #mass per unit length for copper tube
mlp = 0.65  #mass per unit lenght for acrylic pipe
m_n = 0.025 #mass per nozzle
map = 6.375 #mass per unit area for tube plates and end plates
mab = 2.39  #mass per unit area for baffles


#Geometric specifications
nt = 13   #number of tubes
N = 13    #number of tubes in shell flow path
d_i = 6e-3     #ID copper tube
d_o = 8e-3     #OD copper tube
d_n = 20e-3   #nozzle internal diameter
d_sh = 64e-3    #shell internal diameter
nb = 9     #number of baffles
b = l/nb+1    #bafle spacing 
Y = 14e-3    #pitch spacing
pitch_shape = 'square'   #string description 'triangular' or 'square'
A_sh = d_sh*(Y - d_o)*(b/Y)     #flow area of fluid in shell inbetween baffles

#Physical properties
Cp = 4179     #specific heat capacity of fluid
kw = 0.632    #thermal conductivity of fluid
mu = 6.51e-4  #dynamic viscosity
rho = 990.1   #fluid density
kt = 386      #thermal conductivity of the tube
nu = mu/rho   #kinematic vicosity
Pr = 4.31     #prandtl number of fluid

#Water input temperatures
T_h_in=60   #hot water input temperature
T_c_in=20   #cold water input temperature

def A(d):
    #function to calclate crosssectional area from diameter
    return np.pi*d**2/4

def pitch(pitch_shape):
    #input pitch shape as string description 'triangular' or 'square'
    if pitch_shape == 'triangular': #to give constants for triangular pitch shape
        c=0.2
        a=0.2
        return c,a
    if pitch_shape == 'square':     #to give constants for square pitch shape
        c=0.15
        a=0.34
        return c,a

c , a = pitch(pitch_shape)


def m_t(m_h):
    m_t = m_h/nt
    return m_t

def m_L(m):
    #convert kg/s to litres/second
    return m/rho
def v_t(m_h):
    #m_t = m_t(m_h)
    m_t = m_h/nt
    v_t = m_t/(rho*A(d_i))
    return  v_t

def Re_t(m_h):
    #calculate Reynolds
    m_t = m_h/nt
    v_t = m_t/(rho*A(d_i))
    Re_t=(v_t*d_i/nu)
    return Re_t

def v_n(m):
    #calculate inlet nozzle velocity
    v_n = m/(rho*A(d_n))
    return v_n

def sigma():
    return nt*A(d_i)/A(d_sh)

    
def v_sh(m_c):
    v_sh=m_c/(rho*A_sh)
    return v_sh

def Re_sh(m_c):
    #calculate Reynolds
    v_sh=m_c/(rho*A_sh)
    Re_sh=(v_sh*d_o/nu)
    return Re_sh
