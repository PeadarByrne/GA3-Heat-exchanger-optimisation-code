from pydoc import doc
import numpy as np

#Geometric constraints
l_max = 350e-3  #maximum permissible length of shell
Lt_total = 3.5  #total length of copper tube available
Lt_extra = 12e-3 #additional length of copper pipe needed to fit pipes in securely, sum of both ends
Lt_max = l_max - 100 -Lt_extra     #Based on maintaining the minium HX
t_b = 1.5e-3    #baffle thickness
t_p = 4.5e-3    #tube plate and end plate thickness
bore_n = 20e-3  #bore of nozzles
holespace_min = 2e-3    #minimum gap between holes in tube plates
l_endspace_min = 50e-3    #minimum length of end chambers
d_i = 6e-3     #ID copper tube
d_o = 8e-3     #OD copper tube
d_n = 20e-3   #nozzle internal diameter
d_sh = 64e-3    #shell internal diameter

#testlester

#Mass constraints
mass_limit = 1.1 #limit to the total mass of the heat exchanger
mlt = 0.2   #mass per unit length for copper tube
mls = 0.65  #mass per unit lenght for acrylic shell
m_n = 0.025 #mass per nozzle
map = 6.375 #mass per unit area for tube plates and end plates
mab = 2.39  #mass per unit area for baffles


#Geometric specifications - variables
l = 350e-3   #length of shell

#Lt = 350e-3    #length of copper tube
#nt = 13   #number of tubes
#N = 13    #number of tubes in shell flow path
#nt_cross = 5    #number of tubes in longest straight line
#nb = 9     #number of baffles
#Y = 14e-3    #pitch spacing between centres
#pitch_shape = 'square'   #string description 'triangular' or 'square'




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

def A_sh(Y,nb,Lt,Ns):
    b = Lt/(nb+1)   #baffle spacing
    if Ns ==1:
        A_sh = d_sh*(Y - d_o)*(b/Y)   #flow area perpendicular to the tubes for the full diameter
    elif Ns ==2:
        A_sh = (d_sh/2)*(Y - d_o)*(b/Y)    #flow area perpendicular to the tubes for the radius
    return A_sh


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


def m_t(m_h,nt):
    m_t = m_h/nt
    return m_t

# def m_L(m):
#     #convert kg/s to litres/second
#     ml =m*(rho/1000)
#     return ml
def v_t(m_h,nt):
    #m_t = m_t(m_h)
    m_t = m_h/nt
    v_t = m_t/(rho*A(d_i))
    return  v_t


def Re_t(m_h,nt):
    #calculate Reynolds from mass flow rate
    m_t = m_h/nt
    v_t = m_t/(rho*A(d_i))
    Re_t=(v_t*d_i)/nu
    return Re_t

def v_n(m):
    #calculate inlet nozzle velocity
    v_n = m/(rho*A(d_n))
    return v_n

def sigma(nt):
    return nt*A(d_i)/A(d_sh)

    
def v_sh(m_c,A_sh):
    v_sh=m_c/(rho*A_sh)
    return v_sh

def Re_sh(m_c,A_sh):
    #calculate Reynolds
    v_sh=m_c/(rho*A_sh)
    Re_sh=(v_sh*d_o/nu)
    return Re_sh

def return_max(array):
    # find the maximum value and its index in an array
    index = np.argmax(array)
    value = array[index]
    return index, value

def index_seperator(index,nt_array,nb_array):
    # find the index for the number of tubes and baffles from the index of the max value
    sep= len(nb_array)   #number of indexes before the next baffle index
    i_nt=int(np.floor(index/sep))
    i_b = int(index%sep)
    return i_nt, i_b