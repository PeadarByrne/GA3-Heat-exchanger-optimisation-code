# from tkinter import Y
import hydraulics_iteration as hydro
import thermal_iteration as thermal
import functions as fu

def single_HX_analysis(nt,nb,Nt,Ns,Lt,Y,N,year,HGn=57.5e-3,HG=57.5e-3):
    #evaluate performance of HX                
    m_c=hydro.hydraulic_c(Lt,Y,nb,N,Ns,year)  #run cold hydrualics function
    m_h=hydro.hydraulic_h(Lt,nt,Nt,HGn,HG,year)    #run hot hydraulics
    e_LMTD,Q_LMTD = thermal.Thermal_LMTD(m_h,m_c,nt,nb,Y,Lt, Nt, Ns)    #Run LMDT analysis
    e_NTU,Q_NTU = thermal.Thermal_NTU(m_h,m_c,nt,nb,Y,Lt,Ns)   #Run NTU analysis

    Q_LMTD =Q_LMTD/1000 #convert to kW
    m_c = fu.mkg_to_mL(m_c) #convert to L/s
    m_h = fu.mkg_to_mL(m_h)
    return e_LMTD , Q_LMTD, e_NTU, Q_NTU, m_c, m_h





