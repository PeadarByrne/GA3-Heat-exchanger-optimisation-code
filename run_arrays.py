from numpy import append
import functions as fu
import validity_check as check
import thermal_iteration as thermal
import hydraulics_iteration as hydro
import input_arrays as input

nb = 9  #number of baffles

#Function runs simulations for geometries in input arrays
def run_optimisation(shape_array,nt_array,nt_cross_array,l_array,lt_array,Y_array):
    #check lengths of input arrays
    check.CheckArrayLength(shape_array,nt_array,nt_cross_array,l_array,lt_array,Y_array)
    #Initialise output arrays
    e_LMTD_array=[]
    Q_LMTD_array=[]
    e_NTU_array=[]
    Q_NTU_array=[]
    x = 0
    length = len(shape_array)
    while x >= length:
        #find datapoints for current design
        shape=shape_array[x]
        nt=nt_array[x]
        nt_cross=nt_cross_array[x]
        l=l_array[x]
        lt=lt_array[x]
        Y=Y_array[x]
        N=nt    #only valid for single pass
        #check design is legl
        check.CheckDesign(shape)
        #run cold hydrualics function
        m_c=hydro.hydraulic_c(lt,Y,nb,N,shape)
        #run hot hydraulics
        m_h=hydro.hydraulic_h(lt,nt)
        #Run LMDT analysis
        (e_LMTD,Q_LMTD) = thermal.Thermal_LMTD(m_h,m_c,nt,nb,Y,lt,shape)
        #Run NTU analysis
        (e_NTU,Q_NTU) = thermal.Thermal_NTU(m_h,m_c,nt,nb,Y,lt,shape)
        #append results into output arrays
        e_LMTD_array.append(e_LMTD)
        Q_LMTD_array.append(Q_LMTD)
        e_NTU_array.append(e_NTU)
        Q_NTU_array.append(Q_NTU)
        x+=1
    
    #print results
    print('LMTD effectivenesses:')
    print(e_LMTD_array)
    print('LMTD heat transfer rates:')
    print(Q_LMTD_array)
    print('NTU effectivenesses:')
    print(e_NTU_array)
    print('NTU heat transfer rates')
    print(Q_NTU_array)

    return e_LMTD_array,Q_LMTD_array,e_NTU_array,Q_NTU_array

    


