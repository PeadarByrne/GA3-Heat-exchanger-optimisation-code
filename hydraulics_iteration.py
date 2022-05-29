import functions as fu
import numpy as np
import math


#------Hotside analysis





def hydraulic_h(Lt,nt,Nt,HGn,HG,year):
    #Guess mh
    m_h=0.5
    m_h_old = 0
    p_calc_old = 0
    e_h_target=0.0001
    e=1

    if Nt ==1:
        sigma_t= 1
        sigma_n = fu.sigma(nt,1)  #area ratio of tubes to full header tank area  
    elif Nt ==2:
        sigma_t = fu.sigma(nt/2,1)    #area ratio (half tubes to full header tank) in turning header tank
        sigma_n =fu.sigma(nt/2,0.5) #area ratio (hall tubes to half header tank) in nozzle header tank
    elif Nt ==4:
        sigma_t = fu.sigma(nt/4,0.5)
        sigma_n = fu.sigma(nt/4,0.25)
    counter =0

    #Exact analytical solution for Re=inf for turbulent flow
    #turning header tank entrance exit losses
    kc_t = 0.4 - 0.4*sigma_t     #equal zero for single pass                     
    ke_t = (1-sigma_t)**2 
    #nozzle header tank entrance exit losses
    kc_n = 0.4 - 0.4*sigma_n                         
    ke_n = (1-sigma_n)**2 

    while(abs(e)>e_h_target and counter<100):
        counter +=1

        v_t=fu.v_t(m_h,nt/Nt)   #velocity tube
        v_nh=fu.v_n(m_h)        #velocity nozzle
        Re_t=fu.Re_t(m_h,nt/Nt) #Re tube

        f=(1.82*np.log10(Re_t) - 1.64)**-2           #estimation of the friction factor in the copper tubes

        #calculate pressure drop from guessed m_h
        p_t =Nt* f*(Lt/fu.d_i)*0.5*fu.rho*v_t**2   #pressure loss along copper tubes from friction
        p_e_n = 0.5*fu.rho*v_t**2*(kc_n + ke_n)   #entrance exit losses at nozzle header tanks
        p_e_t = 0.5*fu.rho*v_t**2*(kc_t + ke_t)*(Nt -1)   #entrance exit losses in turning header tanks
        p_n = fu.rho*v_nh**2    # pressure loss from nozzles entering HX, no half because 2 nozzles
        #Turning losses in header
        if Nt == 1:
            p_hturn = 0
        elif Nt == 2:
            area_ratio = (nt*0.5*math.pi*(fu.d_i/2)**2)/(HG*fu.d_sh)
            v_header = area_ratio * v_t
            p_hturn = 0.5*fu.rho*(v_header**2)
        elif Nt == 4:
            area_ratio = (nt*0.5*math.pi*(fu.d_i/2)**2)/(HG*fu.d_sh)
            v_header = area_ratio * v_t
            area_ratio_n = (nt*0.5*math.pi*(fu.d_i/2)**2)/(HGn*fu.d_sh)
            v_header_n = area_ratio_n * v_t
            p_hturn = 0.5 *fu.rho*(v_header**2)*2+0.5 *fu.rho*(v_header_n**2)
        p_h = p_t + p_e_t + p_e_n + p_n + p_hturn  #pressure in pascal
        p_h_calc = p_h/1e5          #pressure in bar

        #Newton Raphson iterator
        dp_calc = (p_h_calc - p_calc_old)/(m_h - m_h_old) #Calculate an approximate derivative of p_calc 
        m_h_old = m_h   #store m_h from previous guess
        m_hl =(fu.rho/1000)*m_h #convert to litres/s
        p_h_pump = fu.chart_hot_pdrop(year, m_hl, 2)[0]
        dp_h_pump = fu.chart_hot_pdrop(year, m_hl, 2)[1]
        m_h = m_h - (p_h_pump - p_h_calc)/(dp_h_pump - dp_calc)    #calculate new mass flow using newton raphson iteration
        e = p_h_pump - p_h_calc #calculate error
        p_calc_old = p_h_calc   #store previosly calculated pressure for next iteration
      
        if counter == 100:
            raise RuntimeError

    #print(counter)
    # print("p_h_calc", p_h_calc)
    # print("m_h", m_h)

    # calculated m_h is within the limits of the pumps capabilities
    # if m_hl < 0.0694:
    #     print('hotside-outside the pumps performance limits')
    #     raise ValueError('outside the pumps performance limits')
    fudge=0.91
    m_h = m_h*fudge
    return m_h    

#------Coldside analysis


def hydraulic_c(Lt,Y,nb,N,Ns,year):
    m_c=0.3
    m_c_old =0
    p_calc_old =0
    e_c_target=0.0001
    e=1
    
    pitch_shape = "triangular"
    c , a = fu.pitch_constants(pitch_shape) 

    A_sh = fu.A_sh(Y,nb,Lt,Ns) 

    counter =0
    Kt = 1    #Coefficient for turning loss
    while(abs(e)>e_c_target and counter<=100):

        counter+=1
        #calculate pressure drop from guessed m_c
        v_sh = fu.v_sh(m_c,A_sh) 
        Re_sh = fu.Re_sh(m_c,A_sh)
        vn_c = fu.v_n(m_c)
        v_ends = m_c/(fu.rho*fu.A_sh_ends(Y))
        Re_ends = v_ends*fu.d_o/fu.nu

        #Calculate pressure losses
        if Ns==1:
            p_sh = 4*a*Re_sh**(-0.15)*N*fu.rho*v_sh**2*(nb - 1)*Ns #Shell side pressure loss normal to tubes, multiplied by Ns because two passes means each baffle is pass twice
        elif Ns==2:
            p_sh = 4*a*Re_sh**(-0.15)*N*fu.rho*v_sh**2*(nb)*Ns
        p_turn = Kt*0.5*fu.rho*(v_sh**2)*Ns*nb                  #turning pressure loss
        p_ends = 4*a*Re_ends**(-0.15)*N*fu.rho*v_ends**2*2/Ns   #pressure losses in extra spaces at ends of shell for nozzles
        p_n = fu.rho*vn_c**2                            #nozzle losses
        p_c = p_sh + p_n + p_turn + p_ends   #calculated pressure from m_c guess
        p_c_calc = p_c/1e5  #convert pressure to bar

        #Newton Raphson iterator
        dp_calc = (p_c_calc - p_calc_old)/(m_c - m_c_old) #Calculate an approximate derivative of p_calc 
        m_c_old = m_c   #store m_c from previous guess
        m_cl =(fu.rho/1000)*m_c #convert to litres/s
        p_c_pump = fu.chart_cold_pdrop(year, m_cl, 2)[0]    #pump pressure drop for guessed m_c
        dp_c_pump = fu.chart_cold_pdrop(year, m_cl, 2)[1]   #derivative of pressure drop for guessed m_c
        m_c = m_c - (p_c_pump - p_c_calc)/(dp_c_pump - dp_calc)    #calculate new mass flow using newton raphson iteration
        e = p_c_pump - p_c_calc #calculate error
        p_calc_old = p_c_calc   #store previosly calculated pressure for next iteration
      
        if counter == 100:
            raise RuntimeError

    #print(counter)
    #print("p_c_calc", p_c_calc)
    #print("m_c", m_c)

    #check calculated m_c is within the limits of the pumps capabilities
    # if m_cl < 0.1708:
    #     print('coldside-outside the pumps performance limits')
    #     raise ValueError('outside the pumps performance limits')
    return m_c




