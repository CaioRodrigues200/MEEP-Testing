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

# # 3D

# +
import meep as mp
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio   
import scipy.signal
from scipy.special import erfc
import scipy as sp
from meep.materials import Si,SiO2 ## Problem!
import meep as mp
plt.rcParams["figure.figsize"] = (12,6)

SiO2 = mp.Medium(epsilon=2.25)
Si = mp.Medium(epsilon=12)

resolution = 10  # Original: 45
three_d = True

gdsII_file = 'demo.gds'
CELL_LAYER = 1
ESTRUTURA_LAYER = 2
SOURCE_LAYER = 4
PORT1_LAYER = 3
PORT2_LAYER = 5
PORT3_LAYER = 6
PORT4_LAYER = 7

default_d = 0.3

t_oxide = 2.0
t_Si = 0.22


dpml = 0.5
cell_thickness = dpml+t_oxide+dpml

SiO2 = mp.Medium(epsilon=2.25)
Si = mp.Medium(epsilon=12)

λinicial = 1520e-9 *1e6
λfinal = 1575e-9 *1e6
Npontos = 25

finicial = 1/λfinal
ffinal = 1/λinicial

fArray = 1/np.linspace(λinicial,λfinal,Npontos)


fcen = (ffinal + finicial)/2  # pulse center frequency
df = ffinal - finicial   # pulse width (in frequency)

# -

fArray

# Se o bash !mpirun não rodar por algum motivo, tente não executar esta célula abaixo, apesar de que ela ainda será considerada no arquivo .py

# +
from mpi4py.MPI import COMM_WORLD

comm = COMM_WORLD
rank = comm.Get_rank()

# -

# Proccess call: Use a variável "rank" para instruir o processo

if(mp.am_master()==True): isMaster = 'a Master' 
else: isMaster = 'not a Master'
print(f'Hi, im proccess {rank} and im {isMaster}')

# +
####
cell_zmax = 0.5*cell_thickness if three_d else 0
cell_zmin = -0.5*cell_thickness if three_d else 0
si_zmax = 0.5*t_Si if three_d else 10
si_zmin = -0.5*t_Si if three_d else -10

estrutura = mp.get_GDSII_prisms(Si, gdsII_file, ESTRUTURA_LAYER, si_zmin, si_zmax)

# cell = mp.GDSII_vol(gdsII_file, CELL_LAYER, cell_zmin, cell_zmax)
# p1 = mp.GDSII_vol(gdsII_file, PORT1_LAYER, si_zmin, si_zmax)
# p2 = mp.GDSII_vol(gdsII_file, PORT2_LAYER, si_zmin, si_zmax)
# p3 = mp.GDSII_vol(gdsII_file, PORT3_LAYER, si_zmin, si_zmax)
# p4 = mp.GDSII_vol(gdsII_file, PORT4_LAYER, si_zmin, si_zmax)
# src_vol = mp.GDSII_vol(gdsII_file, SOURCE_LAYER, si_zmin, si_zmax)

cell = mp.GDSII_vol(gdsII_file, CELL_LAYER, cell_zmin, cell_zmax)
p1 = mp.GDSII_vol(gdsII_file, PORT1_LAYER, cell_zmin, cell_zmax)
p2 = mp.GDSII_vol(gdsII_file, PORT2_LAYER, cell_zmin, cell_zmax)
p3 = mp.GDSII_vol(gdsII_file, PORT3_LAYER, cell_zmin, cell_zmax)
p4 = mp.GDSII_vol(gdsII_file, PORT4_LAYER, cell_zmin, cell_zmax)
src_vol = mp.GDSII_vol(gdsII_file, SOURCE_LAYER, cell_zmin, cell_zmax)
sources = [mp.EigenModeSource(src=mp.GaussianSource(fcen,fwidth=df),
                                  volume=src_vol,
                                  eig_parity=mp.NO_PARITY if three_d else mp.EVEN_Y+mp.ODD_Z)]

# sources = [mp.EigenModeSource(src=mp.ContinuousSource(fcen,fwidth=df),
#                               volume=src_vol,
#                               eig_parity=mp.EVEN_Y+mp.ODD_Z)]

size=mp.Vector3(30.4,30.4,0)

# chunk_layout = mp.BinaryPartition(data=[ (mp.X,-10.0), 0, [ (mp.X,0), 1 ,
#                                         [ (mp.X,10.0) , 2 , 3 ]]])

sim = mp.Simulation(resolution=resolution,
                    cell_size=cell.size,
                    boundary_layers=[mp.PML(dpml)],
                    sources=sources,
                    geometry=estrutura,
                    default_material=SiO2,
                    split_chunks_evenly=True)

mode1 = sim.add_mode_monitor(fcen, df, Npontos, mp.ModeRegion(volume=p1))
mode2 = sim.add_mode_monitor(fcen, df, Npontos, mp.ModeRegion(volume=p2))
mode3 = sim.add_mode_monitor(fcen, df, Npontos, mp.ModeRegion(volume=p3))
mode4 = sim.add_mode_monitor(fcen, df, Npontos, mp.ModeRegion(volume=p4))

# -

# ## Aplicação MPI A
#
# 5 cores onde cada um considera todos monitores, com a mesma source, porém cada um com 5 pontos (totalizando os 25) 
#
# É necessário mudar a variável *cores*, mais abaixo no código, para 5
#
# OBS: Veja que a célula abaixo possui a tag "active-ipynb". Portanto ela está DESATIVADA para o uso do mpi. Para ATIVAR, retire a tag

# + tags=["active-ipynb"]
# # mode1 = sim.add_mode_monitor(fcen, df, Npontos, mp.ModeRegion(volume=p1))
# # mode2 = sim.add_mode_monitor(fcen, df, Npontos, mp.ModeRegion(volume=p2))
# # mode3 = sim.add_mode_monitor(fcen, df, Npontos, mp.ModeRegion(volume=p3))
# # mode4 = sim.add_mode_monitor(fcen, df, Npontos, mp.ModeRegion(volume=p4))
#
# fcenRank = (fArray[rank] + fArray[rank+5])/2
# dfRank = fArray[rank] - fArray[rank+5]
#
# print(f'Hi, im proccess {rank} and im starting the simulation with fcen = {fcenRank} and df = {dfRank}.')
#
# Npontos = 5
#
# # MPI TEST: Render 5 monitor points for each proccess -------------------------------------------------------------
# mode1 = sim.add_mode_monitor(fcenRank, dfRank, Npontos, mp.ModeRegion(volume=p1))
# mode2 = sim.add_mode_monitor(fcenRank, dfRank, Npontos, mp.ModeRegion(volume=p2))
# mode3 = sim.add_mode_monitor(fcenRank, dfRank, Npontos, mp.ModeRegion(volume=p3))
# mode4 = sim.add_mode_monitor(fcenRank, dfRank, Npontos, mp.ModeRegion(volume=p4))
# -

# ## Aplicação MPI B
#
# 4 cores onde cada um considera somente um monitor, com a mesma source 
#
# É necessário mudar a variável *cores*, mais abaixo no código, para 4
#
# OBS: A célula abaixo não possui a tag "active-ipynb". Portanto ela está ATIVADA para o uso do mpi. Para DESATIVAR, insira a tag

# + tags=["active-ipynb"]
# # mode1 = sim.add_mode_monitor(fcen, df, Npontos, mp.ModeRegion(volume=p1))
# # mode2 = sim.add_mode_monitor(fcen, df, Npontos, mp.ModeRegion(volume=p2))
# # mode3 = sim.add_mode_monitor(fcen, df, Npontos, mp.ModeRegion(volume=p3))
# # mode4 = sim.add_mode_monitor(fcen, df, Npontos, mp.ModeRegion(volume=p4))
#
# print(f'Hi, im proccess {rank} and im starting the simulation with monitor p{rank+1} only.')
#
# # MPI TEST: Render one monitor for each proccess -------------------------------------------------------------
# if rank==0: mode = sim.add_mode_monitor(fcen, df, Npontos, mp.ModeRegion(volume=p1))
# if rank==1: mode = sim.add_mode_monitor(fcen, df, Npontos, mp.ModeRegion(volume=p2))
# if rank==2: mode = sim.add_mode_monitor(fcen, df, Npontos, mp.ModeRegion(volume=p3))
# if rank==3: mode = sim.add_mode_monitor(fcen, df, Npontos, mp.ModeRegion(volume=p4))
# -

if(mp.am_master()):
    sim.plot2D(output_plane=mp.Volume(center=mp.Vector3(0,0,0), size=mp.Vector3(30.4,30.4,0)))

    plt.savefig("Plot2D (rank " + str(rank) + ").png", transparent=False, facecolor="white", bbox_inches="tight")

# +
print(f'Starting the simulation now... (rank: {rank})')

sim.run(until_after_sources=100)

print(f'Barrier encoutered (rank: {rank})')
comm.barrier()
# -

# # mpirun bash
#
# Ao executar esta célula, todo o arquivo será executado na quantidade de cores descrita
#
# Células com "active-ipynb" serão ignoradas
#
# Requisito: lib jupytext , lib mpi4py, e MPI instalado (https://www.open-mpi.org/software/ompi/v5.0/)

# +
cores = 6
resultPath = 'Result' + str(cores) + 'Cores.out'

# !jupytext --to py meep_MaisATUALIZADO.ipynb
# # !mpirun -np $cores python meep_MaisATUALIZADO.py
# !mpirun -np $cores python meep_MaisATUALIZADO.py > $resultPath

# +
print(f'Simulation finished (rank: {rank})')

sim.plot2D(fields=mp.Ez,
        plot_sources_flag=True,
        plot_monitors_flag=True,
        plot_boundaries_flag=True,
        output_plane=mp.Volume(center=mp.Vector3(0,0,0), size=mp.Vector3(30.4,30.4,0)))

if(mp.am_master()):

        plt.axis('off')
        plt.savefig("Plot2D Ez (rank " + str(rank) + ").png", transparent=False, facecolor="white", bbox_inches="tight")

# +
# S parameters
p1_trans = np.zeros(Npontos)
p2_trans = np.zeros(Npontos)
p3_trans = np.zeros(Npontos)
p4_trans = np.zeros(Npontos)

from IPython.utils import io

for i in range(Npontos):
    p1_coeff = sim.get_eigenmode_coefficients(mode1, [1], eig_parity=mp.NO_PARITY if three_d else mp.EVEN_Y+mp.ODD_Z).alpha[0,i,0]
    p1r_coeff = sim.get_eigenmode_coefficients(mode1, [1], eig_parity=mp.NO_PARITY if three_d else mp.EVEN_Y+mp.ODD_Z).alpha[0,i,1]
    p2_coeff = sim.get_eigenmode_coefficients(mode2, [1], eig_parity=mp.NO_PARITY if three_d else mp.EVEN_Y+mp.ODD_Z).alpha[0,i,1]
    p3_coeff = sim.get_eigenmode_coefficients(mode3, [1], eig_parity=mp.NO_PARITY if three_d else mp.EVEN_Y+mp.ODD_Z).alpha[0,i,0]
    p4_coeff = sim.get_eigenmode_coefficients(mode4, [1], eig_parity=mp.NO_PARITY if three_d else mp.EVEN_Y+mp.ODD_Z).alpha[0,i,0]

    # transmittance
    p1_trans[i] = abs(p1r_coeff)**2/abs(p1_coeff)**2
    p2_trans[i] = abs(p2_coeff)**2/abs(p1_coeff)**2
    p3_trans[i]= abs(p3_coeff)**2/abs(p1_coeff)**2
    p4_trans[i] = abs(p4_coeff)**2/abs(p1_coeff)**2

# -

if(mp.am_master()):
    w = np.linspace(1520,1575,Npontos)
    plt.plot(p3_trans)
    plt.plot(p4_trans)
    plt.figure()
    plt.plot(p1_trans)
    plt.plot(p2_trans)

    plt.savefig("S parameters (rank " + str(rank) + ").png", transparent=False, facecolor="white", bbox_inches="tight")

cores = 4
# !mpirun -np $cores python ../teste.py
