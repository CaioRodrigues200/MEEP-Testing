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
from IPython.display import clear_output, Math, HTML
# -

# If the bash !mpirun fails running for some reason, try avoid running the cell below, although it will still be considered in the .py file

# +
from mpi4py.MPI import COMM_WORLD

comm = COMM_WORLD
rank = comm.Get_rank()
# -

# The cell below is for single core meep simulation

# Rankfreq = [0.65146580,0.6493506,0.64724919,0.64516129,0.6430861,0.6410256]
FreqArray = [1/3,1/2.9,1/2.8,1/2.7,1/2.6,1/2.5,1/2.4,1/2.3,1/2.2,1/2.1,1/2,1/1.9,1/1.8,1/1.7,1/1.6,1/1.5,1/1.4,1/1.3,1/1.2,1/1.1,1/1,1/0.9,1/0.8,1/0.7,1/0.6,1/0.5,1/0.4]
print(len(FreqArray))

print(f'Hi, im proccess {rank} and im starting the simulation on the wavelength {1/FreqArray[0]} μm')

# +
cell = mp.Vector3(40,16,0)  # This is the simulation window. Here is defined a 2D-cell

pml_layers = [mp.PML(2.0)]  # Adding an absorbing layer (PML) of thickness 0.1 μm around all sides of the cell

geometry = [mp.Block(mp.Vector3(mp.inf,0.5,0.22), 
                     center=mp.Vector3(),             # Centered at (0,0)
                     material=mp.Medium(epsilon=12))] # Material with ε=12    # Defines a parallelepiped block 

resolution = 30

# + tags=["active-ipynb"]
# print(f'Kc={np.sqrt((1*np.pi/0.5)**2 + (0*np.pi/0.22)**2)}')
# print(f'LambdaC = {3.17*2*np.pi/6.283185307179586}')

# +
sources = [mp.Source(mp.ContinuousSource(frequency=FreqArray[0]),  
                    component=mp.Ez,                     # Component Ez to specify a eletric current
                    center=mp.Vector3(-7,0))]     

# Is important to leave a little space between sources and the cell boundaries, 
# to keep the boundary conditions from interfering with them.

sim = mp.Simulation(cell_size=cell,
                    boundary_layers=pml_layers,
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution)
# -

sim.run(until=200)  # Run until a time of t = 100

# + tags=["active-ipynb"]
# for i in FreqArray:
#
#     print(f'Wavelength: {1/i} μm')
#     sources = [mp.Source(mp.ContinuousSource(frequency=i),  
#                         component=mp.Ez,                     # Component Ez to specify a eletric current
#                         center=mp.Vector3(-16,0))]     
#
#     # Is important to leave a little space between sources and the cell boundaries, 
#     # to keep the boundary conditions from interfering with them.
#
#     sim = mp.Simulation(cell_size=cell,
#                         boundary_layers=pml_layers,
#                         geometry=geometry,
#                         sources=sources,
#                         resolution=resolution)
#     
#     pt = mp.Vector3(0,0)
#
#     sim.run(until=200)  # Run until a time of t = 200
#     #sim.run(until_after_sources=mp.stop_when_fields_decayed(50, mp.Ez, pt, 1e-1))
# -

# ## Parallel Simulation

cores = 1
resultPath = 'ParallelResults/Result.out'

# !jupytext --to py MEEPParalleltesting.ipynb
# !mpirun -np $cores python MEEPParalleltesting.py > $resultPath

# ## Analyze

# Getting the dieletric region

# + tags=["active-ipynb"]
# eps_data = sim.get_array(center=mp.Vector3(), size=mp.Vector3(8,4,0), component=mp.Dielectric)
# plt.figure()
# plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
# plt.axis('off')
# plt.show()
# -

sim.get_array(center=mp.Vector3(), size=mp.Vector3(10,16,0), component=mp.Ez)

# Getting results

# + tags=["active-ipynb"]
# ez_data = sim.get_array(center=mp.Vector3(), size=mp.Vector3(8,4,0), component=mp.Ez)
# plt.figure()
# plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
# plt.imshow(ez_data.transpose(), interpolation='spline36', cmap='RdBu', alpha=0.9)
# plt.axis('off')
# # plt.plot((16/2-7)*resolution,8/2*resolution,'go')
# # plt.text((16/2-7)*resolution,(8/2 + 1)*resolution,'Source',color='g')
# # plt.plot(80,39,'ro')
# # plt.text(4,55,'Field Decay',color='g')
# plt.show()
