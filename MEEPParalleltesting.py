# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: mp
#     language: python
#     name: python3
# ---

# +
root_path = 'miniconda3'
import sys
sys.path.append(f'{root_path}envs/mp/lib/python3.12.4/site-packages/')

import meep as mp
import numpy as np
import matplotlib.pyplot as plt
from mpi4py.MPI import COMM_WORLD
from IPython.display import clear_output, Math, HTML

# +
comm = COMM_WORLD
rank = comm.Get_rank()

Rankfreq = 0.15 - 0.005*rank
print(f'Hi, im proccess {rank} and im starting the simulation on the wavelength {1/Rankfreq} μm')

# +
cell = mp.Vector3(16,8,0)  # This is the simulation window. Here is defined a 2D-cell with Δx=16um and Δy=8um 

pml_layers = [mp.PML(1.0)]  # Adding an absorbing layer (PML) of thickness 1 μm around all sides of the cell

geometry = [mp.Block(mp.Vector3(mp.inf,1,mp.inf),     # Defines a parallelepiped block of size ∞ × 1 × ∞
                     center=mp.Vector3(),             # Centered at (0,0)
                     material=mp.Medium(epsilon=12))] # Material with ε=12

# By default, any place where there are no objects there is air (ε=1)

# +
sources = [mp.Source(mp.ContinuousSource(frequency=Rankfreq),  # Frequency f corresponds to a vacuum wavelength of 1/0.15=6.67 μm
                     component=mp.Ez,                      # Component Ez to specify a eletric current
                     center=mp.Vector3(7,0))]             # The current is located at (-7,0)

# Is important to leave a little space between sources and the cell boundaries, 
# to keep the boundary conditions from interfering with them.
# -

resolution = 60

sim = mp.Simulation(cell_size=cell,
                    boundary_layers=pml_layers,
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution)

sim.run(until=500)  # Run until a time of t = 500

# ## Parallel Simulation

cores = 4
resultPath = 'ParallelResults/Result.out'

# !jupytext --to py MEEPParalleltesting.ipynb
# !mpirun -np $cores python MEEPParalleltesting.py > $resultPath

# ## Analyze

# Getting the dieletric region

# + tags=["active-ipynb"]
# eps_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Dielectric)
# plt.figure()
# plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
# plt.axis('off')
# plt.show()
# -

# Getting results

# + tags=["active-ipynb"]
# ez_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ez)
# plt.figure()
# plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
# plt.imshow(ez_data.transpose(), interpolation='spline36', cmap='RdBu', alpha=0.9)
# plt.plot(10,39,'go')
# plt.text(4,55,'Source',color='g')
# plt.axis('off')
# plt.plot(80,39,'ro')
# plt.text(4,55,'Field Decay',color='g')
# plt.show()
