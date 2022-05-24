import validity_check as check
import single_HX_calculation as HXcalc
import functions as fu

#design1=[14,16,2,1,0.238,0.013,4]
# design2=[14,7,2,2,0.238,0.014,3]
# design3=[16,6,2,2,0.207,11.57e-3,4]
# design4=[16,13,2,1,0.207,11.57e-3,4]
# design5=[18,11,2,1,0.182,12e-3,4]


#output1=HXcalc.HX_analysis(design1[0],design1[1],design1[2],design1[3],design1[4],design1[5],design1[6])
# output2=HXcalc.HX_analysis(design2[0],design2[1],design2[2],design2[3],design2[4],design2[5],design2[6])
# output3=HXcalc.HX_analysis(design3[0],design3[1],design3[2],design3[3],design3[4],design3[5],design3[6])
# output4=HXcalc.HX_analysis(design4[0],design4[1],design4[2],design4[3],design4[4],design4[5],design4[6])
# output5=HXcalc.HX_analysis(design5[0],design5[1],design5[2],design5[3],design5[4],design5[5],design5[6])
#output6=HXcalc.HX_analysis(design6[0],design6[1],design6[2],design6[3],design6[4],design6[5],design6[6])

#print('Q1 = ',output1[1])
# print('Q2 = ',output2[1])
# print('Q3 = ',output3[1])
# print('Q4 = ',output4[1])
# print('Q5 = ',output5[1])
#print('Q6 = ',output6[1])

# print('e1 = ',output1[0])
# print('e2 = ',output2[0])
# print('e3 = ',output3[0])
# print('e4 = ',output4[0])
# print('e5 = ',output5[0])

print(fu.A_sh(0.014,12,0.232,1))