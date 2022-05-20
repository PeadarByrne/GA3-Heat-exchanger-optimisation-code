import math
import numpy as np
import matplotlib.pyplot as plt

#PROPERTIES AT 40˚C (FIXED)
cp = 4179 #J/kgK
k = 0.632 #thermal conductivity W/mK
mu = 6.51e-4 #dynamic viscosity kg/ms
Pr = 4.31    #Prandtl number
rho = 990.1  #density    
k_tube = 386 #copper tube thermal conductivity

#FIXED PARAMETERS
d_i = 0.006               #copper tube inner diameter
d_o = 0.008               #copper tube outer diameter
d_n = 0.019               #nozzle diamter
d_sh = 0.064              #shell inner diameter

def calc_hot_pdrop(m_h, N, pitch_type, Y, baffle_number, L_shellgap, L_tubes):
    #this func returns the calculated HOT tot pdrop given a massflowrate value and HX parameters of:
    # N:no_tubes, pitch_type: square or triangular, Y: tube_pitch, baffle_number, L:shell_length

    #FIXED PARAMETERS
    d_i = 0.006               #copper tube inner diameter
    d_o = 0.008               #copper tube outer diameter
    d_n = 0.019               #nozzle diamter
    d_sh = 0.064              #shell inner diameter

    #PROPERTIES AT 40˚C (FIXED)
    cp = 4179 #J/kgK
    k = 0.632 #thermal conductivity W/mK
    mu = 6.51e-4 #dynamic viscosity kg/ms
    Pr = 4.31    #Prandtl number
    rho = 990.1  #density    
    k_tube = 386 #copper tube thermal conductivity

    pitch_vals = ["triangular", "square"]
    if pitch_type not in pitch_vals:
        raise ValueError("Invalid pitch type, input triangular or square")

    if pitch_type == "triangular":
        a=0.2
        c=0.2

    elif pitch_type == "square":
        a=0.34
        c=0.15

    #CALCULATIONS
    B = L_shellgap/(baffle_number + 1) #baffle spacing

    m_tube = m_h/N                                  #tube mass flow rate
    v_tube = m_tube / (0.25*rho*math.pi*d_i**2)     #tube velocity
    Re_t = (v_tube*rho*d_i)/mu                      #Reynolds number in tube
    v_noz_h = m_h/(0.25*rho*math.pi*(d_n**2))       #nozzle velocity for hot side
    sigma = N * (d_i/d_sh)**2                       #ratio of free area
    kc = 0.4 - 0.4*sigma                          
    ke = (1-sigma)**2 
    f = (1.82*math.log10(Re_t) - 1.64)**(-2)        #friction factor
    deltap_tube = f*L_tubes*0.5*rho*(v_tube**2)/d_i       #pressure drop along the tubes                           
    deltap_inout = 0.5*rho*(v_tube**2)*(kc + ke)    #pressure drop associated with flows in and out of tube bundle
    deltap_noz_h = rho*(v_noz_h**2)                 #pressure drop associated with flows in and out of nozzles

    deltap_total_h = (deltap_tube + deltap_inout + deltap_noz_h)*10**(-5) #total pressure drop in Pa 
    return deltap_total_h

def calc_cold_pdrop(m_c, N, pitch_type, Y, baffle_number, L_shellgap, L_tubes):
    #this func returns the calculated COLD tot pdrop given a massflowrate value and HX parameters of:
    # N:no_tubes, pitch_type: square or triangular, Y: tube_pitch, baffle_number, L:shell_length

    #FIXED PARAMETERS
    d_i = 0.006               #copper tube inner diameter
    d_o = 0.008               #copper tube outer diameter
    d_n = 0.019               #nozzle diamter
    d_sh = 0.064              #shell inner diameter

    #PROPERTIES AT 40˚C (FIXED)
    cp = 4179 #J/kgK
    k = 0.632 #thermal conductivity W/mK
    mu = 6.51e-4 #dynamic viscosity kg/ms
    Pr = 4.31    #Prandtl number
    rho = 990.1  #density    
    k_tube = 386 #copper tube thermal conductivity

    #whether pitch is triagular or square
    pitch_vals = ["triangular", "square"]
    if pitch_type not in pitch_vals:
        raise ValueError("Invalid pitch type, input triangular or square")

    if pitch_type == "triangular":
        a=0.2
        c=0.2
    elif pitch_type == "square":
        a=0.34
        c=0.15

    #CALCULATIONS
    B = L_shellgap/(baffle_number + 1) #baffle spacing
    A_sh = (d_sh*(Y - d_o)*B)/Y    #shell area
    v_sh = m_c/(rho*A_sh)        #bulk velocity/velocity across tube bundle
    Re_sh = v_sh*d_o*rho/mu      #Re based on bulk velocity                

    deltap_shell = 4*a*(Re_sh**-0.15)*N*rho*(v_sh**2)  #Shell side pressure drop            
    v_noz_c = m_c/(0.25*rho*math.pi*(d_n**2))          #nozzle velocity for cold side
    deltap_noz_c = rho*(v_noz_c**2)                    #pressure drop associated with flows in and out of nozzles
    deltap_total_c = (deltap_shell + deltap_noz_c)*10**(-5)       #total pressure drop in bar

    return deltap_total_c

def chart_hot_pdrop(flowrate, poly_deg=3):
    #2022 Hot Characteristic Data Points
    flowrate_hot = [0.4583,0.4236,0.4010,0.3611,0.3125,0.2639,0.2222,0.1597,0.1181,0.0694]
    pdrop_hot = [0.1333,0.1756,0.2024,0.2577,0.3171,0.3633,0.4233,0.4784,0.5330,0.5715] 

    #check i/p flowrate is not above the max value in given data
    #note: we will allow extrapolation for the minimum value down to 0 pressure drop
    max_flowrate = np.amax(flowrate_hot)
    #if flowrate > max_flowrate:
        #raise ValueError("Input flowrate is above the maximum value, please input a value lower than {}".format(max_flowrate))

    hot_coeffs = np.polyfit(flowrate_hot, pdrop_hot,poly_deg)
    pdrop_hot = np.poly1d(hot_coeffs)

    return pdrop_hot(flowrate)

def chart_cold_pdrop(flowrate, poly_deg=3):

    #2022 Cold Characteristic Data Points
    flowrate_cold = [0.5833, 0.5083, 0.4750, 0.4250, 0.3792, 0.3417, 0.2958, 0.2583, 0.2125, 0.1708]
    pdrop_cold = [0.1113,0.2157,0.2538,0.3168,0.3613,0.4031,0.4511,0.4846,0.5181,0.5573]

    #check i/p flowrate is not above the max value in given data
    #note: we will allow extrapolation for the minimum value down to 0 pressure drop
    max_flowrate = np.amax(flowrate_cold)
    #if flowrate > max_flowrate:
        #raise ValueError("Input flowrate is above the maximum value, please input a value lower than {}".format(max_flowrate))

    cold_coeffs= np.polyfit(flowrate_cold, pdrop_cold,poly_deg)
    pdrop_cold = np.poly1d(cold_coeffs)
    return pdrop_cold(flowrate)

#SET VARIABLE PARAMETERS HERE
N = 13  #number of tubes
Y = 0.011 #tube pitch
baffle_number = 9
pitch_type = "triangular"
L = 0.35  #shell length, max = 0.35m
poly_deg = 3
cp = 4179 #J/kgK of water

Ns = 1 #1 for one shell pass, Ns = number of SHELL PASSES
Nt = 1 # number of tube passes


#SET VARIABLE PARAMETERS HERE
N = 13  #number of tubes
Y = 0.011 #tube pitch
baffle_number = 9
pitch_type = "triangular"
L = 0.35  #shell length, max = 0.35m
poly_deg = 3
cp = 4179 #J/kgK of water

Ns = 1 #1 for one shell pass, Ns = number of SHELL PASSES
Nt = 1 # number of tube passes

#in this code, we are always going to have a set val for header tanks, meaning shell length is fixed depenfin on even or odd tueb pass
header_gap_v = 0.05 #gap between plates in header when we have a valve
header_gap_nv = 0.03    #gap between plates in header when we have no valve
L_acrylic_header_v = header_gap_v + 0.0035
L_acrylic_header_nv = header_gap_nv + 0.0035


#mass of nozzle
m_noz = 4*0.025 #4 nozzles

#mass of 2 tube plates and 2 end plates
rho_plate=6.375
m_tube_plate= ((np.pi*0.25*0.069**2*0.0015 +np.pi*0.25*0.06370**2*0.003)- (N*np.pi*0.25*d_o**2*0.0045))*rho_plate*2
m_endplate = (np.pi*0.25*0.069**2*0.0025+np.pi*0.0637**2*0.25*0.002)*rho_plate

#mass of baffles
rho_baffle = 2.39
p_a=0.5 #proportion of circle that baffle area occupies
#this is assuming baffles are half the circle of shell, i.e. for 2 shell
m_baffle=1.5*np.pi*0.0635**2*rho_baffle*baffle_number*p_a -(N*0.5*np.pi*d_o**2*0.25*0.0015)

#need separating plate


#For header tank variations:
if Nt%2 == 0: #if we have an even no of tube passes, we only need one header tank to be 51mm, the other can be much smaller as we dont need valve
    L_sh = 0.35 - (L_acrylic_header_v + (0.0025+0.0015)*2 + L_acrylic_header_nv ) #L_sh is length of main shell acrylic
    L_shellgap = L_sh - 0.003
    L_tubes = L_sh + 0.009 #by geometry in fig 8a
    L_acrylic_tot = L_sh + L_acrylic_header_nv + L_acrylic_header_v

elif  Nt%2 ==1: # we have odd number of passes, hence need both header tanks to be 51mm
    L_sh = 0.35 - (L_acrylic_header_v + 0.0025+0.0015)*2 
    L_shellgap = L_sh - 0.003
    L_tubes = L_sh + 0.009
    L_acrylic_tot = L_sh + 2*L_acrylic_header_v

#total mass of acrylic
rho_sh=0.650
hole_nozzle_d = 0.025 #25mm in moodle example design, but 24.5 in handout
m_acrylic = (np.pi * 0.25*(D_sh**2 - d_sh**2)*L_acrylic_tot - 4*np.pi*hole_nozzle_d**2*0.25*((D_sh-d_sh)/2))*rho_sh

#total tube mass
rho_tube=0.2 #check this
m_tubes = (N*np.pi*0.25*(d_o**2-d_i**2)*(L_tubes))*rho_tube


#ITERATORS TO OBTAIN FLOWRATES

def calc_m_h():
    m_h_vals = np.arange(0.0694,1, 0.0001) #min flowarate: 0.0694, max flowrate:0.4583 from 2022 data 
    min_error = None

    for m_h in m_h_vals:
        calc_pdrop = calc_hot_pdrop(m_h, N, pitch_type, Y, baffle_number, L_shellgap, L_tubes)
        chart_pdrop = chart_hot_pdrop(m_h*1000/rho,poly_deg)                   #mass flowrate to volumetric flow rate
        error = abs(calc_pdrop-chart_pdrop)

        if min_error==None:
            min_error = error
            data_hot = [m_h, min_error]
        elif error < min_error:
            min_error = error
            data_hot = [m_h, min_error]
        else:
            pass

    #m_h is from now the optimal one
    m_h = data_hot[0]
    return m_h

def calc_m_c():
    m_c_vals = np.arange(0.1708,1, 0.0001)    #min flowarate: 0.1708, max flowrate:0.5833 from 2022 data 
    min_error = None

    for m_c in m_c_vals:
        calc_pdrop = calc_cold_pdrop(m_c, N, pitch_type, Y, baffle_number, L_shellgap, L_tubes)
        chart_pdrop = chart_cold_pdrop(m_c*1000/rho,poly_deg)
        error = abs(calc_pdrop-chart_pdrop)

        if min_error==None:
            min_error = error
            data_cold = [m_c, min_error]
        elif error < min_error:
            min_error = error
            data_cold = [m_c, min_error]
        
        else:
            pass

    #m_c is from now the optimal one
    m_c = data_cold[0]
    return m_c

m_h = calc_m_h()
m_c = calc_m_c()
print("PRESSURE DROP",calc_hot_pdrop(m_h, N, pitch_type, Y, baffle_number, L_shellgap, L_tubes))
print("PRESSURE DROP",calc_cold_pdrop(m_c, N, pitch_type, Y, baffle_number, L_shellgap, L_tubes))


#THERMAL DESIGN SECTION
def UA_coeff(m_h, m_c, N, pitch_type, Y, baffle_number, L_shellgap):
    #FIXED PARAMETERS
    d_i = 0.006               #copper tube inner diameter
    d_o = 0.008               #copper tube outer diameter
    d_n = 0.019               #nozzle diamter
    d_sh = 0.064              #shell inner diameter

    #PROPERTIES AT 40˚C (FIXED)
    cp = 4179 #J/kgK
    k = 0.632 #thermal conductivity W/mK
    mu = 6.51e-4 #dynamic viscosity kg/ms
    Pr = 4.31    #Prandtl number
    rho = 990.1  #density    
    k_tube = 386 #copper tube thermal conductivity

    pitch_vals = ["triangular", "square"]
    if pitch_type not in pitch_vals:
        raise ValueError("Invalid pitch type, input triangular or square")

    if pitch_type == "triangular":
        a=0.2
        c=0.2

    elif pitch_type == "square":
        a=0.34
        c=0.15

    #CALCULATIONS
    B = L_shellgap/(baffle_number + 1) #baffle spacing
    m_tube = m_h/N                                  #tube mass flow rate
    v_tube = m_tube / (0.25*rho*math.pi*d_i**2)     #tube velocity
    Re_t = (v_tube*rho*d_i)/mu                      #Reynolds number in tube

    A_sh = (d_sh*(Y - d_o)*B)/Y    #shell area
    v_sh = m_c/(rho*A_sh)        #bulk velocity/velocity across tube bundle
    Re_sh = v_sh*d_o*rho/mu      #Re based on bulk velocity 

    Nu_i = 0.023*(Re_t**0.8)*(Pr**0.3) #Nusselt number based on inner tube diameter
    h_i = Nu_i*k/d_i                   #tube inner film heat transfer coefficient 
    Nu_o = c*(Re_sh**0.6)*(Pr**0.3)    #Nusselt number based on outer tube diameter
    h_o = Nu_o*k/d_o                   #tube outer filmheat transfer coefficient
    U = 1/((1/h_i)+(0.5*d_i*math.log(d_o/d_i)/k_tube)+(d_i/(d_o*h_o))) #overall heat transfer coefficient
    A = math.pi*d_i*L_shellgap*N  

    return U*A

UA = UA_coeff(m_h, m_c, N, pitch_type, Y, baffle_number, L_shellgap)

#fixed parameters
Th_in = 60
Tc_in = 20

#LMTD method
def calc_LMTD():
    
    Th_out_vals = np.linspace(40,59.99,2000)
    Tc_out_vals = np.linspace(20.01,40,2000)

    min_tot_error = None

    for Th_out in Th_out_vals:
        for Tc_out in Tc_out_vals:

            deltaT_1 = Th_in - Tc_out
            deltaT_2 = Th_out - Tc_in
            deltaT_lm = ((deltaT_1)-(deltaT_2))/(math.log(deltaT_1/deltaT_2))  #LMTD

            Q1 = m_c*cp*(Tc_out-Tc_in)
            Q2 = m_h*cp*(Th_in-Th_out)

            if (Nt ==1) and (Ns==1): #one shell one pass
                Q3 = UA* deltaT_lm 
                
            elif Nt > 1: # if we have more than 1 tube pass, need F
                R = (Th_in-Th_out)/(Tc_out-Tc_in)
                P = (Tc_out-Tc_in)/(Th_in-Tc_in)

                if R!= 1:
                    W = ((1-P*R)/(1-P))**(1/Ns)
                    S = ((R**2 +1)**0.5)/(R-1)
                    F = (S*np.log(W))/np.log((1+W-S+S*W)/(1+W+S-(S*W)))
                elif R==1: #must take Ns=1
                    W_dash = (Ns - Ns*P)/(Ns-Ns*P+P)
                    F = np.sqrt(2)*((1-W_dash)/W_dash)/np.log(((W_dash/(1-W_dash))+(1/np.sqrt(2)))/((W_dash/(1-W_dash))-(1/np.sqrt(2))))

                Q3= UA*F* deltaT_lm 

            tot_error = abs(Q1-Q3) + abs(Q1-Q2) + abs(Q2 - Q3)

            if min_tot_error == None:
                min_tot_error = tot_error
                tempsout_data = [Th_out,Tc_out, min_tot_error]

            elif tot_error < min_tot_error:
                min_tot_error = tot_error
                tempsout_data = [Th_out,Tc_out, min_tot_error]

            else:
                pass

    deltaT_1 = Th_in - tempsout_data[1]
    deltaT_2 = tempsout_data[0] - Tc_in
    deltaT_lm = ((deltaT_1)-(deltaT_2))/(math.log(deltaT_1/deltaT_2))  #LMTD
    Q1 = m_c*cp*(tempsout_data[1]-Tc_in)
    Q2 = m_h*cp*(Th_in-tempsout_data[0])
    Q3 = UA* deltaT_lm 
    #from now on, set Th_out and Tc_in to be the optimal vals

    Th_out = tempsout_data[0]
    Tc_out = tempsout_data[1]
    
    #LMTD effectiveness
    if m_h < m_c:
        LMTD_epsilon = (Th_in-Th_out)/(Th_in - Tc_in)

    elif m_c< m_h:
        LMTD_epsilon = (Tc_out-Tc_in)/(Th_in - Tc_in)

    elif m_c == m_h:
        LMTD_epsilon = (Tc_out-Tc_in)/(Th_in - Tc_in) #either eqn can be taken as they are equal (but we do not want this)

    print("LMTD method:")
    print("m_c:", m_c, "", "m_h",m_h)
    print("T hot out = ", Th_out, "", "T cold out:", Tc_out)
    print("Effectiveness=",LMTD_epsilon)
    print("Q1:", Q1, "Q2:", Q2, "Q3:", Q3 )
    return

calc_LMTD()

#epsilon-NTU method
def calc_epsilon_NTU():
    C_h = m_h*cp
    C_c = m_c*cp

    if C_c <= C_h:
        C_min = C_c
        C_max = C_h
    else:
        C_min = C_h
        C_max = C_c
        
    NTU = UA/C_min
    R_c = C_min / C_max

    NTU_epsilon = (1 - math.exp(-NTU*(1-R_c)))/(1 - R_c*math.exp(-NTU*(1-R_c)))      #for counterflow arrangement. epsilon = effectiveness 

    Th_out = Th_in - NTU_epsilon*C_min*(Th_in-Tc_in)/C_h
    Tc_out = Tc_in + NTU_epsilon*C_min*(Th_in-Tc_in)/C_c
    Q = NTU_epsilon*C_min*(Th_in-Tc_in)

    print(" ")
    print("Epsilon-NTU method:")
    print("T hot out = ", Th_out, "", "T cold out:", Tc_out)
    print("Effectiveness=",NTU_epsilon)
    print("Q:", Q)
    return

calc_epsilon_NTU()
