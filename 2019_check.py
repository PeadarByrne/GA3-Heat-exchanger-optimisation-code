import functions as fu
import single_HX_calculation as HXcalc
import thermal_iteration as thermal
import hydraulics_iteration as hydro

print('2019')

design1=[]
design2=[]
design3=[]
design4=[]
design5=[]
design6=[]

output1=HXcalc.single_HX_analysis(design1[0],design1[1],design1[2],design1[3],design1[4],design1[5],design1[6],design1[7],design1[8],design1[9])
output2=HXcalc.single_HX_analysis(design2[0],design2[1],design2[2],design2[3],design2[4],design2[5],design2[6],design2[7],design2[8],design1[9])
output3=HXcalc.single_HX_analysis(design3[0],design3[1],design3[2],design3[3],design3[4],design3[5],design3[6],design3[7],design3[8],design1[9])
output4=HXcalc.single_HX_analysis(design4[0],design4[1],design4[2],design4[3],design4[4],design4[5],design4[6],design4[7],design4[8],design1[9])
output5=HXcalc.single_HX_analysis(design5[0],design5[1],design5[2],design5[3],design5[4],design5[5],design5[6],design5[7],design5[8],design1[9])
output6=HXcalc.single_HX_analysis(design6[0],design6[1],design6[2],design6[3],design6[4],design6[5],design6[6],design6[7],design6[8],design1[9])

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
print('Ef = ',output6[0])

print('m_ca = ',output1[4])
print('m_cb = ',output2[4])
print('m_cc = ',output3[4])
print('m_cd = ',output4[4])
print('m_ce = ',output5[4])
print('m_cf = ',output6[4])

print('m_ha',output1[5])
print('m_hb',output2[5])
print('m_hc',output3[5])
print('m_hd',output4[5])
print('m_he',output5[5])
print('m_hf',output6[5])

