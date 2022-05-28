from numpy import append
import functions as fu
#import validity_check as check
import single_HX_calculation as HXcalc
import input_arrays as input
import validity_check as check


def run_optimisation(nt_array,nb_array,passes_array,Lt_array,pitch_array):
    #initialise output array
    output_array = []
    Q_output_array = []


    for i in range(len(passes_array)):
        #Iterates different configurations of passes
        Nt=passes_array[i][0]
        Ns=passes_array[i][1]

        for j in range(len(nt_array)):
            #iterates for different numbers of tubes
            nt=nt_array[j]

            #find Lt
            if Nt==1:
                Lt=Lt_array[0][j]
            elif Nt==2:
                Lt=Lt_array[1][j]
            
            #find Y
            Y=pitch_array[j]

            #find N the number of rows passed
            N = input.choose_N(nt,Nt)
            
            for k in range(len(nb_array)):
                #iterate for different number of baffles
                nb=nb_array[k]

                #uncomment below to run analysis without mass checks
                # e_LMTD , Q_LMTD, e_NTU, Q_NTU = HXcalc.HX_analysis(nt,nb,Nt,Ns,Lt,Y,N)
                # #append results into one output array
                # output=[nt,nb,Nt,Ns,Lt,Y,Q_LMTD,e_LMTD]
                # output_array.append(output)
                # Q_output_array.append(Q_LMTD)


                #Check if design is overweight
                try:
                    check.CheckMass(Lt,nt,nb,Nt,Ns)
                    #run single analysis
                    e_LMTD , Q_LMTD, e_NTU, Q_NTU, m_c, m_h = HXcalc.single_HX_analysis(nt,nb,Nt,Ns,Lt,Y,N,2022)
                    #append results into one output array
                    output=[nt,nb,Nt,Ns,Lt,Y,Q_LMTD, e_LMTD,m_c,m_h]    #added Q to this array so all design data in this array
                    output_array.append(output)
                    Q_output_array.append(Q_LMTD)
                except ValueError:
                    print('Illegal design skipped')
                k+=1
            
    #Find index of best heat transfer case
    N_designs = 20  #number of top designs to print
    top_designs = []    #array of top designs
    for i in range(N_designs):
        index_max, Q_LMTD = fu.return_max(Q_output_array)
        top_designs.append(output_array.pop(index_max))
        Q_top_design = Q_output_array.pop(index_max)
    
    return top_designs #nt,nb,Nt,Ns,Lt,Y,e_LMTD,Q_LMTD

top_designs =run_optimisation(input.nt_array,input.nb_array,input.passes_array,input.Lt_array,input.pitch_array)
print(top_designs)

top_design=top_designs[0]    
#Find design values of best case
nt=top_design[0]
nb=top_design[1]
Nt=top_design[2]
Ns=top_design[3]
Lt=top_design[4]
Y=top_design[5]
Q_LMTD = top_design[6]
e_LMTD = top_design[7]
m_c = top_design[8]
m_h = top_design[9]

print('nt = ',nt)
print('nb = ',nb)
print('Nt = ',Nt)
print('Ns = ',Ns)
print('Lt = ',Lt)
print('Y = ',Y)
print('e_LMTD = ',e_LMTD)
print('Q_LMTD = ',Q_LMTD)
print('m_c = ',m_c)
print('m_h = ',m_h)
