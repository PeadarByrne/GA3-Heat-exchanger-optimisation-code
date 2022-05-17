import hydraulics_iteration as hydro
import thermal_iteration as thermal
import functions as fu

def HX_analysis(nt,nb,N,Y,lt,shape):
    m_c=hydro.hydraulic_c(lt,Y,nb,N,shape)  #run cold hydrualics function
    m_h=hydro.hydraulic_h(lt,nt)    #run hot hydraulics
    e_LMTD,Q_LMTD = thermal.Thermal_LMTD(m_h,m_c,nt,nb,Y,lt,shape)    #Run LMDT analysis
    e_NTU,Q_NTU = thermal.Thermal_NTU(m_h,m_c,nt,nb,Y,lt,shape)   #Run NTU analysis

    return e_LMTD , Q_LMTD, e_NTU, Q_NTU

# e_LMTD , Q_LMTD, e_NTU, Q_NTU =HX_analysis(13, 9, 13, 14e-3, 350e-3,'square')
# print(e_LMTD , Q_LMTD, e_NTU, Q_NTU)







