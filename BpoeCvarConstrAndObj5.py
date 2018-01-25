from data1 import *
from functions3 import parse_x
from stochDemand2 import *
from scipy.optimize import minimize
from pynverse import inversefunc

#cvar for r.v. ksi defined for S scenarios
def cvar(ksi, alpha):
    f = lambda c: c + (1.0/(1.0-alpha))*sum([max(ksi[k]-c, 0) for k in range(S)])/S #DL lambda c: c + (1.0/(1.0-alpha))*sum([max(cost(x, k)-c, 0) for k in range(S)]) #DL Expectation so divide
    sol = minimize(f, 0.0)
    return sol.fun

def cvar_ineq_constraints(x):
    #inequalities
    _, _, _, _, _, dem, _, _, px, fx = parse_x(x)
    ret = []

    # zeta is maximum deviation from realized demand over the planning horizon
    zetad = []
    for k in range(S):
        zetad.append(max(dem[k, j, t] - stochd[k, j, t] for j in range(n_dem) for t in range(Nt)))
    #cvar of zetad
    ret.append(-cvar(zetad, alphad) + dstar)

    zetaf = []
    for k in range(S):
        ssfcost = 0.0
        for i in range(n_links):
            for j in range(Nx):
                ssfcost += cT * (fx[k, i, Nt - 1, j] - fx[k, i, 0, j]) ** 2.0*dx[i]
        zetaf.append(1e-6*ssfcost)
    #cvar of zetaf
    ret.append(-cvar(zetaf, alphaf) + fstar)

    zetap = []
    for k in range(S):
        sspcost = 0.0
        for i in range(n_links):
            for j in range(Nx):
                sspcost += cT*(px[k, i, Nt-1, j] - px[k, i, 0, j])**2.0*dx[i]
        zetap.append(1e-6 * sspcost)
    #cvar of zetap
    ret.append(-cvar(zetap, alphap) + pstar)

    return np.array(ret)


def cvar_ineq_constraints_jac(x, flag = True): #todo
    _, _, _, _, _, dem, _, _, px, fx = parse_x(x)
    ret = np.zeros((3, len(x)))
    return ret

def objbPOE(x):
    _, _, _, _, _, _, pw, _, _, _ = parse_x(x)
    #cost of compressor operation
    comprCost = []
    for k in range(S):
        boostcost = 0.0
        for j in range(n_links - 2):
            for t in range(Nt):
                boostcost += ce * pw[k, j, t] * (dt / 3600.0)
        comprCost.append(boostcost)

    bpoeCost = bpoe(boostcost) #todo !!!!!
    return bpoeCost


#bpoe by definition
def bpoe(x_val):
    return 1.0 - inversefunc(cvar, y_values=x_val)


def objbPOE_jac(x, flag = True): #todo
    return

