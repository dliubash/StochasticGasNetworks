import numpy as np


# link data
n_links = 5#12 #5 #DL 3#12
LINK = np.array(['l1','l2','l3','l4','l5','l6','l7','l8','l9','l10','l11','l12']) #OK
lstartloc = np.array(['n1','n2','n3','n4','n5','n6','n7','n8','n9','n10','n11','n12']) #OK
lendloc = np.array(['n2','n3','n4','n5','n6','n7','n8','n9','n10','n11','n12','n13']) #OK
ldiam = np.array([920.0, 920.0, 920.0, 920.0, 920.0, 920.0, 920.0, 920.0, 920.0, 920.0, 920.0, 920.0]) #OK
llength = np.array([300.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 300.0]) #OK
ltype = np.array(['p','a','a','a','a','a','a','a','a','a','a','p']) #OK

# node data
n_nodes = n_links + 1#13 #DL 4#13
NODE = np.array(['n1','n2','n3','n4','n5','n6','n7','n8','n9','n10','n11','n12','n13']) #OK
pmin = np.array([57.0, 34.0, 34.0, 34.0, 34.0, 34.0, 34.0, 34.0, 34.0, 34.0, 34.0, 34.0, 39.0]) #OK
pmax = np.array([70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 41.0]) #OK

# supply data
n_sup = 1
SUP = np.array([1]) #OK
sloc = np.array(['n1']) #OK
smin = np.array([0.0]) #OK
smax = np.array([30.0]) #OK

# demand data
n_dem = 1
DEM = np.array([1]) #OK
dloc = np.array(['n13']) #OK
d = np.array([10]) #OK

# scaling factors
rhon = 0.72                                  # density of air at normal conditions - [kg/m3] #OK
ffac = (1e+6*rhon)/(24*3600)                 # from scmx10-6/day to kg/s #OK
ffac2 = (3600)/(1e+4*rhon)                   # from kg/s to scmx10-4/hr #OK
pfac = 1e+5                                  # from bar to Pa #OK
pfac2 = 1e-5                                 # from Pa to bar #OK
dfac = 1e-3                                  # from mm to m #OK
lfac =1e+3                                   # from km to m #OK

# convert units for input data
ldiam = ldiam*dfac                    # from  mm to m #OK
llength = llength*lfac                # from  km to m #OK
smin = smin*ffac*ffac2                # from scmx106/day to kg/s and then to scmx10-4/hr #OK
smax = smax*ffac*ffac2                # from scmx106/day to kg/s and then to scmx10-4/hr #OK
d = d*ffac*ffac2                      # from scmx106/day to kg/s and then to scmx10-4/hr #OK
pmin = pmin*pfac*pfac2                # from bar to Pascals and then to bar #OK
pmax = pmax*pfac*pfac2                # from bar to Pascals and then to bar #OK

eps = 0.025                                             # pipe rugosity - [mm]  #OK
lam = np.array([
    (2*np.log10(3.7*ldiam[i]/(eps*dfac)))**(-2.0)
                for i in range(len(LINK))])             # friction coefficient  #OK
A = (1/4)*np.pi*(ldiam**2)                              # pipe transveral area - [m^2] #OK
Cp = 2.34                                               # heat capacity @ constant pressure [kJ/kg-K] #OK
Cv = 1.85                                               # hat capacity @ constant volume [kJ/kg-K] #OK
gam = Cp/Cv                                             # expansion coefficient [-] #OK
z = 0.80                                                # gas compressibility  - []  #OK
R = 8314.0                                              # universal gas constant [J/kgmol-K]  #OK
Tgas = 293.15                                           # reference temperature [K]  #OK
M = 18.0                                                # gas molar mass [kg/kgmol]  #OK
nu2 = gam*z*R*Tgas/M                                    # gas speed of sound [m/s]  #OK
om = (gam-1)/gam                                        # aux constant [-] #OK
c1 = (pfac2/ffac2)*(nu2/A)  # aux constant [] #OK
c2 = A*(ffac2/pfac2)  # aux constant [] #OK
c3 = np.array([A[i]*(pfac2/ffac2)*(8*lam[i]*nu2)/(np.pi*np.pi*(ldiam[i]**5)) for i in range(len(LINK))]) # aux constant []  #OK
c4 = (1/ffac2)*(Cp*Tgas) # aux constant [kW/(scmx10-4/hr)] #OK

TF = 24*3600                          # horizon time - [s] #OK
Nt = 4 #48#4 #Nt = 6#48 #DL                                # number of temporal grid points #OK
TDEC = 4 #20 #4 #DL 5#20                             # decision time step #OK #<= Nt
assert TDEC <= Nt #DL

TIME = np.arange(1, Nt+1)             # set of temporal grid points  #OK
TIMEm = np.arange(1, Nt)              # set of temporal grid points minus 1  #OK

Nx = 3 #10#3 #DL 5#10                               # number of spatial grid points #OK
DIS = np.arange(1, Nx+1)              # set of spatial grid points  #OK
S = 3                                 # number of scenarios #OK
lambd = 0.9                           # trade-off exp value and cvar #OK
dt = TF/Nt                            # temporal grid spacing - [s]  #OK
dx = llength/(Nx-1)                   # spatial grid spacing - [m]  #OK

# cost factors
ce = 0.1         # cost of compression [$/kWh] #OK
cd = 1e6         # demand tracking cost [-] #OK
cT = 1e6         # terminal constraint cost [-] #OK
cs = 0           # supply cost [$/scmx10-4] #OK
