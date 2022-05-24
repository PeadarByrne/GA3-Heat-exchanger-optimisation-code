import validity_check as check
import single_HX_calculation as HXcalc


design1=[12,7,2,2,0.238,,]
design2=[16,6,2,2,0.207,,]
design3=[14,16,2,1,0.238,,]
design4=[16,13,2,1,0.207,,]
design5=[18,5,2,2,0.182,,]
design6=[18,11,2,1,0.182,,]

output1=HXcalc.HX_analysis(design1[0],design1[1],design1[2],design1[3],design1[4],design1[5],design1[6])