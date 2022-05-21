from numpy import append
import functions as fu
#import validity_check as check
import single_HX_calculation as HXcalc
import input_arrays as input

def choose_N(nt):
    if nt>15:
        N=4
    else:
        N=3
    return N

def run_optimisation(nt_array,nb_array,passes_array,Lt_array,pitch_array):
    #initialise output array
    output_array = []
    Q_output_array = []


    #passes loop
    for i in range(len(passes_array)):
        #Iterates different passes
        Nt=passes_array[i][0]
        Ns=passes_array[i][1]

        #nt loop
        for j in range(len(nt_array)):
            nt=nt_array[j]

            #find Lt
            if Nt==1:
                Lt=Lt_array[0][j]
            elif Nt==2:
                Lt=Lt_array[1][j]
            
            #find Y
            Y=pitch_array[j]

            N = choose_N(nt)
            
            
            #nb loop
            for k in range(len(nb_array)):
                nb=nb_array[k]

                #run single analysis
                e_LMTD , Q_LMTD, e_NTU, Q_NTU = HXcalc.HX_analysis(nt,nb,Nt,Ns,Lt,Y,N)
                #append results into one output array
                output=[nt,nb,Nt,Ns,Lt,Y,e_LMTD]
                output_array.append(output)
                Q_output_array.append(Q_LMTD)
                k+=1
            
    #Find index of best heat transfer case
    index_max, Q_LMTD = fu.return_max(Q_output_array)
    #Find design values of best case
    nt=output_array[index_max][0]
    nb=output_array[index_max][1]
    Nt=output_array[index_max][2]
    Ns=output_array[index_max][3]
    Lt=output_array[index_max][4]
    Y=output_array[index_max][5]
    #Find effectiveness of best case
    e_LMTD=output_array[index_max][6]
    return nt,nb,Nt,Ns,Lt,Y,e_LMTD,Q_LMTD

           
nt,nb,Nt,Ns,Lt,Y,e_LMTD,Q_LMTD=run_optimisation(input.nt_array,input.nb_array,input.passes_array,input.Lt_array,input.pitch_array)
print('nt = ',nt)
print('nb = ',nb)
print('Nt = ',Nt)
print('Ns = ',Ns)
print('Lt = ',Lt)
print('Y = ',Y)
print('e_LMTD = ',e_LMTD)
print('Q_LMTD = ',Q_LMTD)