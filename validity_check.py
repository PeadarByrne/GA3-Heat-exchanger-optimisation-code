import functions as fu

#check that we have enough pipe
Lt_used = (fu.Lt + fu.Lt_extra) * fu.nt
if Lt_used > fu.Lt_total:
    raise ValueError('This design uses too much copper pipe')

#check that pipes fit in shell




