import validity_check as check
import single_HX_calculation as HXcalc
import functions as fu

design1=[14,12,1,1,0.232.0.01304,4]
design2=[]
design3=[]
design4=[]
design5=[]
design6=[]

output1=HXcalc.HX_analysis(design1[0],design1[1],design1[2],design1[3],design1[4],design1[5],design1[6])
output2=HXcalc.HX_analysis(design2[0],design2[1],design2[2],design2[3],design2[4],design2[5],design2[6])
output3=HXcalc.HX_analysis(design3[0],design3[1],design3[2],design3[3],design3[4],design3[5],design3[6])
output4=HXcalc.HX_analysis(design4[0],design4[1],design4[2],design4[3],design4[4],design4[5],design4[6])
output5=HXcalc.HX_analysis(design5[0],design5[1],design5[2],design5[3],design5[4],design5[5],design5[6])
output6=HXcalc.HX_analysis(design6[0],design6[1],design6[2],design6[3],design6[4],design6[5],design6[6])

print('Qa = ',output1[1])
print('Qb = ',output2[1])
print('Qc = ',output3[1])
print('Qd = ',output4[1])
print('Qe = ',output5[1])
print('Qf = ',output6[1])

print('Ea = ',output1[0])
print('Eb = ',output2[0])
print('Ec = ',output3[0])
print('Ed = ',output4[0])
print('Ee = ',output5[0])
print('Ee = ',output5[0])


