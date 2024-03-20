import numpy as np
import math
#import sympy as sp
#import sympy.abc as s

# values
density_smog = 6.57 # arbitrary value
L = (10**-5) # arbitrary value
d_particle = 10
g = 9.81
charge = 1.6 * 10**-12
sigma = (1.6 * 10**-19) / 12.25 # random value
epsilon = 8.854187817 * 10**-12
height = 7 # meters
pi = np.pi
percentPollution = 0.04


# density values
density_fluid = 1.293
density_particle = 1000
viscosity = 1.48 * 10**-5 # m^2/s

# reynolds eq
Re = (density_fluid * L)/(viscosity)

print(f"Re: {Re}")
# drag coefficient
Cd = 24 / Re

# multiplied by v
v_coefficient = 3/4 * (density_fluid / density_particle) * (Cd / L)
print(f"v: {v_coefficient}")


height = int(input("Desired height to start: "))
time = 0
concentration = 1 # for one particle
Dlast = 0
v_last = 0
timeStep = .00001




added_values = (g * (density_fluid - density_particle) / density_particle) - ((charge * sigma) / (12 * np.pi**2 * epsilon *
                                                                              density_particle**3))
#multiplied by D and c(t)
dC_coefficient = (2 * charge**2)/(12 * pi * epsilon * density_particle * L**3)

#multiplied by c(t)
c_coefficient = (charge**2 * height)/(12 * pi * epsilon * density_particle * L**3)

print(f"av: {added_values} dC: {dC_coefficient}; c: {c_coefficient}")
while height > Dlast:
    
    Dnext = Dlast + -v_last * timeStep
    
    v_next = v_last + (added_values + v_coefficient * v_last + Dlast * dC_coefficient - c_coefficient) * timeStep
    
    time+= timeStep
    Dlast = Dnext
    v_last = v_next
    
    
    
print(f"time it took to drop at height {height}: {time}")   

print(height / time)