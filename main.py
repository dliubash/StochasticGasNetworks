import numpy as np
import data1
import datetime
import functions3 as func
import functions24 as func2
import setVariables6
from scipy.optimize import minimize

#import pyipopt

#initial guess and bounds
bnds, x0 = setVariables6.setInitials()
# num of variables, eq/ineq, total constr
nvar, neq, nineq, ncon = setVariables6.problemSize()
print('number of variables:', nvar)

#bounds of variables
x_L = np.zeros(nvar)
x_U = np.zeros(nvar)
for i in range(nvar):
    x_L[i] = -1e10 if bnds[i][0] is None else bnds[i][0]
    x_U[i] = 1e10 if bnds[i][1] is None else bnds[i][1]


# constraints
def eval_g(x):
    return np.append(func2.g_eq(x), func2.g_ineq(x))


def eval_jac_g(x, flag): #todo should be like in hs071.py? and in commented part. flag value??
    ret = np.append(func2.g_eq_jac(x), func2.g_ineq_jac(x), axis=0)
    i_s = []
    j_s = []
    if flag:
        for i in range(len(x)):
            for j in range(len(ret)):
                i_s.append(i)
                j_s.append(j)
        return (np.array(i_s), np.array(j_s))
    else:
        return ret.flatten()



# def eval_jac_g(x, flag=True):
#     ret = np.append(func2.g_eq_jac(x, True), func2.g_ineq_jac(x, True), axis=0)
#     if flag:
#         return ret
#     else:
#         ret.flatten()

#max non-zero entries into jacobian
nnzj = len(eval_jac_g(x0, False)) #todo
#max non-zero entries into hessian
nnzh = nvar^2 #S*(n_dem*Nt+n_links*Nx*4+n_links*Nx*4) #todo


#print(eval_g(x0))
print("nnzj = " + str(nnzj))
print("nnzh = " + str(nnzh))
print("ncon = " + str(ncon))
print(nvar*ncon) # =len(eval_jac_g(x0, False))


g_L = np.zeros((len(eval_g(x0))))
g_U = np.zeros_like(g_L)
g_U[neq:] = 1e10 #DL because >= in inequalities


"""
nlp = pyipopt.create(nvar, x_L, x_U, ncon, g_L, g_U, nnzj, nnzh, avg_cost, avg_cost_grad, eval_g, eval_jac_g)


nlp.num_option('bound_relax_factor', 0.1)
nlp.str_option("mu_strategy", "adaptive")
nlp.str_option("derivative_test", "first-order")
nlp.str_option('warm_start_init_point', 'yes')
nlp.str_option('linear_solver', 'mumps')
print(datetime.datetime.now(), ": Going to call solve")
x, zl, zu, constraint_multipliers, obj, status = nlp.solve(x0)
nlp.close()
print(x)
"""

















"""
bnds, x0 = setVariables.setInitials()
nvar, neq, nineq, ncon = setVariables.problemSize()
print('number of variables:', nvar)

cons = ({'type': 'eq',
         'fun': func2.g_eq,
         'jac': lambda x: func2.g_eq_jac(x,True)},
        {'type': 'ineq',
         'fun': func2.g_ineq,
         'jac': lambda x: func2.g_ineq_jac(x,True)})

#todo
#for scipy minimize bounds can be None
res = minimize(func.avg_cost, x0=x0, method='SLSQP', jac=func.avg_cost_grad,
      bounds=bnds, constraints=cons, options={'disp': True})

"""




"""
bnds, x0 = get_bounds_and_initialx()
#print(x0)
nvar = len(x0)
print('number of variables:', nvar)
x_L = np.zeros(nvar) # DL Bounds
x_U = np.zeros(nvar) #DL Bounds
for i in range(nvar):
    x_L[i] = -1e10 if bnds[i][0] is None else bnds[i][0]
    x_U[i] = 1e10 if bnds[i][1] is None else bnds[i][1]
# constraints
neq = len(eq_constr(x0))+len(compr_eq(x0))
ncon = neq+len(ineq_constr(x0))
nnzh = S*(n_dem*Nt+n_links*Nx*4+n_links*Nx*4)


def eval_g(x): #constraints
    return np.append(np.append(eq_constr(x), compr_eq(x)), ineq_constr(x))


def eval_jac_g(x, flag):
    ret = np.append(np.append(eq_constr_jac(x), compr_eq_jac(x), axis=0), ineq_constr_jac(x), axis=0)
    i_s = []
    j_s = []
    if flag:
        for i in range(len(x0)): #DL mb like in hs071.py ncon?
            for j in range(len(ret)): #DL nvar*ncon
                i_s.append(i)
                j_s.append(j)
        return (np.array(i_s), np.array(j_s))
    else:
        return ret.flatten()



nnzj = len(eval_jac_g(x0, False))

print(eval_g(x0))
print("nnzj=" + str(nnzj))
print("ncon=" + str(ncon))
print(nvar*ncon) # =len(eval_jac_g(x0, False))


g_L = np.zeros((len(eval_g(x0)))) #DL why zeros, what about negative values?
g_U = np.zeros_like(g_L)
g_U[neq:] = 1e10 #DL because >= in inequalities
"""

"""
nlp = pyipopt.create(nvar, x_L, x_U, ncon, g_L, g_U, nnzj, nnzh, avg_cost, avg_cost_grad, eval_g, eval_jac_g)


nlp.num_option('bound_relax_factor', 0.1)
nlp.str_option("mu_strategy", "adaptive")
nlp.str_option("derivative_test", "first-order")
nlp.str_option('warm_start_init_point', 'yes')
nlp.str_option('linear_solver', 'mumps')
print(datetime.datetime.now(), ": Going to call solve")
x, zl, zu, constraint_multipliers, obj, status = nlp.solve(x0)
nlp.close()
print(x)
"""




