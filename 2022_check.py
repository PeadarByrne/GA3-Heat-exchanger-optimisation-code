import validity_check as check
import single_HX_calculation as HXcalc
import functions as fu
import thermal_iteration as thermal

design1=[14,12,1,1,0.232,0.014,4,2022,57.5e-3,57.5e-3]
design2=[16,6,1,1,0.21,0.01,3,2022,50e-3,50e-3]
design3=[20,4,2,1,0.165,0.01,4,2022,53.5e-3,50e-3]
design4=[12,8,2,1,0.25,0.012,3,2022,53e-3,30e-3]
design5=[24,4,4,1,0.136,0.010,4,2022,53e-3,41e-3]
design6=[20,6,4,2,0.163,0.010,3,2022,58e-3,23e-3]
design7=[13, 14,1,1,0.35,0.012,3,2022,0.0535,0.5350] #JPL-2018 tested 2022
design8=[14,12,	2,2,0.221,0.015,3,2022,0.0410,0.0230] #2017-B tested 2022




output1=HXcalc.single_HX_analysis(design1[0],design1[1],design1[2],design1[3],design1[4],design1[5],design1[6],design1[7],design1[8],design1[9])
output2=HXcalc.single_HX_analysis(design2[0],design2[1],design2[2],design2[3],design2[4],design2[5],design2[6],design2[7],design2[8],design2[9])
output3=HXcalc.single_HX_analysis(design3[0],design3[1],design3[2],design3[3],design3[4],design3[5],design3[6],design3[7],design3[8],design3[9])
output4=HXcalc.single_HX_analysis(design4[0],design4[1],design4[2],design4[3],design4[4],design4[5],design4[6],design4[7],design4[8],design4[9])
output5=HXcalc.single_HX_analysis(design5[0],design5[1],design5[2],design5[3],design5[4],design5[5],design5[6],design5[7],design5[8],design5[9])
output6=HXcalc.single_HX_analysis(design6[0],design6[1],design6[2],design6[3],design6[4],design6[5],design6[6],design6[7],design6[8],design6[9])
output7=HXcalc.single_HX_analysis(design7[0],design7[1],design7[2],design7[3],design7[4],design7[5],design7[6],design7[7],design7[8],design7[9])
output8=HXcalc.single_HX_analysis(design8[0],design8[1],design8[2],design8[3],design8[4],design8[5],design8[6],design8[7],design8[8],design8[9])

print('2022')
print('Qa     = ',output1[1])
print('Qb     = ',output2[1])
print('Qc     = ',output3[1])
print('Qd     = ',output4[1])
print('Qe     = ',output5[1])
print('Qf     = ',output6[1])
print('Q_jpl  = ',output7[1])
print('Q_2017 = ',output8[1])

print('Ea     = ',output1[0])
print('Eb     = ',output2[0])
print('Ec     = ',output3[0])
print('Ed     = ',output4[0])
print('Ee     = ',output5[0])
print('Ef     = ',output6[0])
print('E_jpl  = ',output7[0])
print('E_2017 = ',output8[0])

print('m_ca   = ',output1[4])
print('m_cb   = ',output2[4])
print('m_cc   = ',output3[4])
print('m_cd   = ',output4[4])
print('m_ce   = ',output5[4])
print('m_cf   = ',output6[4])
print('m_cjpl  = ',output7[4])
print('m_c2017 = ',output8[4])

print('m_ha   =',output1[5])
print('m_hb   =',output2[5])
print('m_hc   =',output3[5])
print('m_hd   =',output4[5])
print('m_he   =',output5[5])
print('m_hf   =',output6[5])
print('m_hjpl  =',output7[5])
print('m_h2017 =',output8[5])

