import numpy as np
import sympy as sp
import sympy.abc as s

# values
density_smog = 0.7 # arbitrary value
L = (10**-6) # arbitrary value
viscosity = 1 # arbitrary value
d_particle = 10
g = 9.81
charge = 1.6 * 10**-19 
sigma = 1 # random value
epsilon = 1 
height = 10


# density values
density_fluid = 0.1
density_particle = 0.1

# reynolds eq
Re = (density_smog * (15 * 10**-6) * L) / viscosity

# drag coefficient
Cd = 24 / Re

# multiplied by v^2
v_squared_coefficient = 3/4 * (density_fluid / density_particle) * (Cd / d_particle)

added_values = (g * (density_fluid - density_particle) / density_particle) - ((charge * sigma) / 12 * np.pi**2 * epsilon *
                                                                              density_particle**3)

D_constant_eqn = sp.Eq((2 * charge**2 * s.c) / (12 * np.pi * epsilon * density_particle * d_particle**3 ), s.d)
c_solution = sp.solveset(D_constant_eqn, s.c)
print(c_solution)
