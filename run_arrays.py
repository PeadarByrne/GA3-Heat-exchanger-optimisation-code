import functions as fu
import validity_check as check
import thermal_iteration as thermal
import hydraulics_iteration as hydro
import input_arrays as in

#hydraulic_h(Lt,nt)
#hydraulic_c(Lt,Y,nb,N,pitch_shape)
#Thermal(m_h, m_c, nt, nb, Y, Lt, pitch_shape)

#Function runs simulations for geometries in input arrays
def run(shape,nt,nt_cross,l,lt,Y):
    count = 0
    while count >= l