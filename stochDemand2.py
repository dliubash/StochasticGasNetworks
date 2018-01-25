# stochastic demand #todo
from data1 import *

rand_s = np.fromfunction(lambda s, j: d[0] * (1 + (s + 1) * 1.0 / 10), (S, n_dem), dtype=int)  # DL
stochd = np.ones((S, n_dem, Nt))  # DL - parameters - stochastic demands - [scmx10-4/hr]

#todo for bpoe
for s in range(S):
    for t in range(Nt):
        if (t <= TDEC):
            stochd[s, 0, t] = d[0]  # for example
        elif t < 30: #todo 30?
            stochd[s, 0, t] = rand_s[s]
        else:
            stochd[s, 0, t] = d[0]

#data for cvar constraints
#todo how to define it?
alphad = 0.9
dstar = 100
alphaf = 0.9
fstar = 200
alphap = 0.9
pstar = 300


"""
# set stochastic demands
param rand_d{k in SCEN,j in DEM}; 

# scenarios
let{k in 1..1,j in 1..1} rand_d[k,j] :=  1.1*d[j];
let{k in 2..2,j in 1..1} rand_d[k,j] :=  1.2*d[j];
let{k in 3..3,j in 1..1} rand_d[k,j] :=  1.3*d[j];

let{k in SCEN,j in DEM,t in TIME: t <= TDEC} stochd[k,j,t]:= d[j];
let{k in SCEN,j in DEM,t in TIME: t >  TDEC && t < 30} stochd[k,j,t]:= rand_d[k,j];
let{k in SCEN,j in DEM,t in TIME: t >= 30} stochd[k,j,t]:= d[j];             
"""
