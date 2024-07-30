root_path = 'miniconda3'
import sys
sys.path.append(f'{root_path}envs/mp/lib/python3.12.4/site-packages/')

import meep as mp
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import clear_output, Math, HTML

cell = mp.Vector3(16,8,0)  # This is the simulation window. Here is defined a 2D-cell with Δx=16um and Δy=8um 

pml_layers = [mp.PML(1.0)]  # Adding an absorbing layer (PML) of thickness 1 μm around all sides of the cell

geometry = [mp.Block(mp.Vector3(mp.inf,1,mp.inf),     # Defines a parallelepiped block of size ∞ × 1 × ∞
                     center=mp.Vector3(),             # Centered at (0,0)
                     material=mp.Medium(epsilon=12))] # Material with ε=12

# By default, any place where there are no objects there is air (ε=1)

sources = [mp.Source(mp.ContinuousSource(frequency=0.15),  # Frequency f corresponds to a vacuum wavelength of 1/0.15=6.67 μm
                     component=mp.Ez,                      # Component Ez to specify a eletric current
                     center=mp.Vector3(-7,0))]             # The current is located at (-7,0)

# Is important to leave a little space between sources and the cell boundaries, 
# to keep the boundary conditions from interfering with them.

resolution = 10

sim = mp.Simulation(cell_size=cell,
                    boundary_layers=pml_layers,
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution)

sim.run(until=20000)  # Run until a time of t = 200