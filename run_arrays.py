from numpy import append
import functions as fu
import validity_check as check
import thermal_iteration as thermal
import hydraulics_iteration as hydro
import input_arrays as input



#Function runs simulations for geometries in input arrays
def run_optimisation(shape_array,nt_array,nt_cross_array,l_array,lt_array,Y_array,nb_array):
    #check lengths of input arrays
    check.CheckArrayLength(shape_array,nt_array,nt_cross_array,l_array,lt_array,Y_array)
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



        for j in range(len(nb_array)):
            nb = nb_array[j]

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
    index_LMTD, e_LMTD_max = fu.return_max(e_LMTD_array)  
    Q_LMTD_max = Q_LMTD_array[index_LMTD] 
    index_NTU, e_NTU_max = fu.return_max(e_NTU_array)  
    Q_NTU_max = Q_NTU_array[index_NTU] 
    #print(shape(e_LMTD_max))
    #print results
    # print('LMTD effectivenesses:')
    # print(e_LMTD_array)
    # print('LMTD heat transfer rates:')
    # print(Q_LMTD_array)
    # print('NTU effectivenesses:')
    # print(e_NTU_array)
    # print('NTU heat transfer rates')
    # print(Q_NTU_array)
    i_nt, i_nb =fu.index_seperator(index_LMTD,nt_array,nb_array)
    if i_nt>5:
        shape = "triangle"
    else:
        shape = "square"
    nb=nb_array[i_nb]
    nt=nt_array[i_nt]
    return e_LMTD_max ,Q_LMTD_max, e_NTU_max, Q_NTU_max ,nt, nb, shape #e_LMTD_array,Q_LMTD_array,e_NTU_array,Q_NTU_array

    
e_LMTD_max, Q_LMTD_max, e_NTU_max, Q_NTU_max, i_nt, i_b, shape = run_optimisation(input.shape_array,input.nt_array,input.nt_cross_array,input.l_array,input.lt_array,input.Y_array,input.nb_array)

print("e_LMTD_max: {}, Q_LMTD_max: {},e_NTU_max: {}, Q_NTU_max: {},nt: {}, nb: {}, shape: {}".format(e_LMTD_max, Q_LMTD_max,e_NTU_max, Q_NTU_max,i_nt, i_b, shape))
