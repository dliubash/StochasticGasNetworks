#import numpy as np
import functions as func
import functions2 as func2

def setInitials():
    bnds, x0 = func.get_bounds_and_initialx()
    return bnds, x0

def problemSize():
    bnds, x0 =  setInitials() # some bnds are None which is Ok for scipy
    nvar = len(x0)
    #print('number of variables:', nvar)
    neq = len(func2.g_eq(x0))
    nineq = len(func2.g_ineq(x0))
    ncon = neq + nineq
    return nvar, neq, nineq, ncon
