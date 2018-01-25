#import numpy as np
import functions3 as func
import functions24 as func2
import BpoeCvarConstrAndObj5 as bpcvar

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

def problemSizeBpoe():
    bnds, x0 =  setInitials() # some bnds are None which is Ok for scipy
    nvar = len(x0)
    #print('number of variables:', nvar)
    neq = len(func2.g_eq(x0))
    nineq = len(func2.g_ineq(x0)) + len(bpcvar.cvar_ineq_constraints(x0))
    ncon = neq + nineq
    return nvar, neq, nineq, ncon
