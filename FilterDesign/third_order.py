"""Topology is like given in the project folder topology.png"""
from calendar import c
from scipy.optimize import fsolve
from math import pi
import numpy as np

cap_table = np.array([0.1, 0.15, 0.18, 0.22, 0.33, 0.47, 0.56, 0.68, 0.82, 0.1, 0.15, 0.18, 0.22, 0.33, 0.47, 0.56, 0.68, 0.82, 1])

def butterworth_get_params(f, gain, r1, r2, r4, init_params):
    r3 = gain * (r1+r2)
    
    w = 2*pi*f
    
    ps1 = 2 / w
    ps2 = 2 / (w**2)
    ps3 = 1 / (w**3)

    def fun(variables) :
        (c1,c2,c3) = variables
        y1 = ((c1 * r1 * r2 + c3 * (r3 * r4 + (r1 + r2) * (r3 + r4))) / (r1 + r2)) - ps1
        y2 = (c3 * (c1 * r1 * (r3 * r4 + r2 * r3 + r2 * r4) + c2 * r3 * r4 * (r1 + r2)) / (r1 + r2)) - ps2
        y3 = (c1 * c2 * c3 * r1 * r2 * r3 * r4 / (r1 + r2)) - ps3
        return [y1, y2, y3]
    
    return fsolve(fun, init_params)

def find_best(f=3.6E3, 
              gain=1, 
              r1s = np.linspace(1E3, 10E3, 20), 
              r2s = np.linspace(5E3, 25E3, 20), 
              r4s = np.linspace(0.33E3, 6.8E3, 20), tries=50):

    
    caps=cap_table * 1E-7
    minnorm = 1E37
    minparams = ()
    
    for r1 in r1s:
        for r2 in r2s:
            for r4 in r4s:
                if ((r2 < (1.25 * r1)) or (r4 > r2)):
                    continue

                for t in range(tries):
                    init_params = np.random.rand(3) * 3E-8 + 1e-10
                    (c1, c2, c3) = butterworth_get_params(f, gain, r1, r2, r4, init_params)

                    mins = np.array([np.min(np.abs(caps - c1) / caps),
                                     np.min(np.abs(caps - c2) / caps),
                                     np.min(np.abs(caps - c3) / caps)])
                    
                    dist = np.max(mins) * np.sum(mins)
                    
                    if minnorm > dist:
                        minparams = (c1, c2, c3, r1, r2, r1+r2, r4)
                        minnorm = dist

    return minparams

result = find_best()
print("cap1:", result[0], " cap2:", result[1], " cap3:", result[2], " r4:", result[3])
