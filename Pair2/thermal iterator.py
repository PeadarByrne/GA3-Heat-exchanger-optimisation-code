  
    import numpy as np
    
    Th_out_vals = np.linspace(40,fu.T_h_in,1000)
    Tc_out_vals = np.linspace(fu.T_c_in,40,1000)

    min_tot_error = None
    counter = 0
    for Th_out in Th_out_vals:
        for Tc_out in Tc_out_vals:
            counter += 1
            deltaT_1 = fu.T_h_in - Tc_out
            deltaT_2 = Th_out - fu.T_c_in
            deltaT_lm = ((deltaT_1)-(deltaT_2))/(math.log(deltaT_1/deltaT_2))  #LMTD

            Q1 = m_c*fu.Cp*(Tc_out-fu.T_c_in)
            Q2 = m_h*fu.Cp*(fu.T_h_in-Th_out)

            if (Nt ==1) and (Ns==1): #one shell one pass
                F = 1
                
            elif Nt > 1: # if we have more than 1 tube pass, need F
                R = (fu.T_h_in-Th_out)/(Tc_out-fu.T_c_in)
                P = (Tc_out-fu.T_c_in)/(fu.T_h_in-fu.T_c_in)

                if R!= 1:
                    W = ((1-P*R)/(1-P))**(1/Ns)
                    S = ((R**2 +1)**0.5)/(R-1)
                    F = (S*np.log(W))/np.log((1+W-S+S*W)/(1+W+S-(S*W)))
                elif R==1: #must take Ns=1
                    W_dash = (Ns - Ns*P)/(Ns-Ns*P+P)
                    F = np.sqrt(2)*((1-W_dash)/W_dash)/np.log(((W_dash/(1-W_dash))+(1/np.sqrt(2)))/((W_dash/(1-W_dash))-(1/np.sqrt(2))))

            Q3= U*A_i*F* deltaT_lm 

            tot_error = abs(Q1-Q3) + abs(Q1-Q2) + abs(Q2 - Q3)

            if min_tot_error == None:
                min_tot_error = tot_error
                tempsout_data = [Th_out,Tc_out, min_tot_error]

            elif tot_error < min_tot_error:
                min_tot_error = tot_error
                tempsout_data = [Th_out,Tc_out, min_tot_error]

            else:
                pass
    
    T_h_out = tempsout_data[0]
    T_c_out = tempsout_data[1]

    print(counter)
    print("Correction factor:", F)
    print("T_c_out", T_c_out)
    print("T_h_out", T_h_out)            

    deltaT_1 = fu.T_h_in - T_c_out
    deltaT_2 = T_h_out - fu.T_c_in
    delta_T_lm = ((deltaT_1)-(deltaT_2))/(math.log(deltaT_1/deltaT_2))  #LMTD
    #Q1 = m_c*fu.Cp*(T_c_out-fu.T_c_in)
    #Q2 = m_h*fu.Cp*(fu.T_h_in-T_h_out)
    #Q3 = U*A_i* deltaT_lm 
    #from now on, set Th_out and Tc_in to be the optimal vals
    