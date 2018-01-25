import numpy as np
import functions3 as func

def g_eq(x): #constraints
    return np.append(func.eq_constr(x),func.compr_eq(x))

def g_ineq(x): #constraints
    return func.ineq_constr(x)

def g_eq_jac(x, flag=True):
    ret = np.append(func.eq_constr_jac(x), func.compr_eq_jac(x), axis=0)
    if flag:
        return ret
    else:
        return ret.flatten()

def g_ineq_jac(x, flag=True):
    ret = func.ineq_constr_jac(x)
    if flag:
        return ret
    else:
        return ret.flatten()

