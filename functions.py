#  contains all functions used for optimization
#import numpy as np
from scipy.optimize import minimize
from data import*
from pynverse import inversefunc
from stochDemand import *

def parse_x(x):
    # node pressure - [bar]
    p = np.reshape(x[:S*n_nodes*Nt], (S, n_nodes, Nt))
    # compressor boost - [bar]
    dp = np.reshape(x[S*n_nodes*Nt:S*n_nodes*Nt+S*(n_links-2)*Nt], (S, n_links-2, Nt))
    # flow in pipe - [scmx10-4/hr]
    fin = np.reshape(x[S*Nt*(n_nodes+n_links-2):S*Nt*(n_nodes+2*n_links-2)], (S, n_links, Nt))
    # flow out pipe - [scmx10-4/hr]
    fout = np.reshape(x[S*Nt*(n_nodes+2*n_links-2):S*Nt*(n_nodes+3*n_links-2)], (S, n_links, Nt))
    # supply flow - [scmx10-4/hr]
    s = np.reshape(x[S*Nt*(n_nodes+3*n_links-2):S*Nt*(n_nodes+3*n_links-2+n_sup)], (S, n_sup, Nt))
    # demand flow - [scmx10-4/hr]
    dem = np.reshape(x[S*Nt*(n_nodes+3*n_links-2+n_sup):S*Nt*(n_nodes+3*n_links-2+n_sup+n_dem)], (S, n_dem, Nt))
    # compressor power [kW]
    pw = np.reshape(x[S*Nt*(n_nodes+3*n_links-2+n_sup+n_dem):S*Nt*(n_nodes+4*n_links-4+n_sup+n_dem)], (S, n_links-2, Nt))
    # auxiliary variable
    slack = np.reshape(x[S*Nt*(n_nodes+4*n_links-4+n_sup+n_dem):S*Nt*(n_nodes+4*n_links-4+n_sup+n_dem+n_links*Nx)],
                       (S, n_links, Nt, Nx))
    # link pressure profile - [bar]
    px = np.reshape(x[S*Nt*(n_nodes+4*n_links-4+n_sup+n_dem+n_links*Nx):S*Nt*(n_nodes+4*n_links-4+n_sup+n_dem+2*n_links*Nx)],
                    (S, n_links, Nt, Nx))
    # link flow profile - [scmx10-4/hr]
    fx = np.reshape(x[S*Nt*(n_nodes+4*n_links-4+n_sup+n_dem+2*n_links*Nx):S*Nt*(n_nodes+4*n_links-4+n_sup+n_dem+3*n_links*Nx)],
                    (S, n_links, Nt, Nx))
    return p, dp, fin, fout, s, dem, pw, slack, px, fx


def compose_x(p=np.zeros((S, n_nodes, Nt)), dp=np.zeros((S, n_links-2, Nt)), fin=np.zeros((S, n_links, Nt)),
              fout=np.zeros((S, n_links, Nt)), s=np.zeros((S, n_sup, Nt)), dem=np.zeros((S, n_dem, Nt)),
              pw=np.zeros((S, n_links-2, Nt)), slack=np.zeros((S, n_links, Nt, Nx)),
              px=np.zeros((S, n_links, Nt, Nx)), fx=np.zeros((S, n_links, Nt, Nx))):
    x = np.zeros(S*Nt*(n_nodes+4*n_links-4+n_sup+n_dem+3*n_links*Nx))
    # node pressure - [bar]
    x[:S * n_nodes * Nt] = np.reshape(p, (S*n_nodes*Nt))
    # compressor boost - [bar]
    x[S * n_nodes * Nt:S * n_nodes * Nt + S * (n_links - 2) * Nt] = np.reshape(dp, (S*(n_links - 2)*Nt))
    # flow in pipe - [scmx10-4/hr]
    x[S * Nt * (n_nodes + n_links - 2):S * Nt * (n_nodes + 2 * n_links - 2)] = np.reshape(fin, (S*n_links*Nt))
    # flow out pipe - [scmx10-4/hr]
    x[S * Nt * (n_nodes + 2 * n_links - 2):S * Nt * (n_nodes + 3 * n_links - 2)] = np.reshape(fout, (S*n_links*Nt))
    # supply flow - [scmx10-4/hr]
    x[S * Nt * (n_nodes + 3 * n_links - 2):S * Nt * (n_nodes + 3 * n_links - 2 + n_sup)] = np.reshape(s, (S*n_sup*Nt))
    # demand flow - [scmx10-4/hr]
    x[S * Nt * (n_nodes + 3 * n_links - 2 + n_sup):S * Nt * (n_nodes + 3 * n_links - 2 + n_sup + n_dem)] = \
        np.reshape(dem, (S*n_dem*Nt))
    # compressor power [kW]
    x[S * Nt * (n_nodes + 3 * n_links - 2 + n_sup + n_dem):S * Nt * (n_nodes + 4 * n_links - 4 + n_sup + n_dem)] = \
        np.reshape(pw,(S*(n_links - 2)*Nt))
    # auxiliary variable
    x[S * Nt * (n_nodes + 4 * n_links - 4 + n_sup + n_dem):S * Nt * (n_nodes + 4 * n_links - 4 + n_sup + n_dem + n_links * Nx)]= \
        np.reshape(slack, (S*n_links*Nt*Nx))
    # link pressure profile - [bar]
    x[S * Nt * (n_nodes + 4 * n_links - 4 + n_sup + n_dem + n_links * Nx):S * Nt * (n_nodes + 4 * n_links - 4 + n_sup + n_dem + 2 * n_links * Nx)] =\
        np.reshape(px, (S*n_links*Nt*Nx))
    # link flow profile - [scmx10-4/hr]
    x[S * Nt * (n_nodes + 4 * n_links - 4 + n_sup + n_dem + 2 * n_links * Nx):S * Nt * (n_nodes + 4 * n_links - 4 + n_sup + n_dem + 3 * n_links * Nx)]=\
        np.reshape(fx, (S*n_links*Nt*Nx))
    return x


def get_bounds_and_initialx():
    x0 = np.ones(S*Nt*(n_nodes+4*n_links-4+n_sup+n_dem+3*n_links*Nx))
    bnds = []
    # node pressure - [bar]
    pmax_arr = np.ones((S, n_nodes, Nt))
    pmin_arr = np.ones((S, n_nodes, Nt))
    for i in range(n_nodes):
        pmax_arr[:, i, :] = pmax[i]
        pmin_arr[:, i, :] = pmin[i]
    pmax_arr = np.reshape(pmax_arr, S*n_nodes*Nt)
    pmin_arr = np.reshape(pmin_arr, S*n_nodes*Nt)
    x0[:S * n_nodes * Nt] = 50.0
    for i in range(S*n_nodes*Nt):
        bnds.append((pmin_arr[i], pmax_arr[i]))
    # compressor boost - [bar]
    x0[S * n_nodes * Nt:S * n_nodes * Nt + S * (n_links - 2) * Nt] = 10.0 #DL '- 2' cause 2 inactive links
    for i in range(S * (n_links - 2) * Nt):
        bnds.append((0.0, 100.0))
    # flow in pipe - [scmx10-4/hr]
    x0[S * Nt * (n_nodes + n_links - 2):S * Nt * (n_nodes + 2 * n_links - 2)] = 100.0
    for i in range(S*n_links*Nt):
        bnds.append((1.0, 500.0))
    # flow out pipe - [scmx10-4/hr]
    x0[S * Nt * (n_nodes + 2 * n_links - 2):S * Nt * (n_nodes + 3 * n_links - 2)] = 100.0
    for i in range(S*n_links*Nt):
        bnds.append((1.0, 500.0))
    # supply flow - [scmx10-4/hr]
    x0[S * Nt * (n_nodes + 3 * n_links - 2):S * Nt * (n_nodes + 3 * n_links - 2 + n_sup)] = 10.0
    for i in range(S*n_sup*Nt):
        bnds.append((0.01, smax[0])) # DL: because smax contains 1 element; otherwise smax[j], j in SUP
    # demand flow - [scmx10-4/hr]
    x0[S * Nt * (n_nodes + 3 * n_links - 2 + n_sup):S * Nt * (n_nodes + 3 * n_links - 2 + n_sup + n_dem)] = 100.0
    for i in range(S*n_dem*Nt):
        bnds.append((None, None))
    # compressor power [kW]
    x0[S * Nt * (n_nodes + 3 * n_links - 2 + n_sup + n_dem):S * Nt * (n_nodes + 4 * n_links - 4 +n_sup+n_dem)] = 1000.0
    for i in range(S * (n_links - 2) * Nt):
        bnds.append((0.0, 3000.0))
    # auxiliary variable
    x0[S * Nt * (n_nodes + 4 * n_links - 4 + n_sup + n_dem):S * Nt * (
        n_nodes + 4 * n_links - 4 + n_sup + n_dem + n_links * Nx)] = 10.0
    for i in range(S*n_links*Nt*Nx):
        bnds.append((0.0, None))
    # link pressure profile - [bar]
    x0[S * Nt * (n_nodes + 4 * n_links - 4 + n_sup + n_dem + n_links * Nx):S * Nt * (
        n_nodes + 4 * n_links - 4 + n_sup + n_dem + 2 * n_links * Nx)] = 50.0
    for i in range(S*n_links*Nt*Nx):
        bnds.append((20.0, 100.0))
    # link flow profile - [scmx10-4/hr]
    x0[S * Nt * (n_nodes + 4 * n_links - 4 + n_sup + n_dem + 2 * n_links * Nx):S * Nt * (
        n_nodes + 4 * n_links - 4 + n_sup + n_dem + 3 * n_links * Nx)] = 100.0
    for i in range(S*n_links*Nt*Nx):
        bnds.append((1.0, 500.0))
    return bnds, x0



# cost function #DL for each scenario
def cost(x, k):
    assert k <= S
    _, _, _, _, s, dem, pw, _, px, fx = parse_x(x)
    supcost = 0.0 #DL seems to be omitted in Zavala2013 paper but included into its code (actually, was 0 anyway)
    for j in range(n_sup):
        for t in range(Nt):
            supcost += cs*s[k, j, t]*(dt/3600.0)
    boostcost = 0.0
    for j in range(n_links-2):
        for t in range(Nt):
            boostcost += ce*pw[k, j, t]*(dt/3600.0)
    trackcost = 0.0
    for j in range(n_dem):
        for t in range(Nt):
            trackcost += cd*(dem[k, j, t] - stochd[k, j, t])**2.0
    sspcost = 0.0
    for i in range(n_links):
        for j in range(Nx):
            sspcost += cT*(px[k, i, Nt-1, j] - px[k, i, 0, j])**2.0
    ssfcost = 0.0
    for i in range(n_links):
        for j in range(Nx):
            ssfcost += cT * (fx[k, i, Nt - 1, j] - fx[k, i, 0, j]) ** 2.0 # DL mb times dx[i] for track-,ssp-,ssfcost
    return 1e-6*(supcost+boostcost+trackcost+sspcost+ssfcost)


# gradient of cost function
def cost_grad(x, k):
    assert k <= S
    _, _, _, _, s, dem, pw, _, px, fx = parse_x(x)
    d_s = np.zeros(np.shape(s))
    for j in range(n_sup):
        for t in range(Nt):
            d_s[k, j, t] = 1e-6*cs*(dt/3600.0)
    d_dem = np.zeros(np.shape(dem))
    for j in range(n_dem):
        for t in range(Nt):
            d_dem[k, j, t] = 1e-6*2*cd*(dem[k, j, t] - stochd[k, j, t])
    d_pw = np.zeros(np.shape(pw))
    for j in range(n_links-2):
        for t in range(Nt):
            d_pw[k, j, t] = 1e-6*ce*(dt/3600.0)
    d_px = np.zeros(np.shape(px))
    for i in range(n_links):
        for j in range(Nx):
            d_px[k, i, Nt-1, j] = 1e-6*2*cT*(px[k, i, Nt-1, j] - px[k, i, 0, j])
            d_px[k, i, 0, j] = -1e-6*2*cT*(px[k, i, Nt-1, j] - px[k, i, 0, j])
    d_fx = np.zeros(np.shape(fx))
    for i in range(n_links):
        for j in range(Nx):
            d_fx[k, i, Nt-1, j] = 1e-6*2*cT*(fx[k, i, Nt-1, j] - fx[k, i, 0, j])
            d_fx[k, i, 0, j] = -1e-6*2*cT*(fx[k, i, Nt-1, j] - fx[k, i, 0, j])
    d_x = compose_x(s=d_s, dem=d_dem, pw=d_pw, px=d_px, fx=d_fx)
    return d_x


# average cost
def avg_cost(x):
    ret = 0.0
    for k in range(S):
        ret += cost(x, k)
    return ret/S


# gradient of average cost
def avg_cost_grad(x):
    ret = 0.0
    for k in range(S):
        ret += cost_grad(x, k)
    return ret / S


# equality constraints
def eq_constr(x):
    ret = []
    p, dp, fin, fout, s, dem, pw, slack, px, fx = parse_x(x)
    # node balances #DL
    for k in range(S):
        for i in range(n_nodes):
            for t in range(Nt):
                ret.append((s[k, 0, t] if i == 0 else fout[k, i-1, t]) -
                           (dem[k, 0, t] if i == n_nodes-1 else fin[k, i, t]))
    # flow equations for passive and active links
    for j in range(S):
        for i in range(n_links):
            for t in range(Nt-1):
                for k in range(Nx-1):
                    ret.append((px[j, i, t+1, k]-px[j, i, t, k])/dt +
                               c1[i]*(fx[j, i, t+1, k+1]-fx[j, i, t+1, k])/(dx[i]))
    # boundary conditions flow
    for j in range(S):
        for i in range(n_links):
            for t in range(Nt):
                ret.append(fx[j, i, t, 0]-fin[j, i, t])
                ret.append(fx[j, i, t, Nx-1]-fout[j, i, t])
    # pressure equations for passive and active links
    for j in range(S):
        for i in range(n_links):
            for t in range(Nt-1):
                for k in range(Nx-1):
                    ret.append(-(fx[j, i, t+1, k]-fx[j, i, t, k])/dt
                               - c2[i]*(px[j, i, t+1, k+1]-px[j, i, t+1, k])/dx[i] - slack[j, i, t+1, k])
    # slack equations
    for j in range(S):
        for i in range(n_links):
            for t in range(Nt-1):
                for k in range(Nx):
                    ret.append(slack[j, i, t, k]*px[j, i, t, k] - c3[i]*fx[j, i, t, k]*fx[j, i, t, k])
    # boundary conditions pressure, passive links #DL passive links - first and last
    for j in range(S):
        for t in range(Nt):
            ret.append(px[j, 0, t, 0] - p[j, 0, t])
            ret.append(px[j, n_links-1, t, 0] - p[j, n_links-1, t])
            ret.append(px[j, 0, t, Nx-1] - p[j, 1, t])
            ret.append(px[j, n_links-1, t, Nx-1] - p[j, n_links, t])
    # boundary conditions, active links
    for j in range(S):
        for i in range(n_links-2):
            for t in range(Nt):
                ret.append(-px[j, i+1, t, 0]+p[j, i+1, t]+dp[j, i, t])
                ret.append(px[j, i+1, t, Nx-1]-p[j, i+2, t])
    # fix pressure at supply nodes
    for k in range(S):
        for t in range(Nt):
            ret.append(p[k, 0, t] - pmin[0])
    # non-anticipativity constraints #todo
    for j in range(S):
        for i in range(n_links-2):
            for t in range(TDEC):
                ret.append(dp[j, i, t] - dp[0, i, t])  # DL dp[1, i, t])

    for j in range(S):
        for t in range(TDEC):
            ret.append(dem[j, 0, t] -  dem[0, 0, t]) #DL dem[1, 0, t])
    # ss constraints
    for j in range(S):
        for i in range(n_links):
            for k in range(Nx-1):
                ret.append(fx[j, i, 0, k+1]-fx[j, i, 0, k])
                ret.append(- c2[i]*(px[j, i, 0, k+1]-px[j, i, 0, k])/dx[i] - slack[j, i, 0, k])
    return np.array(ret)


# jacobian of equality constraints
def eq_constr_jac(x):
    n = len(eq_constr(x))
    m = len(x)
    ret = np.zeros((n, m))
    p, _, _, _, _, _, _, slack, px, fx = parse_x(x)
    for j in range(m):
        x0 = np.zeros(m)
        x0[j] = 1.0
        ret[:, j] = eq_constr(x0) #DL thus we get coefficients in linear constraints w.r.t. variable
    # slack equations
    idx = S*n_links*(2*Nt+2*(Nt-1)*(Nx-1))+S*n_nodes*Nt
    for j in range(S):
        for i in range(n_links):
            for t in range(Nt - 1):
                for k in range(Nx):
                    d_slack = np.zeros(np.shape(slack))
                    d_slack[j, i, t, k] = px[j, i, t, k]
                    d_px = np.zeros(np.shape(px))
                    d_px[j, i, t, k] = slack[j, i, t, k]
                    d_fx = np.zeros(np.shape(fx))
                    d_fx[j, i, t, k] = -2*c3[i]*fx[j, i, t, k]
                    ret[idx, :] = compose_x(slack=d_slack, px=d_px, fx=d_fx)
                    idx += 1
    # fix pressure at supply nodes
    idx += S*Nt*4+S*(n_links-2)*Nt*2 #DL S*Nt*4+S*n_links*2
    for k in range(S):
        for t in range(Nt):
            d_p = np.zeros(np.shape(p))
            d_p[k, 0, t] = 1.0
            ret[idx, :] = compose_x(p=d_p)
            idx += 1 #DL 1/18/18
    return ret




# compressor equations
def compr_eq(x):
    p, dp, fin, _, _, _, pw, _, _, _ = parse_x(x)
    ret = []
    for j in range(S):
        for i in range(n_links-2): #DL power for active links
            for t in range(Nt):
                ret.append(pw[j, i, t]-c4*fin[j, i+1, t]*(((p[j, i+1, t]+dp[j, i, t])/p[j, i+1, t])**om - 1.0)) #DL i+1 cause active links start from 1, not 0
    return np.array(ret)


# compressor equations jacobian
def compr_eq_jac(x):
    p, dp, fin, _, _, _, pw, _, _, _ = parse_x(x)
    ret = np.zeros((S*(n_links-2)*Nt, len(x)))
    idx = 0
    for j in range(S):
        for i in range(n_links-2):
            for t in range(Nt):
                #if abs(p[j, i+1, t]) > 1: #DL 1/18/18
                d_p = np.zeros_like(p) #DL
                d_dp = np.zeros_like(dp) #DL
                d_fin = np.zeros_like(fin) #DL
                d_pw = np.zeros_like(pw) #DL

                d_p[j, i+1, t] = (c4*fin[j, i+1, t]*om*((p[j, i+1, t]+dp[j, i, t])/p[j, i+1, t])**(om-1))*dp[j, i, t]/((p[j, i+1, t])**2) #DL
                d_dp[j, i, t] = -(c4*fin[j, i+1, t]*om*((p[j, i+1, t]+dp[j, i, t])/p[j, i+1, t])**(om-1))/p[j, i+1, t]
                d_fin[j, i+1, t] = -c4*(((p[j, i+1, t]+dp[j, i, t])/p[j, i+1, t])**om - 1.0)
                d_pw[j, i, t] = 1.0
                ret[idx, :] = compose_x(p=d_p, dp=d_dp, fin=d_fin, pw=d_pw)
                # if j==0 and i ==0 and t ==1:
                #     for iii in range(len(ret[idx, :])):
                #      if abs( ret[idx,iii] ) > 0:
                #          print(iii)
                idx += 1

    return ret






# inequality constraints #DL todo check that should be >=0 not <=0 (true for ipopt)
def ineq_constr(x):
    p, dp, _, _, _, _, _, _, _, _ = parse_x(x)
    ret = []
    # discharge pressure for compressors
    for j in range(S):
        for i in range(n_links - 2):
            for t in range(Nt):
                ret.append(pmax[i+1] - p[j, i+1, t] - dp[j, i, t])
    return np.array(ret)


# inequality constraints jacobian
# #DL todo check: jacobian shouldn't be transposed (true for pyiopt: every var for eq1, then every var for eq 2...)
#and maybe +- due to >=  / <=
def ineq_constr_jac(x):
    p, dp, _, _, _, _, _, _, _, _ = parse_x(x)
    ret = np.zeros((S*(n_links-2)*Nt, len(x)))
    idx = 0
    for j in range(S):
        for i in range(n_links - 2):
            for t in range(Nt):
                d_p = np.zeros_like(p)
                d_dp = np.zeros_like(dp)
                d_p[j, i+1, t] = -1.0
                d_dp[j, i, t] = -1.0
                ret[idx, :] = compose_x(p=d_p, dp=d_dp)
                idx += 1
    return ret


def cvar_cost(x, alpha):
    f = lambda c: c + (1.0/(1.0-alpha))*sum([max(cost(x, k)-c, 0) for k in range(S)])/S #DL lambda c: c + (1.0/(1.0-alpha))*sum([max(cost(x, k)-c, 0) for k in range(S)]) #DL Expectation so divide
    sol = minimize(f, 0.0)
    return sol.fun


# def bpoe(x, x_val):
#     return 1.0 - inversefunc(cvar_cost, y_values=x_val)