from pydoc import doc
import numpy as np


#Geometric constraints
L_HX_max = 350e-3  #maximum permissible length of shell
Lt_total_cu = 3.5  #total length of copper tube available
Lt_extra = 12e-3 #additional length of copper pipe needed to fit pipes in securely, sum of both ends
t_b = 1.5e-3    #baffle thickness
t_p = 4.5e-3    #tube plate and end plate thickness
bore_n = 20e-3  #bore of nozzles
holespace_min = 2e-3    #minimum gap between holes in tube plates
l_endspace_min = 50e-3    #minimum length of end chambers
d_i = 6e-3     #ID copper tube
d_o = 8e-3     #OD copper tube
d_n = 19e-3   #nozzle internal diameter
d_sh = 64e-3    #shell internal diameter
shell_nozzle_space = 38.625e-3  #extra room needed t end of shell for nozzle

#Mass constraints
mass_limit = 1.155 #limit to the total mass of the heat exchanger
mlt = 0.2   #mass per unit length for copper tube
mls = 0.65  #mass per unit lenght for acrylic shell
m_n = 0.025 #mass per nozzle
map = 6.375 #mass per unit area for tube plates and end plates
mab = 2.39  #mass per unit area for baffles


#Geometric specifications - variables
l = 350e-3   #length of shell

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
T_c_in=20  #cold water input temperature

def A(d):
    #function to calclate crosssectional area from diameter
    return np.pi*d**2/4

def A_sh(Y,nb,Lt,Ns):
    #calculate flow area between tubes
    if Ns ==1:
        b = (Lt-(2*shell_nozzle_space))/(nb-1)  #baffle spacing
        A_sh = d_sh*(Y - d_o)*(b/Y)   #flow area perpendicular to the tubes for the full diameter
    elif Ns ==2:
        b = (Lt-shell_nozzle_space)/(nb)  #baffle spacing
        A_sh = (d_sh/2)*(Y - d_o)*(b/Y)    #flow area perpendicular to the tubes for the radius
    return A_sh

def A_sh_ends(Y):
    A_sh_ends = d_sh*(Y - d_o)*(shell_nozzle_space/Y)
    return A_sh_ends

def pitch_constants(pitch_shape):
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
    #Calculate tube velocity
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

def sigma(nt,ratio):
    #calculate area of tube exit to shell expansion area
    return nt*A(d_i)/(ratio*A(d_sh))

    
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

flowrate_cold_2022 = [0.5833, 0.5083, 0.4750, 0.4250, 0.3792, 0.3417, 0.2958, 0.2583, 0.2125, 0.1708]
pdrop_cold_2022 = [0.1113,0.2157,0.2538,0.3168,0.3613,0.4031,0.4511,0.4846,0.5181,0.5573]

flowrate_hot_2022 = [0.4583,0.4236,0.4010,0.3611,0.3125,0.2639,0.2222,0.1597,0.1181,0.0694]
pdrop_hot_2022 = [0.1333,0.1756,0.2024,0.2577,0.3171,0.3633,0.4233,0.4784,0.5330,0.5715] 

flowrate_cold_2019 = [0.6917,0.6750,0.6292,0.5917,0.5458,0.5083,0.4625,0.4250,0.3792,0.3417,0.2958,0.2542,0.2125,0.1708]
pdrop_cold_2019 = [0.1475,0.1619,0.2178,0.2607,0.3041,0.3417,0.3756,0.4118,0.4423,0.4711,0.5031,0.5297,0.5561,0.5823]

flowrate_hot_2019 = [0.5382,0.5278,0.4931,0.4549,0.4201,0.3854,0.3507,0.3160,0.2813,0.2465,0.2118,0.1771,0.1424,0.1076,0.0694]
pdrop_hot_2019 = [0.1101,0.1315,0.1800,0.2185,0.2537,0.2999,0.3440,0.3780,0.4149,0.4547,0.5005,0.5271,0.5677,0.5971,0.6045]

flowrate_cold_2018 = [0.4426,0.4255,0.4055,0.3913,0.3799,0.3628,0.3485,0.3286,0.3058,0.2801,0.2573,0.2317,0.2060,0.1861,0.1576,0.1319,0.1034,0.0806,0.0664,0.0521]
pdrop_cold_2018 = [0.1068,0.1418,0.1779,0.2056,0.2382,0.2601,0.2858,0.3187,0.3627,0.4037,0.4426,0.4845,0.5213,0.5569,0.6036,0.6412,0.6838,0.7121,0.7343,0.7744]

flowrate_hot_2018 = [0.4954,0.4805,0.4640,0.4475,0.4310,0.4145,0.3980,0.3815,0.3650,0.3485,0.3320,0.3155,0.2990,0.2825,0.2660,0.2495,0.2330,0.2165,0.2000,0.1819,0.1670,0.1472,0.1307,0.1142,0.1010,0.0845,0.0680,0.0515]
pdrop_hot_2018 = [0.0989,0.1245,0.1541,0.1827,0.2083,0.2339,0.2625,0.2880,0.3115,0.3330,0.3575,0.3800,0.4014,0.4249,0.4503,0.4647,0.4900,0.5134,0.5337,0.5470,0.5703,0.5966,0.6068,0.6150,0.6242,0.6304,0.6375,0.6457]

def chart_cold_pdrop(year, flowrate, poly_deg):

    if year == 2022:
        flowrate_cold = flowrate_cold_2022
        pdrop_cold = pdrop_cold_2022

    elif year == 2019:
        flowrate_cold = flowrate_cold_2019
        pdrop_cold = pdrop_cold_2019

    elif year == 2018:
        flowrate_cold = flowrate_cold_2018
        pdrop_cold = pdrop_cold_2018   

    #check i/p flowrate is not above the max value in given data
    #note: we will allow extrapolation for the minimum value down to 0 pressure drop
    max_flowrate = np.amax(flowrate_cold)
    #if flowrate > max_flowrate:
        #raise ValueError("Input flowrate is above the maximum value, please input a value lower than {}".format(max_flowrate))

    cold_coeffs= np.polyfit(flowrate_cold, pdrop_cold,poly_deg)
    pdrop_cold = np.poly1d(cold_coeffs)
    pdrop_cold_deriv = pdrop_cold.deriv(1)

    return pdrop_cold(flowrate), pdrop_cold_deriv(flowrate)

def chart_hot_pdrop(year, flowrate, poly_deg):
    if year == 2022:
        flowrate_hot = flowrate_hot_2022
        pdrop_hot = pdrop_hot_2022

    elif year == 2019:
        flowrate_hot = flowrate_hot_2019
        pdrop_hot = pdrop_hot_2019

    elif year == 2018:
        flowrate_hot = flowrate_hot_2018
        pdrop_hot = pdrop_hot_2018   

    #check i/p flowrate is not above the max value in given data
    #note: we will allow extrapolation for the minimum value down to 0 pressure drop
    max_flowrate = np.amax(flowrate_hot)
    #if flowrate > max_flowrate:
        #raise ValueError("Input flowrate is above the maximum value, please input a value lower than {}".format(max_flowrate))

    hot_coeffs = np.polyfit(flowrate_hot, pdrop_hot,poly_deg)
    pdrop_hot = np.poly1d(hot_coeffs)
    pdrop_hot_deriv = pdrop_hot.deriv(1)

    return pdrop_hot(flowrate), pdrop_hot_deriv(flowrate)
