import functions as fu

#check that we have enough copper tube
Lt_used = (fu.Lt + fu.Lt_extra) * fu.nt
if Lt_used > fu.Lt_total:
    raise ValueError('This design uses too much copper pipe')

#check that tubes fit in shell
d_t_total = (fu.nt_cross +1)*fu.Y
if d_t_total > fu.d_sh:
    raise ValueError('The pipes do not fit in the shell')

#check that HX in not overweight
#mass_total = 
#if mass_total > fu.mass_limit:
    raise ValueError('This design is overweight')

