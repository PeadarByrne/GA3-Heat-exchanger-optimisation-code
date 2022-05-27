# from tkinter import Y
import hydraulics_iteration as hydro
import thermal_iteration as thermal
import functions as fu



def HX_analysis(nt,nb,Nt,Ns,Lt,Y,N):
    m_c=hydro.hydraulic_c(Lt,Y,nb,N,Ns)  #run cold hydrualics function
    m_h=hydro.hydraulic_h(Lt,nt,Nt)    #run hot hydraulics
    e_LMTD,Q_LMTD = thermal.Thermal_LMTD(m_h,m_c,nt,nb,Y,Lt, Nt, Ns)    #Run LMDT analysis
    e_NTU,Q_NTU = thermal.Thermal_NTU(m_h,m_c,nt,nb,Y,Lt,Ns)   #Run NTU analysis

    return e_LMTD , Q_LMTD, e_NTU, Q_NTU, m_c, m_h

def single_HX_analysis(nt,nb,Nt,Ns,Lt,Y,N,fraction,HGn,HG):
    m_c=hydro.hydraulic_c(Lt,Y,nb,N,Ns)  #run cold hydrualics function
    m_h=hydro.hydraulic_h(Lt,nt,Nt)    #run hot hydraulics
    e_LMTD,Q_LMTD = thermal.Thermal_LMTD(m_h,m_c,nt,nb,Y,Lt, Nt, Ns)    #Run LMDT analysis
    e_NTU,Q_NTU = thermal.Thermal_NTU(m_h,m_c,nt,nb,Y,Lt,Ns)   #Run NTU analysis

    return e_LMTD , Q_LMTD, e_NTU, Q_NTU

#nt,nb,Nt,Ns,Lt,Y,N
JL_2018 = [13,14,1,1,0.35,0.012,3]
B_2017 = [14,12,2,2,0.21612,0.015,3]


e_LMTD , Q_LMTD, e_NTU, Q_NTU =single_HX_analysis(13,14,1,1,0.35,0.012,3)
print("JL_2018:",e_LMTD , Q_LMTD, e_NTU, Q_NTU)
print("JL_2018:19.7%, 14.79kW")


e_LMTD , Q_LMTD, e_NTU, Q_NTU =single_HX_analysis(14,12,2,2,0.21612,0.015,3)
print("B_2017:",e_LMTD , Q_LMTD, e_NTU, Q_NTU)
print("B_2017:31.4%, 13.01kW")

e_LMTD , Q_LMTD, e_NTU, Q_NTU =single_HX_analysis(14,12,1,1,0.232,0.014,4)
print("Our Design:",e_LMTD , Q_LMTD, e_NTU, Q_NTU)




