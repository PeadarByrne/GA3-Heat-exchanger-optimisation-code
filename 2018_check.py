import functions as fu
import single_HX_calculation as HXcalc
import thermal_iteration as thermal
import hydraulics_iteration as hydro

print('2018')

design1=[20,	8,	4,	2,	0.129,	12,	3,	2018,	0.0495,	0.0205]
design2=[24,	6,	2,	2,	0.118,	10,	5,	2018,	0.0495,	0.0225]
design3=[16,	5,	2,	2,	0.156,	10,	4,	2018,	0.0495,	0.0205]

output1=HXcalc.single_HX_analysis(design1[0],design1[1],design1[2],design1[3],design1[4],design1[5],design1[6],design1[7],design1[8],design1[9])
output2=HXcalc.single_HX_analysis(design2[0],design2[1],design2[2],design2[3],design2[4],design2[5],design2[6],design2[7],design2[8],design2[9])
output3=HXcalc.single_HX_analysis(design3[0],design3[1],design3[2],design3[3],design3[4],design3[5],design3[6],design3[7],design3[8],design3[9])

print('Qa = ',output1[1])
print('Qb = ',output2[1])
print('Qc = ',output3[1])


print('Ea = ',output1[0])
print('Eb = ',output2[0])
print('Ec = ',output3[0])


print('m_ca = ',output1[4])
print('m_cb = ',output2[4])
print('m_cc = ',output3[4])


print('m_ha =',output1[5])
print('m_hb =', output2[5])
print('m_hc =',output3[5])
