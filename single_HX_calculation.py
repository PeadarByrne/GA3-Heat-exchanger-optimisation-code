from tkinter import Y
import hydraulics_iteration as hydro
import thermal_iteration as thermal
import functions as fu

def HX_analysis(nt,nb,Nt,Ns):
    N = 3
    Y = 0.010 
    Lt = 0.2
    
    m_c=hydro.hydraulic_c(Lt,Y,nb,N)  #run cold hydrualics function
    m_h=hydro.hydraulic_h(Lt,nt,Nt)    #run hot hydraulics
    e_LMTD,Q_LMTD = thermal.Thermal_LMTD(m_h,m_c,nt,nb,Y,Lt)    #Run LMDT analysis
    e_NTU,Q_NTU = thermal.Thermal_NTU(m_h,m_c,nt,nb,Y,Lt)   #Run NTU analysis

    return e_LMTD , Q_LMTD, e_NTU, Q_NTU

e_LMTD , Q_LMTD, e_NTU, Q_NTU =HX_analysis(22, 20, 1, 1)
print(e_LMTD , Q_LMTD, e_NTU, Q_NTU)







