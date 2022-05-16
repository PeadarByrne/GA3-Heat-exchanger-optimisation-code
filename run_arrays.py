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
    #check.CheckArrayLength(shape_array,nt_array,nt_cross_array,l_array,lt_array,Y_array)
    #Initialise output arrays
    e_LMTD_array=[]
    Q_LMTD_array=[]
    e_NTU_array=[]
    Q_NTU_array=[]


    for i in range(len(shape_array)):
        #find datapoints for current design
        shape=shape_array[i]
        nt=nt_array[i]
        nt_cross=nt_cross_array[i]
        l=l_array[i]
        lt=lt_array[i]
        Y=Y_array[i]
        N=nt    #only valid for single pass

        #check design is legal
        #check.CheckDesign(l,lt,nt,nt_cross,Y,nb)

        
        m_c=hydro.hydraulic_c(lt,Y,nb,N,shape)  #run cold hydrualics function
        m_h=hydro.hydraulic_h(lt,nt)    #run hot hydraulics
        (e_LMTD,Q_LMTD) = thermal.Thermal_LMTD(m_h,m_c,nt,nb,Y,lt,shape)    #Run LMDT analysis
        (e_NTU,Q_NTU) = thermal.Thermal_NTU(m_h,m_c,nt,nb,Y,lt,shape)   #Run NTU analysis
        #append results into output arrays
        e_LMTD_array.append(e_LMTD)
        Q_LMTD_array.append(Q_LMTD)
        e_NTU_array.append(e_NTU)
        Q_NTU_array.append(Q_NTU)
        # except ValueError:
        #     e_LMTD_array.append('nope')
        #     Q_LMTD_array.append('nope')
        #     e_NTU_array.append('nope')
        #     Q_NTU_array.append('nope')
            
    
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

    
run_optimisation(input.shape_array,input.nt_array,input.nt_cross_array,input.l_array,input.lt_array,input.Y_array)

