from data import *
from functions import parse_x
from functions import compose_x
from stochDemand import *
from scipy.optimize import minimize
from pynverse import inversefunc

#zeta is maximum deviation from realized demand over the planning horizon
def zetadem(x):
    _, _,  _,  _,  _, dem,  _,  _,  _,  _ = parse_x(x)
    zeta = max(dem[k, j, t] - stochd[k, j, t] for k in range(S) for j in range(n_dem) for t in range(Nt))
    return zeta

#cvar for r.v. ksi defined for S scenarios
def cvar(ksi, alpha):
    f = lambda c: c + (1.0/(1.0-alpha))*sum([max(ksi[k]-c, 0) for k in range(S)])/S #DL lambda c: c + (1.0/(1.0-alpha))*sum([max(cost(x, k)-c, 0) for k in range(S)]) #DL Expectation so divide
    sol = minimize(f, 0.0)
    return sol.fun


def bpoe(x, x_val):
    return 1.0 - inversefunc(cvar, y_values=x_val)

def cvar_constraints(x):
    p, dp, fin, fout, s, dem, pw, slack, px, fx = parse_x(x)
    ret = []
    for j in range(S):
        for i in range(n_links-2): #DL power for active links
            for t in range(Nt):
                ret.append(pw[j, i, t]-c4*fin[j, i+1, t]*(((p[j, i+1, t]+dp[j, i, t])/p[j, i+1, t])**om - 1.0)) #DL i+1 cause active links start from 1, not 0
    return np.array(ret)
