import numpy as np
import functions as func

def g_eq(x): #constraints
    return np.append(func.eq_constr(x),func.compr_eq(x))

def g_ineq(x): #constraints
    return func.ineq_constr(x)

def g_eq_jac(x, flag=True):
    ret = np.append(func.eq_constr_jac(x), func.compr_eq_jac(x), axis=0)
    # i_s = []
    # j_s = []
    if flag:
        return ret
        # for i in range(len(x)):
        #     for j in range(len(ret)):
        #         i_s.append(i)
        #         j_s.append(j)
        # return (np.array(i_s), np.array(j_s))
    else:
        return ret.flatten()

def g_ineq_jac(x, flag=True):
    ret = func.ineq_constr_jac(x)
    # i_s = []
    # j_s = []
    if flag:
        return ret
        # for i in range(len(x)):
        #     for j in range(len(ret)):
        #         i_s.append(i)
        #         j_s.append(j)
        # return (np.array(i_s), np.array(j_s))
    else:
        return ret.flatten()