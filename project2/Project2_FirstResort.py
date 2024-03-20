import numpy as np
import math
#import sympy as sp
#import sympy.abc as s

# values
density_smog = 6.57 # arbitrary value
L = (10**-5) # arbitrary value
d_particle = 10
g = 9.81
charge = 1.6 * 10**-19 
sigma = (1.6 * 10**-19) / 12.25 # random value
epsilon = 8.854187817 * 10**-12
height = 7 # meters
pi = np.pi
percentPollution = 0.04


# density values
density_fluid = 1.293
density_particle = 6.57

# reynolds eq
Re = (11 * L)/(15 * 10**-6)
# drag coefficient
Cd = 24 / Re

# multiplied by v
v_coefficient = 3/4 * (density_fluid / density_particle) * (Cd / d_particle)
#constants
added_values = (g * (density_fluid - density_particle) / density_particle) - ((charge * sigma) / 12 * np.pi**2 * epsilon *
                                                                              density_particle**3)
#multiplied by D and c(t)
dC_coefficient = (2 * charge**2)/(12 * pi * epsilon * density_particle * d_particle**3)

#multiplied by c(t)
c_coefficient = (charge**2 * height)/(12 * pi * epsilon * density_particle * d_particle**3)

# sets initial value
Dlast = 0
v_last = 0

# calculations for Euler's method
for t in range(0, 327, 1):
    Dnext = Dlast + -v_last*0.001
    v_next = v_last + (added_values + v_coefficient * v_last + dC_coefficient * (1 - (Dlast/7)) - c_coefficient * (1- (Dlast/7))) * 0.001
    Dlast = Dnext
    v_last = v_next
    

finalConcentration = round((1 - (Dnext/7)), 5)
pollutionErased = 85.75 * percentPollution * ((Dnext/7) * (3600/0.327))
numTowers = math.ceil(30000 / pollutionErased)
print("Final Concentration is", finalConcentration, "% of the original")
print("The amount of air pollution that is cleaned up per hour  (m^3/hr) is", pollutionErased )
print('Compared to the original estimates, ', numTowers, 
      ' towers would need to be implemented to erase 30000 m^3 of air pollution each hour' )



