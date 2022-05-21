from numpy import append
import functions as fu
#import validity_check as check
import single_HX_calculation as HXcalc
import input_arrays as input


def run_optimisation(nt_array,nb_array,passes_array,Lt_array,pitch_array,N_array)  :
    #initialise output array
    output_array = []

    #passes loop
    for i in range(len(passes_array)):
        #Iterates different passes
        Nt=passes_array[i,0]
        Ns=passes_array[i,1]

        #nt loop
        for j in range(len(nt_array)):
            nt=nt_array[j]

            #find Lt
            if Nt==1:
                Lt=Lt_array[j,0]
            elif Nt==2:
                Lt=Lt_array[j,1]
            
            #find Y
            Y=pitch_array[j]

            if nt>15:
                N=4
            else:
                N=3
            
            
            #nb loop
            for k in range(len(nb_array)):
                nb=nb_array[k]

                #run single analysis
                e_LMTD , Q_LMTD, e_NTU, Q_NTU = HXcalc.HX_analysis(nt,nb,Nt,Ns,Lt,Y,N)
                #append results into one output array
                output=[nt,nb,Nt,Ns,e_LMTD,Q_LMTD]
                output_array.append(output)

           
