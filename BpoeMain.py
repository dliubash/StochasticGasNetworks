import numpy as np
import data1
import datetime
import functions3 as func
import functions24 as func2
import setVariables6
from scipy.optimize import minimize
import BpoeCvarConstrAndObj5 as bpcvar

#import pyipopt

#initial guess and bounds
bnds, x0 = setVariables6.setInitials()
# num of variables, eq/ineq, total constr
nvar, neq, nineq, ncon = setVariables6.problemSizeBpoe()
print('number of variables:', nvar)

#bounds of variables
x_L = np.zeros(nvar)
x_U = np.zeros(nvar)
for i in range(nvar):
    x_L[i] = -1e10 if bnds[i][0] is None else bnds[i][0]
    x_U[i] = 1e10 if bnds[i][1] is None else bnds[i][1]


# constraints
def eval_g(x):
    return np.append(func2.g_eq(x), func2.g_ineq(x), bpcvar.cvar_ineq_constraints(x))

def eval_jac_g(x, flag=True): #todo or it should be like in hs071.py? and in commented part
    ret = np.append(np.append(func2.g_eq_jac(x, True), func2.g_ineq_jac(x, True), axis=0), bpcvar.cvar_ineq_constraints_jac(x, True), axis=0)
    if flag:
        return ret
    else:
        ret.flatten()